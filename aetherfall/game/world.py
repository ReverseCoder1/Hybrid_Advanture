"""
World module.
Central game state and logic coordination.
"""

from typing import Tuple, Dict, List, Optional
from game.map_graph import WorldMap, START_LOCATION
from game.inventory import Inventory
from game.health import Health
from game.morality import Morality
from game.scoring import Scoring
from game.guard import Guard
from game.general_kael import GeneralKael
from game.ritual import Ritual
from game.puzzles import Puzzles
from utils.config import (
    WORLD_ITEMS,
    ITEM_POINTS,
    DARK_DUNGEON,
    DUNGEON_NO_SWORD_DAMAGE,
    MOUNTAIN_PEAK,
    KING_DIRECT_ATTACK_DAMAGE,
    VALID_DIRECTIONS,
)


class Gameworld:
    """
    Central game world managing all state and game logic.
    Coordinates between different game systems.
    """

    def __init__(self) -> None:
        """Initialize game world."""
        self.map = WorldMap()
        self.inventory = Inventory()
        self.health = Health()
        self.morality = Morality()
        self.scoring = Scoring()
        self.guard = Guard()
        self.kael = GeneralKael()
        self.ritual = Ritual()
        self.puzzles = Puzzles()

        self.current_location: str = START_LOCATION
        self.world_items: Dict[str, List[str]] = self._init_world_items()
        self.game_over: bool = False
        self.ending: str = "None"  # None, True, Dark, Failure
        self.shadow_king_defeated_by_ritual: bool = False
        self.player_name: str = "Hero"  # Default name, can be set later

        # State tracking flags for preventing exploits
        self.dungeon_penalty_applied: bool = False  # Dungeon damage taken once only
        self.mountain_peak_battle_started: bool = False  # Prevent escape during battle

    def _init_world_items(self) -> Dict[str, List[str]]:
        """Initialize items in the world."""
        items_copy = {}
        for location, items in WORLD_ITEMS.items():
            items_copy[location] = items.copy()
        return items_copy

    def move(self, direction: str) -> str:
        """
        Attempt to move in a direction.

        Args:
            direction: Direction to move (north, south, east, west, up, down)

        Returns:
            Movement result message
        """
        direction = direction.lower()

        if direction not in VALID_DIRECTIONS:
            return f"'{direction}' is not a valid direction. Use: north, south, east, west, up, down"

        if not self.map.can_move(self.current_location, direction):
            return f"You cannot move {direction} from here."

        new_location = self.map.move(self.current_location, direction)
        self.current_location = new_location

        # Check special conditions
        return_msg = f"You move {direction}.\n\n{self.look()}"

        # Check for Kael blocking bridge
        if new_location == "Ancient Bridge" and not self.kael.is_defeated():
            return_msg += f"\n\nGeneral Kael blocks your path: You cannot proceed until you defeat him."

        # Check for dungeon damage (one-time only)
        if new_location == DARK_DUNGEON and not self.inventory.has_item("Sword"):
            if not self.dungeon_penalty_applied:
                self.health.take_damage(DUNGEON_NO_SWORD_DAMAGE)
                self.dungeon_penalty_applied = True
                return_msg += f"\n\n⚠️ The dungeon is treacherous without a weapon! You take {DUNGEON_NO_SWORD_DAMAGE} damage."

        return return_msg

    def look(self) -> str:
        """
        Look around current location.

        Returns:
            Location description and available items
        """
        description = self.map.get_description(self.current_location)

        # Check for items
        items_here = self.world_items.get(self.current_location, [])
        if items_here:
            item_list = ", ".join(items_here)
            description += f"\n\nYou see: {item_list}"

        # Check for NPCs
        if self.current_location == "Castle Gate":
            description += "\n\nCaptain Ardyn stands guard here."
        elif self.current_location == "Ancient Bridge":
            description += "\n\nGeneral Kael stands watch here."
        elif self.current_location == "Mountain Peak":
            description += "\n\nThe Shadow King sits upon a dark throne."

        return description

    def take_item(self, item_name: str) -> str:
        """
        Pick up an item.

        Args:
            item_name: Item name to pick up

        Returns:
            Item pickup message
        """
        items_here = self.world_items.get(self.current_location, [])

        # Case-insensitive search
        matching_item = None
        for item in items_here:
            if item.lower() == item_name.lower():
                matching_item = item
                break

        if not matching_item:
            return f"There is no '{item_name}' here."

        if self.inventory.add_item(matching_item):
            items_here.remove(matching_item)
            points = ITEM_POINTS.get(matching_item, 0)
            self.scoring.add_visible_points(points)
            milestone = self.scoring.check_milestones()
            return f"You picked up {matching_item} (+{points} points).{milestone}"
        else:
            return f"You already have {matching_item}."

    def use_item(self, item_name: str) -> str:
        """
        Use an item.

        Args:
            item_name: Item to use

        Returns:
            Item usage result
        """
        item_name = item_name.lower()

        if item_name in ["bless sword", "bless", "blessed sword"]:
            has_sword = self.inventory.has_item("Sword")
            has_amulet = self.inventory.has_item("Magic Amulet")

            if self.current_location != "River":
                return "The blessing ritual requires the sacred waters of the River."

            return self.ritual.bless_sword(has_sword, has_amulet)

        elif item_name in ["crown", "wear crown", "don crown"]:
            if not self.inventory.has_item("Golden Crown"):
                return "You don't have the Golden Crown."

            if self.inventory.is_worn("Golden Crown"):
                self.inventory.remove_worn_item("Golden Crown")
                self.morality.add_righteousness(5)
                return "You remove the Golden Crown. The corruption fades slightly."
            else:
                self.inventory.wear_item("Golden Crown")
                self.morality.add_corruption(10)
                return "You wear the Golden Crown. Darkness whispers in your mind..."

        elif item_name in ["attack king", "strike king", "attack", "strike"]:
            if self.current_location == MOUNTAIN_PEAK:
                self.health.take_damage(KING_DIRECT_ATTACK_DAMAGE)
                return (
                    f"You attack the Shadow King directly! His counterattack is devastating. "
                    f"You take {KING_DIRECT_ATTACK_DAMAGE} damage!"
                )
            return "The Shadow King is not here."

        return f"You cannot use '{item_name}'."

    def get_stats(self) -> str:
        """
        Get player stats display.

        Returns:
            Formatted stats string
        """
        stats = [
            self.health.get_health_string(),
            self.scoring.get_score_string(),
            f"Alignment: {self.morality.get_alignment()}",
        ]
        return "\n".join(stats)

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.game_over or not self.health.is_alive()

    def get_ending(self) -> str:
        """Get game ending type."""
        return self.ending

    def defeat_final_boss(self) -> str:
        """
        Defeat the Shadow King through ritual.

        Returns:
            Ending message
        """
        if self.current_location != MOUNTAIN_PEAK:
            return "The Shadow King is not here."

        # Check all winning conditions
        has_blessed_sword = self.ritual.is_sword_blessed()
        has_amulet = self.inventory.has_item("Magic Amulet")
        wears_crown = self.inventory.is_worn("Golden Crown")
        has_oath_token = self.inventory.has_item("Oath Token")
        bridge_repaired = self.puzzles.is_bridge_repaired()
        kael_defeated = self.kael.is_defeated()
        guard_trusted = self.guard.is_trusted()
        knows_true_strike = self.guard.has_taught_true_strike

        # Ritual step verification
        ritual_complete = self.ritual.is_ritual_complete()

        if not ritual_complete:
            return "The ritual is not complete. You must follow all steps."

        # Critical failure: Missing Oath Token triggers Dark Ending
        if not has_oath_token:
            self.game_over = True
            self.ending = "Dark"
            return (
                "═══════════════════════════════════════════════════════\n"
                "🌑 THE DARK ENDING 🌑\n"
                "═══════════════════════════════════════════════════════\n\n"
                "The Shadow resists you. You lack the Guard's blessing.\n\n"
                "Without the Oath Token, the ritual falters.\n"
                "The Shadow King's power overwhelms you.\n"
                "Darkness consumes the realm...\n\n"
                "You have not proven yourself worthy.\n"
                "The Shadow King remains eternal.\n\n"
                "💀 THE REALM FALLS INTO ETERNAL SHADOW 💀\n"
                "═══════════════════════════════════════════════════════"
            )

        if wears_crown:
            return "The crown's corruption prevents the ritual. You must remove it."

        if not has_blessed_sword:
            return "The Shadow King cannot be defeated without the Blessed Sword."

        if not guard_trusted:
            return "You have not yet proven yourself. The guard has not blessed your path."

        if not kael_defeated or not bridge_repaired:
            return "The path is not clear. Some trials remain."

        if not knows_true_strike:
            return "The True Strike technique is required to seal the victory."

        # True ending achieved
        self.game_over = True
        self.ending = "True"
        self.shadow_king_defeated_by_ritual = True
        return self._true_ending()

    def _true_ending(self) -> str:
        """Get true ending message."""
        return (
            "═══════════════════════════════════════════════════════\n"
            "✨ THE TRUE ENDING ✨\n"
            "═══════════════════════════════════════════════════════\n\n"
            "You stand before the Shadow King, Blessed Sword raised high.\n"
            "The Oath Token glows with divine light. The Magic Amulet resonates.\n\n"
            "You follow the ritual perfectly:\n"
            "1. The crown lies discarded.\n"
            "2. The amulet shines with ancient power.\n"
            "3. The shadows separate from the king.\n"
            "4. You unleash the TRUE STRIKE!\n\n"
            "The Shadow King shatters, destroyed not by mindless attacks,\n"
            "but by the discipline of the ritual and the power of righteousness.\n\n"
            "The corruption that plagued the realm is PURGED.\n"
            "The ancient darkness is sealed away forever.\n\n"
            "You are hailed as the LEGENDARY HERO OF AETHERFALL!\n\n"
            "🏆 THE REALM IS SAVED 🏆\n"
            "═══════════════════════════════════════════════════════"
        )

    def check_failure(self) -> Tuple[bool, str]:
        """
        Check if player has failed.

        Returns:
            Tuple of (is_failed, message)
        """
        if not self.health.is_alive():
            self.game_over = True
            self.ending = "Failure"
            return (
                True,
                (
                    "═══════════════════════════════════════════════════════\n"
                    "💀 YOU HAVE FALLEN 💀\n"
                    "═══════════════════════════════════════════════════════\n\n"
                    "Your body collapses. The darkness embraces you.\n"
                    "The Shadow King remains, eternal and unchallenged.\n\n"
                    "The realm falls into endless shadow...\n"
                    "═══════════════════════════════════════════════════════"
                ),
            )
        return False, ""
