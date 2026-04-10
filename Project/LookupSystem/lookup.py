import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataStructures.HashTable import HashTable


class CampusLookup:
    """
    Fast lookup system for buildings, rooms, and services by name or ID.
    Wraps a HashTable to provide O(1) average insert, delete, and lookup.

    Buildings are indexed by both their name and their bid (building ID),
    so users can search by either key.
    Rooms are indexed by a composite key: "building_id:floor_id:room_id".
    Services are indexed by service name.
    """

    def __init__(self):
        self.table = HashTable()

    def insert_building(self, building):
        """
        Index a building by both its name and its bid.

        Args:
            building: A Building object with .name and .bid attributes.
        """
        self.table.insert(building.bid, building)
        self.table.insert(building.name, building)

    def delete_building(self, building):
        """
        Remove a building from the lookup by both its name and bid.

        Args:
            building: A Building object with .name and .bid attributes.
        """
        self.table.delete(building.bid)
        self.table.delete(building.name)

    def insert_room(self, building_id, floor_id, room):
        """
        Index a room by a composite key "building_id:floor_id:room_id".

        Args:
            building_id: The building's ID.
            floor_id: The floor's ID.
            room: A Room object with a .id attribute.
        """
        key = f"{building_id}:{floor_id}:{room.id}"
        self.table.insert(key, room)

    def delete_room(self, building_id, floor_id, room_id):
        """
        Remove a room from the lookup.

        Args:
            building_id: The building's ID.
            floor_id: The floor's ID.
            room_id: The room's ID.
        """
        key = f"{building_id}:{floor_id}:{room_id}"
        self.table.delete(key)

    def insert_service(self, service_name, data):
        """
        Index a service by its name.

        Args:
            service_name (str): Name of the service.
            data: The service data to store.
        """
        self.table.insert(service_name, data)

    def delete_service(self, service_name):
        """Remove a service from the lookup."""
        self.table.delete(service_name)

    def lookup(self, key):
        """
        Look up any record (building, room, or service) by key.
        Returns the stored object or None.

        Args:
            key: A building name, building ID, room composite key, or service name.
        """
        return self.table.lookup(key)

    def contains(self, key):
        """Check if a key exists in the lookup."""
        return self.table.contains(key)

    def insert(self, key, value):
        """Generic insert for any key-value pair."""
        self.table.insert(key, value)

    def delete(self, key):
        """Generic delete by key."""
        return self.table.delete(key)
