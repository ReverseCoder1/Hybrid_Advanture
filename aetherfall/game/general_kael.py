"""
General Kael module.
Loyal warrior guarding the Ancient Bridge.
Turn-based combat with realistic damage.
"""

import random
from utils.config import (
    ANCIENT_BRIDGE,
    KAEL_DEFEAT_HP_REQUIREMENT,
    KAEL_HP,
    KAEL_DAMAGE_MIN,
    KAEL_DAMAGE_MAX,
)


class GeneralKael:
    """
    Manages General Kael encounter at Ancient Bridge.
    Turn-based combat system with damage dealt each turn.
    """

    def __init__(self) -> None:
        """Initialize General Kael."""
        self.location: str = ANCIENT_BRIDGE
        self.defeated: bool = False
        self.hp: int = KAEL_HP
        self.in_combat: bool = False

    def is_defeated(self) -> bool:
        """
        Check if Kael has been defeated.

        Returns:
            True if defeated
        """
        return self.defeated

    def can_defeat(
        self,
        has_sword: bool,
        current_hp: int,
    ) -> bool:
        """
        Check if player meets requirements to defeat Kael.

        Args:
            has_sword: Player has Sword
            current_hp: Player's current HP

        Returns:
            True if all requirements met
        """
        return has_sword and current_hp >= KAEL_DEFEAT_HP_REQUIREMENT

    def challenge_kael(
        self,
        has_sword: bool,
        current_hp: int,
        is_blessed_sword: bool = False,
    ) -> str:
        """
        Challenge General Kael (initiates combat).

        Args:
            has_sword: Player has Sword
            current_hp: Player's current HP
            is_blessed_sword: Sword is blessed (bonus damage)

        Returns:
            Combat start result
        """
        if self.defeated:
            return "General Kael: Already defeated, the bridge is clear."

        if not self.can_defeat(has_sword, current_hp):
            missing = []
            if not has_sword:
                missing.append("Sword")
            if current_hp < KAEL_DEFEAT_HP_REQUIREMENT:
                missing.append(f"enough HP ({current_hp}/{KAEL_DEFEAT_HP_REQUIREMENT})")

            return (
                f"General Kael: 'You are not ready! You lack: {', '.join(missing)}. "
                "You cannot pass!'"
            )

        # Start combat
        self.in_combat = True
        self.hp = KAEL_HP
        return self._combat_round(current_hp, is_blessed_sword)

    def _combat_round(self, player_hp: int, is_blessed_sword: bool) -> str:
        """
        Execute one round of combat.

        Args:
            player_hp: Player's current HP
            is_blessed_sword: Sword is blessed

        Returns:
            Combat round result
        """
        # Player attacks
        if is_blessed_sword:
            player_damage = random.randint(15, 25)  # Blessed sword bonus
        else:
            player_damage = random.randint(10, 15)

        self.hp -= player_damage

        # Check if Kael defeated
        if self.hp <= 0:
            self.defeated = True
            self.in_combat = False
            return (
                f"You strike with your sword, dealing {player_damage} damage!\n"
                f"General Kael falls to {player_damage} damage total.\n\n"
                "General Kael: 'You have proven yourself worthy. I yield the bridge. "
                "Go forward, hero. Your destiny awaits.'"
            )

        # Kael counter-attacks
        kael_damage = random.randint(KAEL_DAMAGE_MIN, KAEL_DAMAGE_MAX)
        player_hp -= kael_damage

        return (
            f"You attack Kael dealing {player_damage} damage! (Kael HP: {max(0, self.hp)}/100)\n"
            f"General Kael counterattacks dealing {kael_damage} damage!\n"
            f"Your HP: {max(0, player_hp)}/100\n\n"
            f"(Continue attacking to defeat him)"
        )

    def continue_combat(self, player_hp: int, is_blessed_sword: bool) -> tuple:
        """
        Continue combat with Kael.

        Args:
            player_hp: Player's current HP
            is_blessed_sword: Sword is blessed

        Returns:
            Tuple of (result_message, remaining_kael_hp, damage_to_player)
        """
        if not self.in_combat or self.defeated:
            return ("Kael is not in combat.", self.hp, 0)

        # Player attacks
        if is_blessed_sword:
            player_damage = random.randint(15, 25)
        else:
            player_damage = random.randint(10, 15)

        self.hp -= player_damage

        # Check if Kael defeated
        if self.hp <= 0:
            self.defeated = True
            self.in_combat = False
            return (
                f"You strike with your sword, dealing {player_damage} damage!\n"
                "General Kael falls!\n\n"
                "General Kael: 'You have proven yourself worthy. I yield the bridge.'",
                0,
                0,
            )

        # Kael counter-attacks
        kael_damage = random.randint(KAEL_DAMAGE_MIN, KAEL_DAMAGE_MAX)

        return (
            f"You deal {player_damage} damage! (Kael HP: {self.hp}/100)\n"
            f"Kael counterattacks for {kael_damage} damage!",
            self.hp,
            kael_damage,
        )

    def get_guard_message(self) -> str:
        """
        Get message when trying to pass Kael's bridge.

        Returns:
            Guard message
        """
        if self.defeated:
            return "The bridge is clear. General Kael has fallen."
        return "General Kael stands before you, blocking the path northward."
