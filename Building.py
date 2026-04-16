from Room import Room

class Building:
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id = building_id
        self.name = name
        self.location = location
        self.rooms = {}

    def insert_room(self, room_id, capacity, room_type):
        if room_id in self.rooms:
            raise ValueError(f"Room {room_id} already exists in building {self.building_id}")
        room = Room(room_id, capacity, room_type)
        self.rooms[room_id] = room
        return room

    def delete_room(self, room_id):
        if room_id not in self.rooms:
            raise ValueError(f"Room {room_id} does not exist in building {self.building_id}")
        del self.rooms[room_id]

    def lookup_room(self, room_id):
        return self.rooms.get(room_id)

    def get_room_ids(self):
        return list(self.rooms.keys())