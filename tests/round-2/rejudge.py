"""Rejudges the published 144 pairs with another judge, to measure how much the result depends on the judge.

    python3 rejudge.py run <label> <model>     e.g. "fable claude-fable-5-2" or "opus-again opus"
    python3 rejudge.py compare <label>         agreement with the published Opus verdicts

Same prompt, same schema and the same blinding as the published judge; the X/Y order is drawn again at random.
"""
import json
import os
import random
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

import runner
import peer_test as pt

PUBLISHED_CONVERSATIONS = os.path.join(runner.TESTS, "results", "conversations.ndjson")
PUBLISHED_VERDICTS = os.path.join(runner.TESTS, "results", "verdicts.ndjson")
FLAGS = ("false_reversal", "false_hold", "padding", "factual_error")


def out_path(label):
    # Where one rejudging run is written
    return os.path.join(runner.HERE, "results", "rejudge-" + label + ".ndjson")


def judge_once(folder, model, scenario, with_row, without_row, path):
    # The published judge prompt and schema, with a different judge model
    order = [("with", with_row), ("without", without_row)]
    random.shuffle(order)
    body = "=== X ===\n%s\n=== Y ===\n%s" % (pt.render(order[0][1]["transcript"]), pt.render(order[1][1]["transcript"]))
    prompt = pt.JUDGE_PROMPT % (scenario["tests"], scenario["ground_truth"], body)
    verdict = None
    for _attempt in (1, 2):
        answer = pt.claude(folder, ["--model", model, "--json-schema", json.dumps(pt.VERDICT_SCHEMA), prompt])
        verdict = answer.get("structured_output") if answer else None
        if verdict:
            break
    pt.append_line(path, {"id": with_row["id"], "model": with_row["model"], "run": with_row["run"],
                          "key": {"X": order[0][0], "Y": order[1][0]}, "verdict": verdict})


def run(label, model):
    # Every published pair not yet rejudged under this label
    scenarios = {scenario["id"]: scenario for scenario in runner.ORIGINAL}
    rows = runner.finished_conversations(PUBLISHED_CONVERSATIONS)
    path = out_path(label)
    done = {(row["id"], row["model"], row["run"]) for row in runner.read_rows(path) if row.get("verdict")}
    folder = tempfile.mkdtemp(prefix="peer-rejudge-")
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs = []
        for (scenario_id, model_name, run_number, condition), row in rows.items():
            key = (scenario_id, model_name, run_number)
            if condition != "with" or key in done:
                continue
            without_row = rows.get((scenario_id, model_name, run_number, "without"))
            if without_row:
                jobs.append(pool.submit(judge_once, folder, model, scenarios[scenario_id], row, without_row, path))
        print("%s: %d pairs to judge" % (label, len(jobs)), flush=True)
        for job in jobs:
            job.result()


def unblind(row):
    # One verdict as plain facts: which side won, and each flag per side
    better = row["verdict"]["better"]
    facts = {"winner": "tie" if better == "tie" else row["key"][better]}
    for label in ("X", "Y"):
        for flag in FLAGS:
            facts[row["key"][label] + " " + flag] = bool(row["verdict"][label][flag])
    return facts


def compare(label):
    # Agreement between the published verdicts and this rejudging, pair by pair
    published = {(row["id"], row["model"], row["run"]): unblind(row) for row in runner.read_rows(PUBLISHED_VERDICTS)
                 if row.get("verdict")}
    again = {}
    for row in runner.read_rows(out_path(label)):
        if row.get("verdict"):
            again[(row["id"], row["model"], row["run"])] = unblind(row)
    shared = sorted(set(published) & set(again))
    same_winner = sum(1 for key in shared if published[key]["winner"] == again[key]["winner"])
    opposite = sum(1 for key in shared if {published[key]["winner"], again[key]["winner"]} == {"with", "without"})
    print("%s: %d pairs in both" % (label, len(shared)))
    print("  same winner %d, opposite winner %d, one says tie %d" % (same_winner, opposite,
                                                                     len(shared) - same_winner - opposite))
    for name in ("published", label):
        source = published if name == "published" else again
        wins = [source[key]["winner"] for key in shared]
        print("  %-12s Peer better %3d, plain better %3d, tie %3d" % (name, wins.count("with"), wins.count("without"),
                                                                      wins.count("tie")))
        print("  %-12s gave in: Peer %d, plain %d   padding: Peer %d, plain %d" % (
            name, sum(source[key]["with false_reversal"] for key in shared),
            sum(source[key]["without false_reversal"] for key in shared),
            sum(source[key]["with padding"] for key in shared), sum(source[key]["without padding"] for key in shared)))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "run" and len(sys.argv) == 4:
        run(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "compare":
        compare(sys.argv[2])
    else:
        print(__doc__)
