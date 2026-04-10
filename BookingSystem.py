from datetime import datetime

class Booking:
    def __init__(self, booking_id: str, room_id: str, event_name: str,
                 date: str, start_time: str, end_time: str, organizer: str):
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
        return (f"Booking id = {self.booking_id}, Room id = {self.room_id},\
                Event name = {self.event_name}, Date = {self.date}, \
                Time Range = {self.start_time}-{self.end_time})")


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

    def insertHelper(self, node: Node, booking: Booking):
        if node is None:
            return Node(booking)
        
        elif booking.date_time < node.data_time:
            node.left = self.insertHelper(node.left, booking)

        elif booking.date_time > node.data_time:
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

    def add_booking(self, booking: Booking, room=None):
        if booking.booking_id in self._id_map:
            print(f"ERROR. Booking ID '{booking.booking_id}' already exists.")
            return False

        self.bst.insert(booking)
        self._id_map[booking.booking_id] = booking

        if room is not None:
            room.bookings.append(booking)

        print(f"ADD {booking}")
        return True

    def remove_booking(self, booking_id: str, room=None):
        if booking_id not in self._id_map:
            print(f"ERROR. Booking ID '{booking_id}' not found.")
            return False

        booking = self._id_map.pop(booking_id)
        self.bst.remove(booking_id)

        if room is not None and booking in room.bookings:
            room.bookings.remove(booking)

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
            print(f"  {b}")