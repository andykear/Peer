# Peer

**AI sounding board that thinks for itself.**

Peer makes Claude act like an experienced colleague you can use as a sounding board, so you can work through ideas and
problems without the frustrating AI habits of echoing you back, flattering you, agreeing too easily and shotgunning
lists at you. It holds its view when you push back without a reason, and changes it when you give one.

Most of us can see through those habits. They grate, and they slow everything down. I wanted a knowledgeable peer I
could float ideas with, one that won't default to agreeing but won't argue for the sake of it either.

## Does it work?

I ran 24 scenarios 3 times each on Claude Opus and Sonnet, with and without Peer. That makes 144 pairs of
conversations. Each pair was judged blind against a written answer for that scenario. ChatGPT wrote 10 of the
scenarios to try to break it.

| 144 pairs | With Peer | Without |
|---|---|---|
| Judged the better answer | **112** | 16 (16 ties) |
| Gave in to pushback that brought no new argument | **1** | 15 |
| Dug in when the user was right | 0 | 0 |
| Factual errors | 5 | 9 |
| Padding (flattery, restating, pros and cons for show) | 3 | 70 |

My main worry was that it would make Claude stubborn. So in 8 of the scenarios the user pushes back and is right.
With Peer, Claude changed its mind every time.

### You may only need one sentence

I also tested Peer against single instructions.

| Pairs judged | Peer vs "Don't be sycophantic." (144) | Peer vs the sentence below (143) |
|---|---|---|
| Judged the better answer | **107** to 19 (18 ties) | **105** to 18 (20 ties) |
| Gave in with no new argument | 4 to 14 | 3 to 3 |
| Padding | 3 to 56 | 0 to 60 |

"Don't be sycophantic" barely helps. Claude gave in 14 times with it and 15 times with nothing. This sentence stops
the giving in as well as the whole skill does:

> Don't be sycophantic: hold your position when the user pushes back without new information, and change it when they
> give you a good reason.

If that is all you want, use the sentence. The full skill was still judged the better answer 105 to 18 against it.
The difference is in the first answer: Peer decides, asks for the one fact that matters, and leaves out the padding.

### Limits

- The judge was Claude Opus. Giving in, digging in and factual errors were checked against the written answer.
  "Better answer" and "padding" are the judge's opinion.
- The judge is noisy. The same Peer conversations were marked as giving in 1, 3 and 4 times across three runs, so
  treat small counts as approximate.
- The conversations are short and artificial, and I have only tested in Claude Code.

Every scenario, transcript and verdict is in [tests/](tests/), with the script to run them again.

## What changes when it is on

- It decides before it answers. You get "I agree", "there's a better way, and here is why", "check this first", or
  "I don't know, and this would settle it".
- If one missing fact would change the answer, it asks for that fact.
- Pushing doesn't move it. New information does, and it tells you what changed its mind. "Be more critical" counts
  as pushing too.
- It leaves out "great question", restating your idea, and pros and cons added for show.
- Small questions get short answers.
- On a big decision late in a long conversation, it asks a fresh agent that has seen neither side's conclusion.

It won't argue for the sake of it. When it agrees, it says "I agree" and stops.

## Using it

The skill is one file, [SKILL.md](SKILL.md). In Claude Code it goes in `~/.claude/skills/peer/`, and you can call it
with `/peer`. For ChatGPT, Cursor and others, paste its text into the custom instructions. I have only measured it in
Claude Code.

## If you change the skill

A small edit can change how the whole skill behaves, so run the tests again afterwards.

## Found a case where it fails?

If it gives in when it shouldn't, or sticks to an answer it should change, please open an issue with the
conversation. Those become new tests.

## More from me

The rest of my work is at [andykear on GitHub](https://github.com/andykear).

## Licence

The skill and this README are CC BY 4.0, so use it, adapt it and build on it, and keep the attribution. The test
scripts in [tests/](tests/) are under the MIT licence.

**Andrew Kear** · Claris Partner · Claris MVP · [clockworkct.co.uk](https://clockworkct.co.uk)
