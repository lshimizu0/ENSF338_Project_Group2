from datetime import datetime
import re

class Booking:
    def __init__(self, room_id: str, event_name: str,
                 date: str, start_time: str, end_time: str, organizer: str, booking_id = None):
        """
        booking_id  : unique identifier, e.g. "BK001"
        room_id     : e.g. "E101"
        event_name  : human-readable label
        date        : "YYYY-MM-DD"
        start_time  : "HH:MM"  (24-hour)
        end_time    : "HH:MM"
        organizer   : name / ID of the person who made the booking
        """
        self.booking_id = booking_id
        self.room_id = room_id
        self.event_name = event_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.organizer = organizer

        # Bundled date and time for BST ordering
        self.date_time = (date, start_time)

    def __repr__(self):
        return (f"-------------------------------\nBooking id = {self.booking_id}\nRoom id = {self.room_id},\nEvent name = {self.event_name}\nDate = {self.date}\nTime Range = {self.start_time}-{self.end_time}\n-------------------------------")


class Node:
    def __init__(self, booking: Booking):
        self.booking = booking
        self.data_time = booking.date_time
        self.left = None
        self.right = None


class BookingBST:
    def __init__(self):
        self.root = None
        self.booking_number = 0

    def insert(self, booking: Booking):
        self.root = self.insertHelper(self.root, booking)
        self.booking_number += 1

    def overlap_booking(self, root, booking):
        if root is None:
            return False
        if self.overlap_booking(root.left, booking):
            return True
        if (root.booking.room_id == booking.room_id
                and root.booking.date == booking.date
                and root.booking.start_time < booking.end_time
                and booking.start_time < root.booking.end_time):
            return True
        return self.overlap_booking(root.right, booking)


    def insertHelper(self, node: Node, booking: Booking):
        if node is None:
            return Node(booking)
        elif booking.date_time < node.data_time:
            node.left = self.insertHelper(node.left, booking)
        elif booking.date_time > node.data_time:
            node.right = self.insertHelper(node.right, booking)
        elif booking.date_time == node.data_time:
            node.right = self.insertHelper(node.right, booking)

        return node


    def remove(self, booking_id: str):
        """returns a boolean"""
        self.root, removed = self.removeHelper(self.root, booking_id)
        if removed:
            self.booking_number -= 1
        
        return removed

    def removeHelper(self, node: Node, booking_id: str):
        if node is None:
            return node, False
        removed = False

        if booking_id == node.booking.booking_id:
            removed = True

            if node.left is None:
                return node.right, removed
            
            if node.right is None:
                return node.left, removed
            
            # Two children: replace with in-order successor
            successor = self.find_min_node(node.right)
            node.booking = successor.booking
            node.data_time = successor.date_time
            node.right, _ = self.removeHelper(node.right, successor.booking.booking_id)
        
        else:
            node.left, removed = self.removeHelper(node.left, booking_id)
            
            if not removed:
                node.right, removed = self.removeHelper(node.right, booking_id)

        return node, removed

    def find_min_node(self, node: Node):
        while node.left is not None:
            node = node.left

        return node

    # Search by booking_id
    def find_by_id(self, booking_id: str):
        results = []
        self._inorder(self.root, results)
        for b in results:
            if b.booking_id == booking_id:
                return b
        return None

    # Range query
    def queryRange(self, date: str, start_time: str, end_time: str):
        low = (date, start_time)
        high = (date, end_time)
        results = []
        self.queryRangeHelper(self.root, low, high, results)
        return results

    def queryRangeHelper(self, node: Node, low: tuple, high: tuple, results: list):
        if node is None:
            return
        
        if node.data_time >= low:
            self.queryRangeHelper(node.left, low, high, results)

        if low <= node.data_time <= high:
            results.append(node.booking)

        if node.data_time <= high:
            self.queryRangeHelper(node.right, low, high, results)

    # Query by date
    def query_by_date(self, date: str):
        return self.queryRange(date, "00:00", "23:59")

    # Next upcoming event
    def next_upcoming(self):
        now_key = (
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M")
        )
        return self._find_next(self.root, now_key, None)

    def _find_next(self, node: Node, now_key: tuple, best: Booking):
        if node is None:
            return best
        
        if node.data_time >= now_key:
            best = node.booking
            return self._find_next(node.left, now_key, best)
        
        return self._find_next(node.right, now_key, best)

    def get_all_sorted(self):
        results = []
        self._inorder(self.root, results)
        return results

    def _inorder(self, node: Node, results: list):
        if node is None:
            return
        
        self._inorder(node.left, results)
        results.append(node.booking)
        self._inorder(node.right, results)


