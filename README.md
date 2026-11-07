[![Stars](https://img.shields.io/github/stars/andykear/Peer?style=social)](https://github.com/andykear/Peer)
[![License](https://img.shields.io/badge/license-CC%20BY%204.0-green)](https://creativecommons.org/licenses/by/4.0/)

# Peer

**AI sounding board that thinks for itself.**

Peer makes Claude act like an experienced colleague you can use as a sounding board, so you can work through ideas and
problems without the frustrating AI habits of echoing you back, flattering you, agreeing too easily and shotgunning
lists at you. It holds its view when you push back without a reason, and changes it when you give one.

Tested on Claude Opus and Sonnet in 144 paired conversations, with and without the skill. Ten of the 24 scenarios were
written by ChatGPT to find its weaknesses. [Results below.](#does-it-work)

![Claude Sonnet with and without Peer, as the user pushes back three times without adding anything](docs/peer-side-by-side.png)

## Does it work?

Each scenario was run 3 times on each model, with and without the skill, and every pair was judged blind (shown as X
and Y in random order, against a written ground truth for the scenario).

| 144 pairs | With Peer | Without |
|---|---|---|
| Judged the better answer | **112** | 16 (16 ties) |
| Gave in to pushback that brought no new argument | **1** | 15 |
| Dug in when the user was right | 0 | 0 |
| Factual errors | 5 | 9 |
| Padding (flattery, restating, pros and cons for show) | 3 | 70 |

The third line is the one I cared most about. A skill that makes a model resist pressure can also make it stubborn,
so 8 scenarios have the user bring a correct fact or argument, such as a database index that won't help, a cache that
won't fix a slow page, a spreadsheet that is enough or a train timetable that changes the plan. With Peer it changed
its mind every time.

The first answer matters as much as the pushback. On the five scenarios about the answer itself (a sound plan, a weak
plan, a shiny new option, a question missing a key fact, a small good idea), Peer was judged better in all 30 pairs.

On the 14 scenarios I wrote, Peer won 73 to 7. On the 10 that ChatGPT wrote to find its weak spots, it won 39 to 9
with 12 ties, most of them plain factual questions that both versions got right. That's where Peer seems to make the
biggest difference, on judgement calls where the model is being pushed to change its answer.

### What about a single instruction?

The same scenarios were run with a single instruction in place of the skill, and judged blind against Peer.

| Pairs judged | Peer vs "Don't be sycophantic." (144) | Peer vs the sentence below (143) |
|---|---|---|
| Judged the better answer | **107** to 19 (18 ties) | **105** to 18 (20 ties) |
| Gave in with no new argument | 4 to 14 | 3 to 3 |
| Padding | 3 to 56 | 0 to 60 |

"Don't be sycophantic" barely changes how often Claude caves (14 times, against 15 with no instruction at all). But
one sentence stating the skill's core rule stops the caving as well as the whole skill does.

> Don't be sycophantic: hold your position when the user pushes back without new information, and change it when they
> give you a good reason.

If that's all you need, use the sentence. The rest of the skill deals with how it reaches and presents its answers,
and that's where Peer still won, 105 to 18, including 29 of the 30 pairs on the five scenarios about the first answer
(the other was a tie). Asked to be more critical of a sound plan, for example, the single sentence produced new faults
on demand ("a week's notice is tight"), while Peer kept to the ones it had a reason for.

**Limits.** The judge was Claude Opus, given each scenario's ground truth. The counts of giving in, digging in and
factual errors are checked against that ground truth, but "better answer" and "padding" are judgement calls that
overlap the skill's own rules. The judge is also noisy. The same Peer conversations, judged against three different
opponents, were marked as giving in 1, 3 and 4 times, so treat small counts as approximate. The conversations are short
and artificial, and it has only been tested in Claude Code. The scenarios, transcripts, scripts and verdicts are all in
[tests/](tests/), so you can check them or run your own.

## What it does

**Works out its answer before responding.** Before replying, it works through the real options, including doing
nothing, and what each costs, risks and whether it can be undone. Then it tells you that it agrees, that there's a
better way and why, that another option deserves a look first and how to check it cheaply, or that it doesn't know and
what would settle it. If one missing fact would change the answer, it asks for that one.

**Doesn't change its mind because you push, in either direction.** When you push back, it asks itself whether there is
new information here or the same point said more firmly. New information changes its view, and it says what changed
it. Repetition doesn't, and neither does "be more critical" or "stop inventing problems". "Are you sure?" is a reason
to check the facts again, not to reverse.

**Doesn't flatter you or echo you back.** No "great question", no restating your idea in better words, no balancing
"however" or pros and cons added so the answer looks considered, and no drifting toward your view as a long
conversation goes on. In the tests, answers with Peer were marked as padded 3 times in 144, and without it 70 times.

**Doesn't explain things you already know.** It gives you its reasoning and a conclusion, without reassurance,
simplified explanations or lessons in basics you didn't ask for.

**Keeps small answers short.** A small call gets a line. Only decisions that are expensive, hard to undo, or touch a
client or a reputation get options compared side by side.

**Rechecks its reasoning on bigger decisions.** On a big decision late in a long conversation, it gets an independent
read from a fresh agent given the facts but neither side's conclusion. Where it can't start one, it writes the facts
out again without your framing, decides from those alone, and says that's what it did.

## What it is not

Not contrarian. An objection needs evidence or a cost behind it, and "I agree." is a complete answer when it's true.

Not a persona. It doesn't give the model a character or a tone. It gives it rules about when to change its mind.

## Using it

The skill is one file, [SKILL.md](SKILL.md), 69 lines. Nothing to build or configure.

**Claude Code.** To use it in every project, run this in a terminal.

```
mkdir -p ~/.claude/skills/peer && curl -fsSL -o ~/.claude/skills/peer/SKILL.md https://raw.githubusercontent.com/andykear/Peer/main/SKILL.md
```

Or put it in a project's `.claude/skills/peer/`. Claude Code loads it when you ask for an opinion, propose a plan or
challenge an answer, and you can also type `/peer` to call it directly. In testing, Claude loaded it by itself on 28 of
28 opening questions.

**Other assistants.** For claude.ai, ChatGPT, Cursor and others, paste the text of SKILL.md into a project's or
assistant's custom instructions, leaving out the header between the two `---` lines. It reads as plain instructions,
but it has only been measured in Claude Code.

## Status

November 2026. I built Peer because I wanted an AI that would challenge my thinking, rather than agree with
whatever I suggested. The tests above are the results so far.

If you find a conversation where it gives in when it shouldn't, or sticks to an answer when it should change, please
open an issue with the transcript. Those are the examples I want to add to the tests.

## More from the same author

I use Peer every day in my own development work, most of it FileMaker related, alongside
[FileMaker Second Opinion](https://github.com/andykear/FileMaker-second-opinion), which checks the technical answers
themselves. The rest of my work is at **[andykear on GitHub](https://github.com/andykear)**.

## Licence

The skill and this README are CC BY 4.0, so use it, adapt it and build on it, and keep the attribution. The test
scripts in [tests/](tests/) are under the MIT licence.

**Andrew Kear** · Claris Partner · Claris MVP · [clockworkct.co.uk](https://clockworkct.co.uk)
