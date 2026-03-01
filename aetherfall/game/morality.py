"""
Morality and trust tracking module.
Tracks player's moral alignment and corruption.
"""


class Morality:
    """
    Tracks player's moral alignment and corruption from actions.
    """

    def __init__(self) -> None:
        """Initialize morality system."""
        self.corruption: int = 0
        self.righteousness: int = 0

    def add_corruption(self, amount: int) -> None:
        """
        Apply corruption (negative alignment).

        Args:
            amount: Corruption points
        """
        self.corruption += amount

    def add_righteousness(self, amount: int) -> None:
        """
        Apply righteousness (positive alignment).

        Args:
            amount: Righteousness points
        """
        self.righteousness += amount

    def is_corrupted(self) -> bool:
        """
        Check if player is corrupted.

        Returns:
            True if corruption > righteousness
        """
        return self.corruption > self.righteousness

    def get_alignment(self) -> str:
        """
        Get player's moral alignment.

        Returns:
            Alignment description
        """
        balance = self.righteousness - self.corruption
        if balance > 20:
            return "Pure of Heart"
        elif balance > 5:
            return "Virtuous"
        elif balance > -5:
            return "Neutral"
        elif balance > -20:
            return "Tainted"
        else:
            return "Corrupted"

    def get_corruption_level(self) -> int:
        """
        Get net corruption level.

        Returns:
            Corruption - Righteousness
        """
        return self.corruption - self.righteousness

    def handle_crown_worn(self) -> None:
        """Apply corruption when crown is worn."""
        self.add_corruption(10)

    def handle_crown_removed(self) -> None:
        """Reduce corruption when crown is removed."""
        self.add_righteousness(5)
