"""
CS412 - Activity 2: Build a Simple Adaptive Rule
Domain: Instagram

Rule 1: If a user watches 5+ Reels in one session -> boost the Reels
        share of their Home Feed from 20% to 60% for the rest of
        that session.

Rule 2: If 60%+ of a user's last 20 likes/comments are the same
        category (say, Fitness) -> push that category harder on
        their Explore page and in the ads slot.

Why these two specifically: I wanted one rule that reacts fast to
what's happening right now, and one that only kicks in once there's
enough evidence to trust it.

Rule 1 is the "right now" one. If you're five Reels deep in one
sitting, that's a pretty obvious signal you want more of the same,
so the feed should just adjust immediately instead of waiting for
some model to retrain overnight. This is basically the Observation
Layer into Adaptation Layer idea from the behavior based models section
of the module, just compressed into one session.

Rule 2 is the slower the more careful one. I didn't want a single like
to flip the whole Explore page (someone could just be curious, or
misclick), so it only fires once one category makes up a clear
majority of the last 20 interactions. That's the implicit-data idea
from the module - the system isn't asking the user what they like,
it's inferring it from what they keep doing.
"""

import random
from collections import Counter
from datetime import datetime


class InstagramUser:
    """Simulated user - just tracks the two things the rules care about."""

    def __init__(self, username):
        self.username = username
        self.session_reels_watched = 0   # resets each new session, drives Rule 1
        self.recent_interactions = []    # last N liked/commented categories, drives Rule 2
        self.max_history = 20            # window size for Rule 2

    def watch_reel(self):
        self.session_reels_watched += 1

    def engage_with_post(self, category):
        """Like or comment on a post - we only care about its category."""
        self.recent_interactions.append(category)
        # keep only the most recent max_history entries, oldest gets dropped
        if len(self.recent_interactions) > self.max_history:
            self.recent_interactions.pop(0)

    def reset_session(self):
        self.session_reels_watched = 0


class AdaptiveFeedEngine:
    """Takes a user and decides whether the two rules should fire."""

    REELS_WATCH_THRESHOLD = 5
    DEFAULT_REELS_RATIO = 0.20
    BOOSTED_REELS_RATIO = 0.60
    CATEGORY_DOMINANCE_THRESHOLD = 0.60

    def __init__(self, user: InstagramUser):
        self.user = user

    def apply_rule_1(self):
        """If session reel count >= threshold, bump the feed's Reels ratio."""
        if self.user.session_reels_watched >= self.REELS_WATCH_THRESHOLD:
            return self.BOOSTED_REELS_RATIO, True
        return self.DEFAULT_REELS_RATIO, False

    def apply_rule_2(self):
        """If one category dominates recent activity, prioritize it on Explore."""
        history = self.user.recent_interactions
        if not history:
            return None, 0.0, False

        counts = Counter(history)
        top_category, top_count = counts.most_common(1)[0]
        dominance = top_count / len(history)

        if dominance >= self.CATEGORY_DOMINANCE_THRESHOLD:
            return top_category, dominance, True
        return top_category, dominance, False

    def generate_personalized_experience(self):
        reels_ratio, rule1_triggered = self.apply_rule_1()
        top_category, dominance, rule2_triggered = self.apply_rule_2()

        print(f"\n--- Session report for @{self.user.username} ---")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\n[Rule 1] Reels watched this session: {self.user.session_reels_watched}")
        if rule1_triggered:
            print(f"  -> Fired. Reels ratio bumped to {int(reels_ratio * 100)}% "
                  f"(default is {int(self.DEFAULT_REELS_RATIO * 100)}%).")
        else:
            print(f"  -> Not yet. Feed stays at the default {int(reels_ratio * 100)}% Reels.")

        if top_category is not None:
            print(f"\n[Rule 2] Top category in last {len(self.user.recent_interactions)} "
                  f"interactions: {top_category} ({dominance * 100:.0f}%)")
        else:
            print("\n[Rule 2] Nothing to go on yet - no interaction history.")

        if rule2_triggered:
            print(f"  -> Fired. Explore + ads now lean into '{top_category}'.")
        else:
            print("  -> Not yet. Explore stays mixed/general.")

        print("-" * 60)


def simulate():
    """Runs the user through two short sessions so both rules get tested."""
    random.seed(42)
    user = InstagramUser("N-H-H=KANYE")
    engine = AdaptiveFeedEngine(user)

    print("Session 1: normal browsing, shouldn't trigger anything yet")
    user.engage_with_post("Fitness")
    user.engage_with_post("Travel")
    user.watch_reel()
    user.watch_reel()
    engine.generate_personalized_experience()

    print("\nSession 2: reel-watching binge + a bunch of Fitness likes - "
          "this should flip both rules on")
    for _ in range(4):
        user.watch_reel()
    for _ in range(8):
        user.engage_with_post("Fitness")
    for _ in range(3):
        user.engage_with_post("Travel")
    engine.generate_personalized_experience()


if __name__ == "__main__":
    simulate()
