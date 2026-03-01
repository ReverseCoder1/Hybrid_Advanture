"""
Main entry point for Aetherfall RPG.
Handles terminal UI with Colorama and game loop coordination.
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

from game.engine import GameEngine


class GameUI:
    """Handles terminal UI and user interaction."""

    def __init__(self) -> None:
        """Initialize game UI and engine."""
        self.player_name: str = ""
        self.engine = GameEngine()

    def print_header(self, text: str) -> None:
        """Print header text with color."""
        print(f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}")

    def print_success(self, text: str) -> None:
        """Print success message."""
        print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

    def print_warning(self, text: str) -> None:
        """Print warning message."""
        print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")

    def print_error(self, text: str) -> None:
        """Print error message."""
        print(f"{Fore.RED}{text}{Style.RESET_ALL}")

    def print_important(self, text: str) -> None:
        """Print important story message."""
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}")

    def print_stats(self, text: str) -> None:
        """Print stats."""
        print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")

    def print_narrative(self, text: str) -> None:
        """Print narrative text."""
        print(f"{Fore.WHITE}{text}{Style.RESET_ALL}")

    def clear_screen(self) -> None:
        """Clear terminal screen."""
        import os

        os.system("cls" if os.name == "nt" else "clear")

    def get_player_name(self) -> str:
        """
        Prompt player for their name.

        Returns:
            Player name as string
        """
        print(f"\n{Fore.CYAN}{Style.BRIGHT}")
        print("═" * 60)
        print("Welcome, adventurer! What is your name?")
        print("═" * 60)
        print(f"{Style.RESET_ALL}")

        while True:
            name_input = input(
                f"{Fore.GREEN}Enter your name: {Style.RESET_ALL}"
            ).strip()

            if not name_input:
                self.print_warning("Please enter a valid name!")
                continue

            if len(name_input) > 20:
                self.print_warning("Name is too long! (Max 20 characters)")
                continue

            return name_input

    def run(self) -> None:
        """Run the main game loop."""
        # Get player name
        self.player_name = self.get_player_name()
        self.engine.world.player_name = self.player_name

        # Show intro
        intro = self.engine.get_game_intro()
        print("\n")
        self.print_important(f"Welcome, {self.player_name}!")
        print()
        self.print_header(intro)

        # Main game loop
        while not self.engine.is_game_over():
            try:
                # Get user input
                prompt = f"\n{Fore.GREEN}>{Style.RESET_ALL} "
                user_input = input(prompt).strip()

                if not user_input:
                    continue

                # Exit command
                if user_input.lower() in ["quit", "exit", "q"]:
                    self.print_warning("\nThanks for playing Aetherfall!")
                    break

                # Try special commands first
                special_result = self.engine.process_special_command(user_input)
                if special_result:
                    self.print_narrative(special_result)
                    continue

                # Process regular input
                output = self.engine.process_input(user_input)

                # Color output based on content
                if "✨" in output or "🏆" in output or "TRUE" in output:
                    self.print_success(output)
                elif "💀" in output or "FALLEN" in output:
                    self.print_error(output)
                elif "⚠️" in output or "damage" in output:
                    self.print_warning(output)
                elif "═══" in output:  # Title sections
                    self.print_important(output)
                else:
                    self.print_narrative(output)

            except KeyboardInterrupt:
                print()
                self.print_warning("Game interrupted by user.")
                break
            except Exception as e:
                self.print_error(f"An error occurred: {str(e)}")
                continue

        # Game end
        if self.engine.is_game_over():
            ending = self.engine.world.get_ending()
            if ending == "True":
                self.print_success("\n🎉 YOU HAVE WON! 🎉")
            elif ending == "Failure":
                self.print_error("\n💀 GAME OVER 💀")

            final_stats = self.engine.world.get_stats()
            self.print_stats(f"\nFinal Stats:\n{final_stats}")


def main() -> None:
    """
    Main function to start the game.
    """
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║                                                        ║")
    print("║          AETHERFALL: THE SHADOW KING                   ║")
    print("║              An AI-Driven Story RPG                    ║")
    print("║                                                        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

    ui = GameUI()
    ui.run()

    # Goodbye message with player name
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print("═" * 60)
    print(f"Thanks for playing, {ui.player_name}!")
    print("Farewell, hero. May the light guide your next adventure!")
    print("═" * 60)
    print(f"{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