# BookingManager
class BookingManager:

    def __init__(self):
        self.bst = BookingBST()
        self._id_map: dict[str, Booking] = {}
        self.next_booking_id = "1"

    # Asked chat: I want a user to input str: 'HH:MM' and a function that checks if its in that format. If it is in the format 'H:MM' i want it to convert it to 'HH:MM'
    def normalize_time(self, time_str):
        # Match H:MM or HH:MM (hours 0–23, minutes 00–59)
        pattern = r'^(\d{1,2}):([0-5]\d)$'
        match = re.match(pattern, time_str)

        if not match:
            return None  # Invalid format

        hours, minutes = match.groups()

        # Convert hour to integer and back to 2 digits
        hours = int(hours)

        if hours > 23:
            return None  # Invalid hour range

        return f"{hours:02d}:{minutes}"

    # asked chat: now the same with YYYY-MM-DD and do the same with month and day for YYYY-M-D
    def normalize_date(self, date_str):
        # Match YYYY-M-D, YYYY-MM-D, YYYY-M-DD, YYYY-MM-DD
        pattern = r'^(\d{4})-(\d{1,2})-(\d{1,2})$'
        match = re.match(pattern, date_str)

        if not match:
            return None  # Invalid format

        year, month, day = match.groups()

        year = int(year)
        month = int(month)
        day = int(day)

        # Basic validation
        if not (1 <= month <= 12):
            return None
        if not (1 <= day <= 31):
            return None

        # Optional: stricter validation (e.g., Feb, leap years)
        try:
            from datetime import datetime
            datetime(year, month, day)
        except ValueError:
            return None

        return f"{year:04d}-{month:02d}-{day:02d}"
    def add_booking(self, booking: Booking, room=None):
        # check if booking is valid
        time_check = self.normalize_time(booking.start_time)
        if not time_check:
            print("Invalid start time")
            return False
        else:
            booking.start_time = time_check
        time_check = self.normalize_time(booking.end_time)
        if not time_check:
            print("Invalid end time")
            return False
        else:
            booking.end_time = time_check

        date_check = self.normalize_date(booking.date)
        if not date_check:
            print("Invalid date")
            return False
        else:
            booking.date = date_check
        booking.date_time = (booking.date, booking.start_time)
        # check if booking time overlaps with other
        if self.bst.overlap_booking(self.bst.root, booking):
            print(f"Error. Booking time overlaps with other booking")
            if room is not None:
                print(f"Bookings for {booking.date}:")
                for slot in room.bookings:
                    if slot.date == booking.date:
                        print(slot)
            return False



        booking.booking_id = self.next_booking_id
        self.next_booking_id = int(self.next_booking_id) + 1
        self.next_booking_id = str(self.next_booking_id)
        self.bst.insert(booking)
        self._id_map[booking.booking_id] = booking

        if room is not None:
            room.bookings.append(booking)

        print(f"Booking complete:\n {booking}")
        return True

    def remove_booking(self, booking_id: str, room=None):
        if booking_id not in self._id_map:
            print(f"ERROR. Booking ID '{booking_id}' not found.")
            return False

        booking = self._id_map.pop(booking_id)
        self.bst.remove(booking_id)

        if room is not None and booking in room.bookings:
            room.bookings.pop(booking)

        print(f"REMOVED. Removed booking {booking_id}")
        
        return True

    def get_booking(self, booking_id: str):
        booking = self._id_map.get(booking_id)
        
        if booking:
            print(f"GET {booking}")
        
        else:
            print(f"No booking found for ID '{booking_id}'")
        
        return booking

    def queryRange(self, date: str, start_time: str, end_time: str):
        results = self.bst.queryRange(date, start_time, end_time)
        print(f"\nBookings on {date} from {start_time} to {end_time}:")
        
        if not results:
            print("  (none)")
        
        for b in results:
            print(f"  {b}")
        
        return results

    def query_by_date(self, date: str):
        results = self.bst.query_by_date(date)
        print(f"\nAll bookings on {date}:")
        
        if not results:
            print("  (none)")
        
        for b in results:
            print(f"  {b}")
        
        return results

    def next_upcoming(self):
        booking = self.bst.next_upcoming()
        print(f"\n {booking if booking else 'No upcoming bookings'}")
        
        return booking

    def get_all_sorted(self):
        return self.bst.get_all_sorted()

    def print_all(self):
        print("\nALL BOOKINGS - sorted by date/time")
        bookings = self.get_all_sorted()
        
        if not bookings:
            print("  (none)")
        
        for b in bookings:
            print(f"{b}")