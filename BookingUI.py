from BookingSystem import Booking, BookingManager

def divider():
    print("="*20)

def booking_cli(building_name, manager):
    divider()
    print(f"Building: {building_name}")

    while True:
        divider()
        print("Booking Menu")
        divider()
        print("1) Add Booking\
              \n2) Remove Booking\
              \n3) View Booking by ID\
              \n4) View All Bookings\
              \n5) Search by date\
              \n6) Search by date & time range\
              \n7) Next upcoming booking\
              \n8) Back")
        choice = input("Choice (1-8): ").strip()

        match choice:
            # Add booking
            case "1":
                booking_id = input("\nBooking ID (e.g. BK001): ").strip()
                room_id = input("Room ID (e.g. E101): ").strip()
                event_name = input("Event name: ").strip()
                organizer = input("Name: ").strip()
                date = input("Date (YYYY-MM-DD): ").strip()
                start_time = input("Start Time (HH:MM, 24h): ").strip()
                end_time = input("End Time (HH:MM, 24h): ").strip()

                if not all([booking_id, room_id, event_name, organizer, date, start_time, end_time]):
                    print("ERROR: No fields can be left empty")
                    continue

                if start_time >= end_time:
                    print("End time must be later than start time.")
                    continue

                booking = Booking(
                    booking_id=booking_id, 
                    room_id= room_id, 
                    event_name=event_name, 
                    organizer=organizer, 
                    date=date, 
                    start_time=start_time, 
                    end_time=end_time
                    )
                
                manager.add_booking(booking)

            # remove booking
            case "2":
                booking_id = input("Booking ID (e.g. BK001): ").strip()
                room = input("Room name: ").strip()
                manager.remove_booking(booking_id)

            # booking by id
            case "3":
                booking_id = input("Booking ID: ").strip()
                manager.get_booking(booking_id)

            # view all booking
            case "4":
                manager.print_all()

            # search by date
            case "5":
                date = input("Date (YYYY-MM-DD): ")
                manager.query_by_date(date)

            # search by date and time range
            case "6":
                date = input("Date (YYYY-MM-DD): ")
                start_time = input("Start Time (HH:MM, 24h): ")
                end_time = input("End Time (HH:MM, 24h): ")
                manager.queryRange(date, start_time, end_time)

            # upcoming booking
            case "7":
                manager.next_upcoming()

            case "8":
                break

            case _:
                print("Invalid option, please enter (1-8)")

manager = BookingManager()       
booking_cli("ST", manager)
        