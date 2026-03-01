"""
Ritual and blessing system module.
Handles sword blessing and final boss ritual.
"""

from utils.config import RIVER


class Ritual:
    """
    Manages blessing rituals at River and final boss defeat ritual.
    """

    def __init__(self) -> None:
        """Initialize ritual system."""
        self.sword_blessed: bool = False
        self.ritual_stage: int = (
            0  # 0: none, 1: remove crown, 2: activate amulet, 3: wait, 4: true strike
        )

    def bless_sword(self, has_sword: bool, has_amulet: bool) -> str:
        """
        Attempt to bless sword at River.
        Requires both Sword and Magic Amulet.

        Args:
            has_sword: Player has Sword
            has_amulet: Player has Magic Amulet

        Returns:
            Ritual result message
        """
        if self.sword_blessed:
            return "The sword is already blessed. Its power remains eternal."

        if not has_sword:
            return "You have no sword to bless."

        if not has_amulet:
            return (
                "The blessing requires the presence of both steel and magic. "
                "You lack the Magic Amulet."
            )

        self.sword_blessed = True
        return (
            "The waters glow as you hold your sword before them. "
            "The Amulet resonates with power. The sword is now BLESSED! "
            "Its edge shines with divine light."
        )

    def is_sword_blessed(self) -> bool:
        """
        Check if sword is blessed.

        Returns:
            True if sword blessed
        """
        return self.sword_blessed

    def start_final_ritual(self) -> str:
        """
        Begin the final boss ritual.
        Must follow specific steps to succeed.

        Returns:
            First step instruction
        """
        self.ritual_stage = 1
        return (
            "The Shadow King awaits. The ritual begins.\n"
            "Step 1: Remove the corrupted crown from your possession."
        )

    def ritual_remove_crown(self, wearing_crown: bool) -> bool:
        """
        Execute ritual step 1: Remove crown.

        Args:
            wearing_crown: Player is currently wearing crown

        Returns:
            True if step successful
        """
        if wearing_crown:
            return False
        self.ritual_stage = 2
        return True

    def ritual_activate_amulet(self, has_amulet: bool) -> bool:
        """
        Execute ritual step 2: Activate Amulet.

        Args:
            has_amulet: Player has Magic Amulet

        Returns:
            True if step successful
        """
        if not has_amulet:
            return False
        self.ritual_stage = 3
        return True

    def ritual_wait(self) -> bool:
        """
        Execute ritual step 3: Wait for shadow separation.

        Returns:
            True if successful
        """
        self.ritual_stage = 4
        return True

    def ritual_true_strike(
        self, has_blessed_sword: bool, knows_true_strike: bool
    ) -> bool:
        """
        Execute ritual step 4: True Strike.

        Args:
            has_blessed_sword: Player has Blessed Sword
            knows_true_strike: Player learned True Strike from guard

        Returns:
            True if ritual complete and successful
        """
        if not has_blessed_sword or not knows_true_strike:
            return False
        return True

    def is_ritual_complete(self) -> bool:
        """
        Check if ritual has reached completion stage.

        Returns:
            True if ritual stage >= 4
        """
        return self.ritual_stage >= 4

    def check_oath_token(self, has_oath_token: bool) -> bool:
        """
        Check if player has required Oath Token for ritual.

        Args:
            has_oath_token: Player has Oath Token

        Returns:
            True if token present
        """
        return has_oath_token

    def get_ritual_status(self) -> str:
        """
        Get current ritual status.

        Returns:
            Status message
        """
        stages = [
            "Ritual not started",
            "Step 1: Crown removed",
            "Step 2: Amulet activated",
            "Step 3: Shadows separate",
            "Step 4: True Strike ready",
        ]
        return stages[min(self.ritual_stage, 4)]
