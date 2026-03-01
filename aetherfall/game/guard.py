"""
Guard system module - FIXED.
Captain Ardyn at Castle Gate with trust-based mechanics.
FIXED: Trust increases only through specific actions, each action once.
Trust is capped at max 5 levels, cannot be farmed.
"""


class Guard:
    """
    Manages Captain Ardyn's trust and interactions.
    Trust increases only through SPECIFIC actions, tracked with flags.
    Each action can only grant trust once.
    Trust is capped at 5 levels maximum.
    """

    def __init__(self) -> None:
        """Initialize guard system with action tracking."""
        self.trust_level: int = 0  # 0-5 scale
        self.max_trust: int = 5

        # Action flags - each can only trigger once for trust
        self.solved_riddle: bool = False
        self.blessed_sword: bool = False
        self.donated_to_village: bool = False
        self.refused_crown: bool = False
        self.repaired_bridge: bool = False

        # Rewards given
        self.has_given_oath_token: bool = False
        self.has_taught_true_strike: bool = False

        self.location: str = "Castle Gate"

    def add_trust_from_action(self, action: str) -> str:
        """
        Add trust from a specific action. Can only be done once per action.

        Args:
            action: Name of action completed

        Returns:
            Result message
        """
        if action == "solve_riddle" and not self.solved_riddle:
            self.solved_riddle = True
            self.trust_level = min(self.trust_level + 1, self.max_trust)
            return "Captain Ardyn nods approvingly. 'I see you have wisdom.' (+1 Trust)"

        elif action == "bless_sword" and not self.blessed_sword:
            self.blessed_sword = True
            self.trust_level = min(self.trust_level + 1, self.max_trust)
            return "Captain Ardyn watches you bless your blade. 'Good. You prepare wisely.' (+1 Trust)"

        elif action == "donate_village" and not self.donated_to_village:
            self.donated_to_village = True
            self.trust_level = min(self.trust_level + 1, self.max_trust)
            return "Captain Ardyn hears of your kindness in the village. 'Compassion speaks volumes.' (+1 Trust)"

        elif action == "refuse_crown" and not self.refused_crown:
            self.refused_crown = True
            self.trust_level = min(self.trust_level + 1, self.max_trust)
            return "Captain Ardyn sees you reject the Crown. 'You have strength of character.' (+1 Trust)"

        elif action == "repair_bridge" and not self.repaired_bridge:
            self.repaired_bridge = True
            self.trust_level = min(self.trust_level + 1, self.max_trust)
            return (
                "Captain Ardyn sees you mend what was broken. 'A true hero.' (+1 Trust)"
            )

        return ""  # Action already completed or invalid

    def get_trust(self) -> int:
        """
        Get current trust level (0-5).

        Returns:
            Trust level
        """
        return self.trust_level

    def is_fully_trusted(self) -> bool:
        """
        Check if player has maximum trust.

        Returns:
            True if trust >= 4 (high trust)
        """
        return self.trust_level >= 4

    def talk_to_guard(self) -> str:
        """
        Interact with guard - dialogue changes based on trust.
        Talking alone does NOT increase trust.

        Returns:
            Guard's dialogue based on trust level
        """
        if self.trust_level == 0:
            return (
                "Captain Ardyn eyes you suspiciously. 'I don't know you, stranger. "
                "Prove yourself through action, not words.'"
            )
        elif self.trust_level == 1:
            return (
                "Captain Ardyn nods slightly. 'You show some promise. "
                "Continue to prove yourself worthy.'"
            )
        elif self.trust_level == 2:
            return (
                "Captain Ardyn: 'I am beginning to see your value, traveler. "
                "Do not disappoint me.'"
            )
        elif self.trust_level == 3:
            return (
                "Captain Ardyn: 'You have shown courage and wisdom. " "I respect that.'"
            )
        elif self.trust_level >= 4:
            return (
                "Captain Ardyn: 'You have proven yourself worthy. "
                "You have earned my full trust and respect.'"
            )
        return ""

    def get_trust_hint(self) -> str:
        """
        Get a hint about how to increase trust.

        Returns:
            Hint message
        """
        if self.trust_level >= self.max_trust:
            return (
                "Captain Ardyn regards you with deep respect. You have his full trust."
            )

        hints = []
        if not self.solved_riddle:
            hints.append("Solve the Wizard's riddle")
        if not self.blessed_sword:
            hints.append("Bless your weapon at the River")
        if not self.donated_to_village:
            hints.append("Show kindness to the village")
        if not self.refused_crown:
            hints.append("Reject objects of corruption")
        if not self.repaired_bridge:
            hints.append("Repair what is broken")

        if hints:
            return f"To earn trust: {', '.join(hints[:2])}"
        return "You have earned great trust."

    def give_oath_token(self) -> str:
        """
        Give oath token to player if fully trusted.
        Oath Token is REQUIRED for final ritual.

        Returns:
            Dialogue and result
        """
        if self.trust_level < 4:
            return (
                f"Captain Ardyn: 'You are not yet worthy. "
                f"You have earned {self.trust_level}/5 trust. Return when you have proven yourself more.'"
            )

        if self.has_given_oath_token:
            return "Captain Ardyn: 'I have already given you the Oath Token.'"

        self.has_given_oath_token = True
        return (
            "Captain Ardyn: 'You have shown true worth. Take this Oath Token. "
            "It is proof of your character and required for the final ritual. Use it wisely.'"
        )

    def teach_true_strike(self) -> str:
        """
        Teach True Strike technique if fully trusted.

        Returns:
            Dialogue and result
        """
        if self.trust_level < 4:
            return "Captain Ardyn: 'Such knowledge is not for the unworthy.'"

        if self.has_taught_true_strike:
            return "Captain Ardyn: 'You already know the True Strike.'"

        self.has_taught_true_strike = True
        return (
            "Captain Ardyn: 'The True Strike is the only way to pierce the Shadow King's defenses. "
            "Use it in the final moment when his HP is gone. It is the ritual that seals his fate.'"
        )

    def get_status_string(self) -> str:
        """
        Get status of guard relationships.

        Returns:
            Status description
        """
        trust_str = f"Trust: {self.trust_level}/5"

        rewards = []
        if self.has_given_oath_token:
            rewards.append("✓ Oath Token given")
        if self.has_taught_true_strike:
            rewards.append("✓ True Strike taught")

        if rewards:
            return f"{trust_str} | {', '.join(rewards)}"
        return trust_str
