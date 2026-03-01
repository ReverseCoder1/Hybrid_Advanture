"""
Health management module.
Tracks player HP, damage, healing, and health state.
Fixed: Proper healing system with warnings.
"""

from utils.config import START_HP, MAX_HP


class Health:
    """
    Manages player health points with healing and warnings.
    HP is capped at MAX_HP (100).
    Healing can come from: Village rest or Healing Potion.
    """

    def __init__(self) -> None:
        """Initialize health to starting HP."""
        self.max_hp: int = MAX_HP
        self.current_hp: int = START_HP
        self.has_village_rested: bool = False
        self.last_combat_turn: int = 0

    def take_damage(self, damage: int) -> bool:
        """
        Apply damage to player.

        Args:
            damage: Amount of damage

        Returns:
            True if still alive, False if dead
        """
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        return self.current_hp > 0

    def heal(self, amount: int) -> None:
        """
        Heal player to MAX_HP cap.

        Args:
            amount: Amount to heal
        """
        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def rest_in_village(self) -> str:
        """
        Rest in village to recover 30 HP (once per game, only if HP < 100).

        Returns:
            Rest result message
        """
        if self.has_village_rested:
            return "You have already rested here. The villagers suggest you move on."

        if self.current_hp >= self.max_hp:
            return "You are already at full strength. Rest is unnecessary."

        healing_amount = min(30, self.max_hp - self.current_hp)
        self.heal(healing_amount)
        self.has_village_rested = True
        return f"You rest at the village inn. Restored {healing_amount} HP. Current HP: {self.current_hp}/{self.max_hp}"

    def reset_village_rest(self) -> None:
        """Reset village rest (called when leaving village)."""
        self.has_village_rested = False

    def is_alive(self) -> bool:
        """
        Check if player is alive.

        Returns:
            True if HP > 0
        """
        return self.current_hp > 0

    def get_hp(self) -> int:
        """
        Get current HP.

        Returns:
            Current health points
        """
        return self.current_hp

    def get_max_hp(self) -> int:
        """
        Get maximum HP.

        Returns:
            Maximum health points
        """
        return self.max_hp

    def get_health_percentage(self) -> int:
        """
        Get HP as percentage of max.

        Returns:
            Health percentage (0-100)
        """
        return int((self.current_hp / self.max_hp) * 100)

    def is_low_health(self) -> bool:
        """
        Check if health is dangerously low.

        Returns:
            True if HP < 40
        """
        return self.current_hp < 40

    def is_critical_health(self) -> bool:
        """
        Check if health is critically low.

        Returns:
            True if HP < 20
        """
        return self.current_hp < 20

    def get_health_warning(self) -> str:
        """
        Get warning if health is low.

        Returns:
            Warning message or empty string
        """
        if self.is_critical_health():
            return f"⚠️ CRITICAL: Your health is {self.current_hp} HP! You may not survive the next battle!"
        elif self.is_low_health():
            return f"⚠️ WARNING: Your health is low ({self.current_hp} HP). Consider resting before fighting."
        return ""

    def get_health_string(self) -> str:
        """
        Get formatted health string.

        Returns:
            Health display string
        """
        percentage = self.get_health_percentage()
        bar_length = 20
        filled = int(bar_length * self.current_hp / self.max_hp)
        bar = "█" * filled + "░" * (bar_length - filled)
        return f"HP: {self.current_hp}/{self.max_hp} [{bar}] {percentage}%"
