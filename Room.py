class Room:
    def __init__(self, room_id: str, capacity: int, room_type: str):
        self.room_id = room_id # e.g. "ICT-121"
        self.capacity = capacity # max occupancy
        self.room_type = room_type # "lecture", "lab", "office"
        self.bookings = [] # list of Booking objects
    def __repr__(self):
        return f"------------------------------------\nRoom id = {self.room_id}\ncapacity = {self.capacity}\nroom_type = {self.room_type}\n------------------------------------"

