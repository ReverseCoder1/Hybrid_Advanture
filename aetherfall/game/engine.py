"""
Game engine module.
Coordinates NLP prediction with world state and game logic (FSM).
"""

from typing import Tuple, Optional
from enum import Enum
from nlp.predictor import IntentPredictor
from game.world import Gameworld


class GameState(Enum):
    """Game states for the Finite State Machine."""

    START = "start"
    PLAYING = "playing"
    FINAL_BOSS = "final_boss"
    GAME_OVER = "game_over"


class GameEngine:
    """
    Main game engine implementing FSM and coordinating gameplay.
    Handles intent prediction, world updates, and state transitions.
    """

    def __init__(self) -> None:
        """Initialize game engine."""
        self.predictor = IntentPredictor()
        self.world = Gameworld()
        self.state = GameState.START
        self.turn_count = 0
        self.player_name = "Adventurer"  # Default name

    def set_player_name(self, name: str):
        """
        Set the player's name for personalized responses.
        
        Args:
            name: Player's name
        """
        self.player_name = name if name.strip() else "Adventurer"

    def get_game_intro(self) -> str:
        """
        Get game introduction.

        Returns:
            Intro text
        """
        return (
            "═══════════════════════════════════════════════════════\n"
            "              ⚔️  AETHERFALL: THE SHADOW KING  ⚔️\n"
            "═══════════════════════════════════════════════════════\n\n"
            "Long ago, the Shadow King sought immortality through a forbidden ritual.\n"
            "His corruption spread across the realm, binding the land in eternal darkness.\n\n"
            "Only ONE path leads to true victory.\n"
            "Actions matter more than words.\n"
            "The ritual must be perfect, or darkness will consume all.\n\n"
            "Your journey begins...\n"
            "═══════════════════════════════════════════════════════\n\n"
            f"{self.world.look()}\n\n"
            f"{self.world.get_stats()}\n\n"
            "Type 'help' for commands."
        )

    def process_input(self, user_input: str) -> str:
        """
        Process user input through intent prediction and world logic.

        Args:
            user_input: Raw user input

        Returns:
            Game output/response
        """
        if not user_input.strip():
            return "Please enter a command."

        # Transition to playing state
        if self.state == GameState.START:
            self.state = GameState.PLAYING

        # Predict intent
        intent, confidence = self.predictor.predict(user_input)

        if intent == "unknown":
            return "I don't understand that. Try 'help' for available commands."

        self.turn_count += 1

        # Process intent
        result = self._handle_intent(intent, user_input)

        # Add stats footer
        stats_footer = f"\n\n{self.world.get_stats()}"

        # Check game over conditions
        is_failed, failure_msg = self.world.check_failure()
        if is_failed:
            self.state = GameState.GAME_OVER
            return result + failure_msg

        # Check for final boss location
        if self.world.current_location == "Mountain Peak":
            self.state = GameState.FINAL_BOSS

        return result + stats_footer

    def _handle_intent(self, intent: str, user_input: str) -> str:
        """
        Handle specific intent.

        Args:
            intent: Predicted intent
            user_input: Original user input

        Returns:
            Intent handling result
        """
        intent = intent.lower()

        if intent == "move":
            return self._handle_move(user_input)
        elif intent == "take":
            return self._handle_take(user_input)
        elif intent == "look":
            return self._handle_look()
        elif intent == "inventory":
            return self._handle_inventory()
        elif intent == "help":
            return self._handle_help()
        elif intent == "talk":
            return self._handle_talk(user_input)
        elif intent == "attack":
            return self._handle_attack(user_input)
        elif intent == "use":
            return self._handle_use(user_input)
        else:
            return "Unknown intent."

    def _handle_move(self, user_input: str) -> str:
        """Handle movement intent."""
        directions = ["north", "south", "east", "west", "up", "down"]
        direction = None

        for d in directions:
            if d in user_input.lower():
                direction = d
                break

        if not direction:
            return "Which direction? (north, south, east, west, up, down)"

        return self.world.move(direction)

    def _handle_take(self, user_input: str) -> str:
        """Handle take/pick up intent."""
        words = user_input.lower().split()

        # Find item name (everything after "take" or "pick")
        if "take" in words:
            idx = words.index("take")
            if idx + 1 < len(words):
                item_name = " ".join(words[idx + 1 :])
                return self.world.take_item(item_name)

        if "pick" in words:
            idx = words.index("pick")
            if idx + 2 < len(words) and words[idx + 1] == "up":
                item_name = " ".join(words[idx + 2 :])
                return self.world.take_item(item_name)

        return "Take what? Specify an item name."

    def _handle_look(self) -> str:
        """Handle look intent."""
        return self.world.look()

    def _handle_inventory(self) -> str:
        """Handle inventory intent."""
        return self.world.inventory.get_inventory_string()

    def _handle_help(self) -> str:
        """Handle help intent."""
        return (
            "AVAILABLE COMMANDS:\n"
            "  move [direction]  - Move north, south, east, west, up, or down\n"
            "  look              - Look at current location\n"
            "  take [item]       - Pick up an item\n"
            "  inventory         - Check your inventory\n"
            "  talk              - Talk to an NPC\n"
            "  use [item]        - Use an item or ability\n"
            "  attack [target]   - Attack an enemy\n"
            "  help              - Show this message\n\n"
            "EXAMPLES:\n"
            "  move north        - Travel north\n"
            "  take sword        - Pick up sword\n"
            "  talk guard        - Talk to an NPC\n"
            "  bless sword       - Perform ritual at River\n"
            "  attack king       - Attack the Shadow King"
        )

    def _handle_talk(self, user_input: str) -> str:
        """Handle talk intent."""
        location = self.world.current_location

        if location == "Castle Gate":
            return self.world.guard.talk_to_guard()
        elif location == "Ancient Bridge":
            return "General Kael: 'Why do you disturb me?'"
        elif location == "Mountain Peak":
            return (
                "The Shadow King: 'You dare stand before me? "
                "Only a proper ritual can end this.'"
            )
        else:
            return "There's no one to talk to here."

    def _handle_attack(self, user_input: str) -> str:
        """Handle attack intent."""
        location = self.world.current_location

        if location == "Mountain Peak":
            # Try to trigger final boss defeat
            return self.world.defeat_final_boss()
        elif location == "Ancient Bridge":
            # Try to defeat Kael - simplified to just Sword + HP check
            has_sword = self.world.inventory.has_item("Sword")
            hp = self.world.health.get_hp()

            return self.world.kael.challenge_kael(has_sword, hp)
        else:
            return "There's nothing to attack here."

    def _handle_use(self, user_input: str) -> str:
        """Handle use intent."""
        # Extract the item/action to use
        words = user_input.lower().split()

        if "use" in words:
            idx = words.index("use")
            if idx + 1 < len(words):
                item_name = " ".join(words[idx + 1 :])
                return self.world.use_item(item_name)

        # Check for special phrases
        if "bless" in user_input.lower():
            return self.world.use_item("bless sword")
        if "ritual" in user_input.lower():
            return self._handle_ritual()

        return "Use what? Specify an action or item."

    def _handle_ritual(self) -> str:
        """Handle ritual commands."""
        location = self.world.current_location

        if location == "Mountain Peak":
            return self.world.ritual.start_final_ritual()

        return "No ritual available here."

    def is_game_over(self) -> bool:
        """Check if game is over."""
        return self.state == GameState.GAME_OVER

    def process_special_command(self, command: str) -> Optional[str]:
        """
        Process special game commands for advanced interactions.

        Args:
            command: Special command

        Returns:
            Command result if special, None otherwise
        """
        cmd = command.lower().strip()
        location = self.world.current_location

        # Guard interactions
        if (
            cmd in ["oath token", "give oath", "receive oath"]
            and location == "Castle Gate"
        ):
            result = self.world.guard.give_oath_token()
            if (
                "already given" not in result
                and result != self.world.guard.talk_to_guard()
            ):
                self.world.inventory.add_item("Oath Token")
                self.world.scoring.add_secret_points(
                    self.world.guard.GUARD_SECRET_POINTS
                )
            return result

        if (
            cmd in ["true strike", "teach strike", "learn strike"]
            and location == "Castle Gate"
        ):
            result = self.world.guard.teach_true_strike()
            if "already know" not in result and "not for" not in result:
                self.world.guard.has_taught_true_strike = True
            return result

        # Ritual commands
        if cmd in ["remove crown", "take off crown"] and location == "Mountain Peak":
            if self.world.inventory.is_worn("Golden Crown"):
                self.world.inventory.remove_worn_item("Golden Crown")
                self.world.ritual.ritual_remove_crown(False)
                return "You remove the Golden Crown. The ritual advances."
            return "You are not wearing the crown."

        if cmd in ["activate amulet", "use amulet"] and location == "Mountain Peak":
            if self.world.ritual.ritual_activate_amulet(
                self.world.inventory.has_item("Magic Amulet")
            ):
                return "The Magic Amulet activates with brilliant light. The ritual advances."
            return "You cannot activate the amulet."

        if cmd in ["wait", "prepare", "shadow"] and location == "Mountain Peak":
            if self.world.ritual.ritual_wait():
                return (
                    "You wait as the shadows separate from the king. "
                    "The moment of truth approaches..."
                )
            return "The time is not right."

        if (
            cmd in ["true strike", "final strike", "ultimate attack"]
            and location == "Mountain Peak"
        ):
            if self.world.ritual.ritual_true_strike(
                self.world.ritual.is_sword_blessed(),
                self.world.guard.has_taught_true_strike,
            ):
                return self.world.defeat_final_boss()
            return "You cannot perform the True Strike."

        # Puzzle interactions
        if cmd in ["solve riddle", "answer riddle"] and location == "Wizard Tower":
            return self.world.puzzles.solve_wizard_riddle()

        if cmd in ["repair bridge", "fix bridge"] and location == "Ancient Bridge":
            return self.world.puzzles.repair_bridge()

        if cmd in ["return food", "give food"] and location == "Village":
            return self.world.puzzles.return_food_to_village()

        if cmd in ["donate", "donate points"] and location == "Castle Gate":
            points = self.world.scoring.get_visible_score()
            if points >= 10:
                self.world.scoring.add_visible_points(-10)
                return self.world.puzzles.donate_to_cause(10)
            return "You don't have enough points."

        return None
