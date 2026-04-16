from BookingSystem import *

import pytest

def test_add_booking():
    manager = BookingManager()

    booking = Booking("E101", "Lecture", "2026-04-15", "09:00", "10:00", "Prof")

    result = manager.add_booking(booking)

    assert result == True
    assert booking.booking_id == "1"

def test_add_two_bookings():
    manager = BookingManager()

    booking = Booking("E101", "Lecture", "2026-04-15", "09:00", "10:00", "Prof")
    booking2 = Booking("E202", "Lecture", "2026-04-15", "16:00", "18:00", "Prof")
    result1 = manager.add_booking(booking)
    result2 = manager.add_booking(booking2)

    assert result1 == True
    assert booking.booking_id == "1"

    assert booking2.booking_id == "2"
    assert result2 == True

def test_remove_booking():
    manager = BookingManager()

    booking = Booking("E101", "Lecture", "2026-04-15", "09:00", "10:00", "Prof")
    manager.add_booking(booking)

    result = manager.remove_booking("1")

    assert result == True
    assert manager.get_booking("1") is None

def test_overlap():
    manager = BookingManager()

    b1 = Booking("E101", "A", "2026-04-15", "09:00", "10:00", "Prof")
    b2 = Booking("E101", "B", "2026-04-15", "09:30", "10:30", "Prof")

    assert manager.add_booking(b1) == True
    assert manager.add_booking(b2) == False

def test_large_dataset():
    manager = BookingManager()
    count = 0
    rooms = [f"E{100 + i}" for i in range(6)]

    for day in range(1, 21):   # 20 days
        date = f"2026-05-{day:02d}"
        for room_index, room_id in enumerate(rooms):   # 6 rooms each day
            start_hour = 8 + room_index
            booking = Booking(
                room_id,
                f"Event-{count + 1}",
                date,
                f"{start_hour:02d}:00",
                f"{start_hour + 1:02d}:00",
                f"Organizer-{count + 1}"
            )
            assert manager.add_booking(booking) is True
            count += 1

    assert count == 120
    assert len(manager.get_all_sorted()) == 120

def test_same_time_different_rooms():
    manager = BookingManager()
    b1 = Booking("E101", "A", "2026-04-15", "09:00", "10:00", "Prof")
    b2 = Booking("E102", "B", "2026-04-15", "09:00", "10:00", "Prof")

    result1= manager.add_booking(b1)
    result2 =manager.add_booking(b2)

    assert result1 == True
    assert result2 == True

def print_all_bookings():
    manager = BookingManager()
    b1 = Booking("E101", "Math", "2026-04-15", "08:00", "09:00", "Prof A")
    b2 = Booking("E101", "Physics", "2026-04-15", "09:00", "10:00", "Prof B")
    b3 = Booking("E101", "Chemistry", "2026-04-15", "10:00", "11:00", "Prof C")

    b4 = Booking("E102", "Biology", "2026-04-15", "08:00", "09:00", "Prof D")
    b5 = Booking("E102", "History", "2026-04-15", "09:00", "10:00", "Prof E")
    b6 = Booking("E102", "English", "2026-04-15", "10:00", "11:00", "Prof F")

    b7 = Booking("E201", "CS101", "2026-04-15", "08:00", "09:00", "Prof G")
    b8 = Booking("E201", "CS102", "2026-04-15", "09:00", "10:00", "Prof H")
    b9 = Booking("E201", "CS103", "2026-04-15", "10:00", "11:00", "Prof I")

    b10 = Booking("E202", "Art", "2026-04-15", "08:00", "09:00", "Prof J")
    b11 = Booking("E202", "Music", "2026-04-15", "09:00", "10:00", "Prof K")
    b12 = Booking("E202", "Drama", "2026-04-15", "10:00", "11:00", "Prof L")

    b13 = Booking("E301", "Economics", "2026-04-15", "08:00", "09:00", "Prof M")
    b14 = Booking("E301", "Finance", "2026-04-15", "09:00", "10:00", "Prof N")
    b15 = Booking("E301", "Accounting", "2026-04-15", "10:00", "11:00", "Prof O")
    manager.add_booking(b1)
    manager.add_booking(b2)
    manager.add_booking(b3)
    manager.add_booking(b4)
    manager.add_booking(b5)
    manager.add_booking(b6)
    manager.add_booking(b7)
    manager.add_booking(b8)
    manager.add_booking(b9)
    manager.add_booking(b10)
    manager.add_booking(b11)
    manager.add_booking(b12)
    manager.add_booking(b13)
    manager.add_booking(b14)
    manager.add_booking(b15)

    manager.print_all()

