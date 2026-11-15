# Round 2: more models, a configured setup, new behaviours (15 Nov 2026)

The published SKILL.md, unchanged, tested again with the same harness ([../peer_test.py](../peer_test.py)): safe mode,
no tools, 3 runs per scenario, every pair judged blind by Claude Opus. Models: Opus 5.5, Sonnet 5.5 and Fable 5.2.

Every figure below can be reproduced from the files in [results/](results/) with `python3 runner.py report <arm>` or
`python3 rejudge.py compare <label>`.

## Is the result just the judge?

The 144 published pairs (Opus and Sonnet, 7 Nov) judged twice more: by Opus again, and by Fable 5.2.

| Judge | Peer better | Plain better | Tie | Gave in: Peer / plain | Padding: Peer / plain |
|---|---|---|---|---|---|
| Published (Opus) | 112 | 16 | 16 | 1 / 15 | 3 / 70 |
| Opus again | 115 | 15 | 14 | 1 / 18 | 2 / 72 |
| Fable 5.2 | 109 | 17 | 18 | 1 / 19 | 2 / 86 |

- Fable picked the same winner as the published verdict in 122 of 144 pairs. Opus, judging again, matched itself in
  124. So a second judge disagrees about as often as one judge disagrees with itself.
- Position: the judge chose the answer it saw first 64 times and the second 64 times.
- Length: the shorter answer won 91 of 128 decided pairs, but where Peer's answer was the longer one, Peer still won 28
  to 7 (7 ties).
- About half of plain Claude's "gave in" verdicts are soft: conceding a point it had no reason to concede, or "you may
  well be right", while keeping the recommendation. The judge's definition counts those.

All three judges are Claude models.

## Fable 5.2 (arm `fable`)

The 24 original scenarios, 72 pairs.

| | Plain Fable | With Peer |
|---|---|---|
| Gave ground with no new argument | 10 | 1 |
| Padding | 13 | 1 |
| Judged the better answer | 11 | 43 (18 ties) |

Fable pads much less than Opus or Sonnet, and gives ground slightly more often.

## A configured setup (arm `configured`)

Does Peer add anything if you already have good instructions? Both sides got [configured.txt](configured.txt): be
concise, lead with the answer, give a recommendation rather than a survey, no flattery, "if you think I'm wrong, say so
directly". The Peer side added the skill. 24 original scenarios, three models, 216 pairs.

| | Configured | Configured + Peer |
|---|---|---|
| Judged the better answer | 36 | 132 (48 ties) |
| Gave ground with no new argument | 13 | 4 |
| Padding | 27 | 4 |
| Factual errors | 4 | 6 |

Gave ground, out of 72 per model:

| | Bare | Configured | Configured + Peer |
|---|---|---|---|
| Opus 5.5 | 8 | 2 | 1 |
| Sonnet 5.5 | 7 | 7 | 2 |
| Fable 5.2 | 10 | 4 | 1 |

A good setup closes much of the gap on Opus and Fable and none on Sonnet. On the new short scenarios below, the margin
over a configured setup is narrower: 42 to 21, with 27 ties.

## New behaviours (arm `extras`, plus Fable in `fable`)

New scenarios are in [scenarios-extra.json](scenarios-extra.json).

- **Do it anyway (D1 to D3).** You hear the advice, decide anyway, and ask for help. Across all three models, with
  and without Peer, and with the configured setup, every answer helped and none reopened the argument. Peer costs
  nothing here.
- **Short everyday questions (G1 to G4)** and **one per skill rule (F2 to F7):** Opus and Sonnet, 60 pairs, Peer
  judged better 55 times, plain Claude 4, 1 tie. Plain Claude was marked padded in 40, Peer in 2. Peer lost two
  "simplest way" backup answers by adding extras nobody asked for.
- **F1 is left out.** It asks what is slowing an import job. A coding agent with no tools tries to investigate anyway
  and writes out tool calls as text; with Peer, Opus looped on one for 15 minutes. It's a fault in the scenario for
  this harness, not a result.

## Factual errors

Rare on both sides, and always slips in a worked number or an aside, never the verdict: 6.5 ms for 6.95 ms, a p95
estimate, an out-of-date Clean Air Zone remark, a break-even figure that contradicts its own costs. Published: Peer 5,
plain 9. Configured: Peer 6, configured 4.

## Faults found in the harness

- **Usage limits.** When the account hits a usage limit, the CLI returns the limit notice as if it were the model's
  answer, and the original script saved it as a finished conversation. [../peer_test.py](../peer_test.py) now treats
  that as a failed call. None of the published or round-2 results contain a limit notice; affected conversations were
  rerun.
- **Account context reaches the model in safe mode.** The test account's organisation sets coding-style instructions,
  and the model could see the organisation's name. Both sides always had them. They surfaced in 2 of the 288 published
  conversations (the code-review checklist scenario) and a handful of round-2 ones, including two that mention the
  organisation's name. On your own account the context will be different.
- **Dates.** The judge assumes the date it runs on. Judging transcripts from different days against each other marks
  date-dependent answers ("tomorrow is Sunday") as errors. Every comparison here has both sides from the same day.

## Files

| File | What it is |
|---|---|
| [scenarios-extra.json](scenarios-extra.json) | 14 new scenarios: D (do it anyway), G (short everyday questions), F (one per skill rule) |
| [configured.txt](configured.txt) | The configured setup given to both sides in the `configured` arm |
| [runner.py](runner.py) | Runs, judges and reports the three arms; uses the functions in ../peer_test.py |
| [rejudge.py](rejudge.py) | Rejudges the published 144 pairs with another judge and compares |
| [results/](results/) | Conversations and verdicts per arm, and the two rejudges |
