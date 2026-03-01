"""
Configuration module for Aetherfall RPG.
Contains all constants used throughout the game.
"""

from typing import Dict, List

# NLP Configuration
INTENT_CONFIDENCE_THRESHOLD: float = 0.75
INTENTS: List[str] = [
    "move",
    "take",
    "look",
    "inventory",
    "help",
    "talk",
    "attack",
    "use",
]

# Game Configuration - FIXED
START_HP: int = 100
MAX_HP: int = 100
VILLAGE_REST_HEALING: int = 30
HEALING_POTION_HEALING: int = 40

# Combat Configuration - FIXED
DUNGEON_ENTER_DAMAGE: int = 15
DUNGEON_NO_SWORD_DAMAGE: int = 15
KAEL_MIN_HP: int = 60
KAEL_DEFEAT_HP_REQUIREMENT: int = 60  # Minimum HP to defeat Kael
KAEL_HP: int = 100
KAEL_DAMAGE_MIN: int = 8
KAEL_DAMAGE_MAX: int = 18
KING_HP: int = 200
KING_DAMAGE_MIN: int = 10
KING_DAMAGE_MAX: int = 20
KING_BLESSED_BONUS: int = 5
KING_DIRECT_ATTACK_DAMAGE: int = 30  # Punishment for attacking during ritual phase

# Crown Effects - NEW
CROWN_CORRUPTION: int = 10
CROWN_DAMAGE_BONUS: int = 5
CROWN_TRUST_PENALTY: int = 5

# Guard Configuration - FIXED
GUARD_TRUST_MAX: int = 5
GUARD_FULL_TRUST_THRESHOLD: int = 4

# Scoring Configuration
SCORING_MILESTONES: Dict[int, str] = {
    25: "🌟 Rising Adventurer",
    50: "🔥 Hero of the Realm",
    100: "👑 Legendary Explorer",
}

# Directions
VALID_DIRECTIONS: List[str] = ["north", "south", "east", "west", "up", "down"]

# Items and their locations
WORLD_ITEMS: Dict[str, List[str]] = {
    "Enchanted Forest": ["Wood"],
    "Hidden Cave": ["Torch"],
    "Castle Gate": ["Rusty Key"],
    "Royal Courtyard": ["Golden Crown"],
    "Dark Dungeon": ["Sword"],
    "Wizard Tower": ["Magic Amulet"],
}

# Item point values
ITEM_POINTS: Dict[str, int] = {
    "Wood": 5,
    "Torch": 10,
    "Rusty Key": 15,
    "Golden Crown": 25,
    "Sword": 20,
    "Magic Amulet": 30,
}

# Game Locations
CASTLE_GATE: str = "Castle Gate"
ANCIENT_BRIDGE: str = "Ancient Bridge"
MOUNTAIN_PEAK: str = "Mountain Peak"
RIVER: str = "River"
DARK_DUNGEON: str = "Dark Dungeon"
WIZARD_TOWER: str = "Wizard Tower"

# MODEL PATH
MODEL_PATH: str = "nlp/model.pth"
