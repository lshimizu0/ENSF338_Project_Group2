from BookingSystem import Booking

def divider():
    print("="*20)

def booking_cli(manager, campus, name_to_id):
    divider()

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
                building_id = input("What building do you want to book in?: ").strip().lower()
                if name_to_id.get(building_id, None) is not None:
                    building_id = name_to_id[building_id]
                else:
                    print("Not a valid building name")
                    continue
                print("Rooms Available:")
                for room in campus.buildings[building_id].rooms.values():
                    print(room)
                roomID = input("Enter the id of the room you would like to book in: ").strip()
                if campus.buildings[building_id].rooms.get(roomID, None) is None:
                    print("Not a valid room id")
                    continue
                room = campus.buildings[building_id].rooms.get(roomID)
                date = input("Date For booking(YYYY-MM-DD): ")
                start_time = input("Start Time for booking(HH:MM 24h clock): ")
                end_time = input("End Time for booking(HH:MM 24h clock): ")
                event_name = input("Event Name for booking: ")
                organizer_name = input("Organizer Name for booking: ")
                if not all([roomID, event_name, organizer_name, date, start_time, end_time]):
                    print("ERROR: No fields can be left empty")
                    continue

                booking = Booking(roomID, event_name, date, start_time, end_time, organizer_name)
                manager.add_booking(booking, room)

            # remove booking
            case "2":
                booking_id = input("Booking ID (e.g. BK001): ").strip()
                room_id = input("Room Id: ").strip()
                room = None
                for building in campus.buildings.values():
                    if building.rooms.get(room_id, None) is not None:
                        room = building.rooms.get(room_id)
                        break
                if not room:
                    print("Not a valid room id")
                    continue

                manager.remove_booking(booking_id, room)

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

        