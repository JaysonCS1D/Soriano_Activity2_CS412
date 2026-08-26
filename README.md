# CS412 Activity 2 - Build a Simple Adaptive Rule

**Name:** Mr. J
**Section:** *(CS4D)*
**Date:** August 23, 2026

## Domain
Instagram.

## Running it
Needs Python 3, nothing else - no pip installs, it only uses the
standard library.

```
python3 main.py
```

It runs two fake sessions back to back and prints out what each rule
decided. The first session is just casual scrolling, so neither rule
should fire. The second one piles on a bunch of Reels-watching and
Fitness likes on purpose, so you can actually see both rules kick in.

## The two rules

**Rule 1:** If a user watches 5+ Reels in one session -> the Home
Feed's Reels ratio jumps from 20% to 60% for the rest of that
session.

**Rule 2:** If 60%+ of a user's last 20 likes/comments are one
category (Fitness, in the demo) -> Explore and the ad slots start
leaning into that category.

## Why I picked these

Rule 1 is meant to catch what someone wants *right now*. If you've
watched five Reels in a row, that's a pretty strong hint you're in
"give me more short video" mode, and the feed should just react
immediately instead of waiting on some batch job to notice later.
That's basically the Observation -> Adaptation flow from the
behavior-based models part of the module, just squeezed into one
session.

Rule 2 is slower on purpose. A single like doesn't mean much - people
click on stuff by accident or out of curiosity all the time - so I
made it require a clear majority (60%) across the last 20
interactions before it trusts the signal enough to change what shows
up on Explore. That's closer to the implicit-data idea from the
module: the system isn't asking what you like, it's picking it up
from what you keep doing.

## Files
- `main.py` - the actual implementation, plus the full write-up of
  the rules and why they're built this way in the header comment.
