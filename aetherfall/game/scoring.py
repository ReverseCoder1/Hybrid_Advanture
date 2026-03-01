"""
Scoring system module.
Tracks points and achievements.
"""

from typing import Dict, Set
from utils.config import SCORING_MILESTONES


class Scoring:
    """
    Manages player's score and milestones.
    """

    def __init__(self) -> None:
        """Initialize scoring system."""
        self.visible_points: int = 0
        self.secret_points: int = 0
        self.achieved_milestones: Set[int] = set()

    def add_visible_points(self, amount: int) -> None:
        """
        Add visible points.

        Args:
            amount: Points to add
        """
        self.visible_points += amount

    def add_secret_points(self, amount: int) -> None:
        """
        Add secret points.

        Args:
            amount: Secret points to add
        """
        self.secret_points += amount

    def get_total_score(self) -> int:
        """
        Get total score (visible + secret).

        Returns:
            Total score
        """
        return self.visible_points + self.secret_points

    def get_visible_score(self) -> int:
        """
        Get visible score.

        Returns:
            Visible points
        """
        return self.visible_points

    def get_secret_score(self) -> int:
        """
        Get secret score.

        Returns:
            Secret points
        """
        return self.secret_points

    def check_milestones(self) -> str:
        """
        Check for newly achieved milestones.

        Returns:
            String describing new milestones
        """
        achievements = []
        total_score = self.get_total_score()

        for threshold in sorted(SCORING_MILESTONES.keys()):
            if threshold <= total_score and threshold not in self.achieved_milestones:
                self.achieved_milestones.add(threshold)
                achievements.append(SCORING_MILESTONES[threshold])

        if achievements:
            return "\n🏆 Milestone Achieved: " + ", ".join(achievements)
        return ""

    def get_score_string(self) -> str:
        """
        Get formatted score display.

        Returns:
            Score display string
        """
        total = self.get_total_score()
        return f"Score: {self.visible_points} visible + {self.secret_points} secret = {total} total"
