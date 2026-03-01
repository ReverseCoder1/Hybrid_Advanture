"""
Puzzles and challenges module.
World puzzles that players must solve for trust/points.
"""

from utils.config import WIZARD_TOWER


class Puzzles:
    """
    Manages world puzzles and challenges.
    """

    def __init__(self) -> None:
        """Initialize puzzle system."""
        self.wizard_riddle_solved: bool = False
        self.bridge_repaired: bool = False
        self.food_returned: bool = False
        self.sword_blessed_check: bool = False
        self.donation_made: bool = False

    def solve_wizard_riddle(self) -> str:
        """
        Solve Wizard Tower riddle for guard trust.

        Returns:
            Riddle and answer prompt
        """
        return (
            "The Wizard speaks: 'Answer my riddle and earn my respect.'\n"
            "RIDDLE: 'I have cities, but no houses. I have forests, but no trees. "
            "I have water, but no fish. What am I?'\n"
            "(Answer: 'map' or 'a map')"
        )

    def check_riddle_answer(self, answer: str) -> bool:
        """
        Check if riddle answer is correct.

        Args:
            answer: Player's answer

        Returns:
            True if correct
        """
        correct_answers = ["map", "a map", "the map"]
        answer_lower = answer.lower().strip()

        if answer_lower in correct_answers:
            self.wizard_riddle_solved = True
            return True
        return False

    def repair_bridge(self) -> str:
        """
        Repair the Ancient Bridge (structural repair, NOT movement unlock).
        Bridge repair increases guard trust AND is required for final ritual.
        Movement to Mountain Peak only unlocks after defeating Kael in combat.

        Returns:
            Repair message
        """
        self.bridge_repaired = True
        return (
            "You spend time reinforcing the ancient bridge's structure. "
            "The rocks are secured and the pillars are strengthened. "
            "The bridge is structurally sound, and its repairs are noted by the guards.\n"
            "However, General Kael still stands guard. You must defeat him in combat to proceed north."
        )

    def is_bridge_repaired(self) -> bool:
        """
        Check if bridge is repaired.

        Returns:
            True if repaired
        """
        return self.bridge_repaired

    def return_food_to_village(self) -> str:
        """
        Return food to villagers for guard trust.

        Returns:
            Action result
        """
        self.food_returned = True
        return (
            "You gather supplies and bring them to the village. "
            "The grateful villagers thank you for your kindness. "
            "Word of your generosity spreads."
        )

    def is_food_returned(self) -> bool:
        """
        Check if food was returned.

        Returns:
            True if returned
        """
        return self.food_returned

    def donate_to_cause(self, amount: int) -> str:
        """
        Make donation for guard trust (requires 10 points).

        Args:
            amount: Amount to donate

        Returns:
            Donation result
        """
        if amount < 10:
            return f"The guardians need at least 10 points. You offered {amount}."

        self.donation_made = True
        return (
            f"You donate {amount} points to the cause of justice. "
            "The guards acknowledge your support with respect."
        )

    def is_donation_made(self) -> bool:
        """
        Check if donation was made.

        Returns:
            True if donated
        """
        return self.donation_made

    def is_riddle_solved(self) -> bool:
        """
        Check if riddle was solved.

        Returns:
            True if solved
        """
        return self.wizard_riddle_solved
