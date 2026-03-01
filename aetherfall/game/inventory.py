"""
Inventory management module.
Handles item pickup and inventory state.
"""

from typing import List, Set, Dict
from utils.config import ITEM_POINTS


class Inventory:
    """
    Manages player inventory and items in the world.
    """

    def __init__(self) -> None:
        """Initialize empty inventory."""
        self.items: List[str] = []
        self.worn_items: Set[str] = set()
        self.blessed_items: Set[str] = set()  # Track blessed items

    def add_item(self, item: str) -> bool:
        """
        Add item to inventory (no duplicates).

        Args:
            item: Item name

        Returns:
            True if item added, False if already owned
        """
        if item not in self.items:
            self.items.append(item)
            return True
        return False

    def has_item(self, item: str) -> bool:
        """
        Check if player has item.

        Args:
            item: Item name

        Returns:
            True if inventory contains item
        """
        return item in self.items

    def remove_item(self, item: str) -> bool:
        """
        Remove item from inventory.

        Args:
            item: Item name

        Returns:
            True if item removed, False if not found
        """
        if item in self.items:
            self.items.remove(item)
            self.worn_items.discard(item)
            self.blessed_items.discard(item)
            return True
        return False

    def get_items(self) -> List[str]:
        """
        Get all items in inventory.

        Returns:
            List of item names
        """
        return self.items.copy()

    def wear_item(self, item: str) -> bool:
        """
        Wear/equip an item.

        Args:
            item: Item name

        Returns:
            True if item worn, False if not in inventory
        """
        if item in self.items:
            self.worn_items.add(item)
            return True
        return False

    def remove_worn_item(self, item: str) -> bool:
        """
        Remove worn item.

        Args:
            item: Item name

        Returns:
            True if item unworn
        """
        if item in self.worn_items:
            self.worn_items.discard(item)
            return True
        return False

    def is_worn(self, item: str) -> bool:
        """
        Check if item is worn.

        Args:
            item: Item name

        Returns:
            True if item is worn
        """
        return item in self.worn_items

    def get_worn_items(self) -> Set[str]:
        """
        Get all worn items.

        Returns:
            Set of worn item names
        """
        return self.worn_items.copy()

    def get_inventory_string(self) -> str:
        """
        Get formatted inventory string.

        Returns:
            Formatted inventory display
        """
        if not self.items:
            return "Your inventory is empty."

        item_list = []
        for item in self.items:
            worn_indicator = " (worn)" if item in self.worn_items else ""
            points = ITEM_POINTS.get(item, 0)
            item_list.append(f"  - {item} (+{points} points){worn_indicator}")

        return "Inventory:\n" + "\n".join(item_list)

    def calculate_total_points(self) -> int:
        """
        Calculate total points from items.

        Returns:
            Sum of all item point values
        """

    def bless_item(self, item: str) -> bool:
        """
        Bless an item (e.g., sword blessing via ritual).

        Args:
            item: Item name to bless

        Returns:
            True if item blessed, False if not in inventory
        """
        if item in self.items and item not in self.blessed_items:
            self.blessed_items.add(item)
            return True
        return False

    def is_item_blessed(self, item: str) -> bool:
        """
        Check if item is blessed.

        Args:
            item: Item name

        Returns:
            True if item is blessed
        """
        return item in self.blessed_items
        return sum(ITEM_POINTS.get(item, 0) for item in self.items)
