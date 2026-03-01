"""
World map module.
Defines the graph-based map for Aetherfall.
"""

from typing import Dict, List, Optional


# World map structure - directed graph
MAP: Dict[str, Dict[str, str]] = {
    "Enchanted Forest": {"north": "Village", "east": "Hidden Cave"},
    "Hidden Cave": {"west": "Enchanted Forest", "north": "Castle Gate"},
    "Castle Gate": {"south": "Hidden Cave", "north": "Royal Courtyard"},
    "Royal Courtyard": {"south": "Castle Gate", "east": "Wizard Tower"},
    "Wizard Tower": {"west": "Royal Courtyard", "down": "Dark Dungeon"},
    "Dark Dungeon": {"up": "Wizard Tower"},
    "Village": {"south": "Enchanted Forest", "east": "River"},
    "River": {"west": "Village", "north": "Ancient Bridge"},
    "Ancient Bridge": {"south": "River", "north": "Mountain Peak"},
    "Mountain Peak": {"south": "Ancient Bridge"},
}

# Starting location
START_LOCATION: str = "Enchanted Forest"


class WorldMap:
    """
    Manages the game world map.
    Provides navigation and location queries.
    """

    def __init__(self) -> None:
        """Initialize the world map."""
        self.map = MAP

    def get_neighbors(self, location: str) -> Dict[str, str]:
        """
        Get all connected locations from current location.

        Args:
            location: Current location name

        Returns:
            Dictionary of direction -> destination
        """
        return self.map.get(location, {})

    def can_move(self, location: str, direction: str) -> bool:
        """
        Check if movement is possible in given direction.

        Args:
            location: Current location
            direction: Direction to move

        Returns:
            True if movement is possible
        """
        neighbors = self.get_neighbors(location)
        return direction.lower() in neighbors

    def move(self, location: str, direction: str) -> Optional[str]:
        """
        Move to adjacent location if possible.

        Args:
            location: Current location
            direction: Direction to move

        Returns:
            New location if successful, None otherwise
        """
        neighbors = self.get_neighbors(location)
        destination = neighbors.get(direction.lower())
        return destination

    def get_description(self, location: str) -> str:
        """
        Get description of a location.

        Args:
            location: Location name

        Returns:
            Location description
        """
        descriptions = {
            "Enchanted Forest": "A mystical forest filled with ancient trees and glowing fungi. The air shimmers with magic.",
            "Hidden Cave": "A dimly lit cave with echoing sounds. Stalactites hang from the ceiling. Something valuable might be hidden here.",
            "Castle Gate": "The imposing gates of the castle. A stern guard stands here, watching all who pass. Ancient stone walls tower above.",
            "Royal Courtyard": "A grand courtyard with marble fountains and statues. The castle looms in the distance.",
            "Wizard Tower": "A tall, spiraling tower crackling with magical energy. Arcane runes cover the walls.",
            "Dark Dungeon": "A foreboding dungeon shrouded in shadow. The air is cold and oppressive. Strange whispers echo.",
            "Village": "A peaceful village with cottages and a marketplace. Villagers go about their daily lives.",
            "River": "A flowing river with crystalline waters. The current is gentle here. Reeds line the banks.",
            "Ancient Bridge": "A magnificent ancient bridge spanning the river. The structure is supported by mystical pillars. General Kael stands guard here.",
            "Mountain Peak": "The highest peak in the realm, shrouded in mist. The Shadow King's presence hangs heavy. A dark throne sits atop.",
        }
        return descriptions.get(location, "You are in an unknown place.")

    def is_valid_location(self, location: str) -> bool:
        """
        Check if location exists in map.

        Args:
            location: Location name

        Returns:
            True if location is valid
        """
        return location in self.map
