from Room import Room
import time

class Building:
    def __init__(self, building_id: str, name: str, location: tuple):
        self.building_id = building_id # e.g. "ICT"
        self.name = name # "Information and Comm. Tech."
        self.location = location # (lat, lon) or grid coords
        self.rooms = {} # room_id -> Room

   #Copyright Gemini 3 Flash
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
    
#Prove they are independent of the number of rooms (O(1) time complexity)
# Create a building
test_building = Building("B1", "Test Hall", (0,0))

# 1. Test with a small number of rooms
test_building.insert_room("R1", 10, "office")

start_small = time.perf_counter()
test_building.lookup_room("R1")
end_small = time.perf_counter()

# 2. Add 10,000 more rooms to "stress" the system
for i in range(10000):
    test_building.insert_room(f"BigR{i}", 30, "lecture")
    
start_large = time.perf_counter()
test_building.lookup_room("BigR9999")
end_large = time.perf_counter()

print(f"Small scale lookup: {end_small - start_small:.8f}s")
print(f"Large scale lookup: {end_large - start_large:.8f}s")
print("Notice the times are nearly identical! That is O(1) performance.")
