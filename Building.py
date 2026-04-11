from BookingSystem import BookingManager
from Room import Room
import time

class Building:
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id = building_id # e.g. "ICT"
        self.name = name # "Information and Comm. Tech."
        self.location = location # (lat, lon) or grid coords
        self.rooms = {} # room_id -> Room
        self.booking_manager = BookingManager() # bookings


   # Copyright Gemini 3 Flash
    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def store_room(self, room):
        self.rooms[room.room_id] = room

    def insert_room(self, room_id, room_name, capacity):
        if room_id in self.rooms:
            raise ValueError(f"Room {room_id} already exists in building {self.building_id}")
        room = Room(room_id, capacity, room_type=room_name)
        self.rooms[room_id] = room
        return room
    
    def delete_room(self, room_id):
        if room_id not in self.rooms:
            raise ValueError(f"Room {room_id} does not exist in building {self.building_id}")
        del self.rooms[room_id]

    def lookup_room(self, room_id):
        return self.rooms.get(room_id)
