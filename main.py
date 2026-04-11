from BookingSystem import Booking
from NavigationManager import NavigationManager
from Campus import Campus
import BookingSystem
import json

# ---------------------------Setup---------------------------
with open('campus_map.json') as json_data:
    campus_map = json.load(json_data)

# making a name to id dictionary so we only have to have O(n) once instead of multiple times
# to find the id given the name of the building by user
name_to_id = {}
for building_id in campus_map['buildings'].keys():
    name_to_id[campus_map['buildings'][building_id]['name'].lower()] = building_id

booking_id = "0"

navigation = NavigationManager(campus_map)
campus = Campus(campus_map)
bookingManager = BookingSystem.BookingManager()


startup = True
# ---------------------------Program---------------------------
print("Campus Navigation and Event Manager System")
print("Starting program...")
while True:
    choice = input("Main Menu\n1. Navigation\n2. Room Bookings\n3. Service Requests\n4. Quit\nChoice: ").strip()
    match choice:
        # Navigation
        case "1":
            # First time running must get where the user is initially
            if startup:
                current_location = input("what is your current location?: ").strip().lower()
                if name_to_id.get(current_location, None) is not None:
                    navigation.set_starting_point(name_to_id[current_location])
                    startup = False
                else:
                    print("Not a valid building name")
                    continue

            while True:
                print("Current Location: ", campus_map['buildings'][navigation.current_location]['name'])

                nav_choice = input("Navigation Menu\n1. GPS\n2. Movement\n3. Back\nChoice: ").strip()
                match nav_choice:

                    # GPS (Nav Menu)
                    case "1":
                        dest = input("Input Destination for shortest path: ").strip().lower()
                        path, time = campus.shortest_path(navigation.peek(), name_to_id.get(dest, "error"))
                        if path == -1:
                            print('Invalid Destination')
                            continue
                        # Printing it nicely for user
                        print(f'The shortest path to {dest} is', end=' ')
                        for node in path:
                            if node is not path[-1]:
                                print(f'{campus_map['buildings'][node]['name']}->', end=' ')
                            else:
                                print(campus_map['buildings'][node]['name'], end=' ')
                        print(f'which will take {time} minutes')

                    # Movement (Nav Menu)
                    case "2":
                        connections = navigation.get_connections()
                        print('Available buildings (enter undo to undo previous movement):')
                        for connection in connections:
                            print(campus_map['buildings'][connection]['name'], end=' ')
                        print('')
                        choice = input("Choice: ").strip().lower()
                        if choice != 'undo':
                            navigation.push(name_to_id.get(choice, "error"))
                        else:
                            if navigation.push('undo') == -1:
                                continue

                    case "3":
                        break
        # Room Booking
        case '2':
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
            print("Current Bookings: ")
            if not campus.buildings[building_id].rooms[roomID].bookings:
                print("No current bookings")
            else:
                for booking in campus.buildings[building_id].rooms[roomID].bookings:
                    print(booking)
            date = input("Date For booking(YYYY-MM-DD): ")
            start_time = input("Start Time for booking(HH:MM 24h clock): ")
            end_time = input("End Time for booking(HH:MM 24h clock): ")
            event_name = input("Event Name for booking: ")
            organizer_name = input("Organizer Name for booking: ")

            booking = BookingSystem.Booking(booking_id, roomID, event_name, date, start_time, end_time, organizer_name)
            booking_id = int(booking_id)
            booking_id+=1
            booking_id = str(booking_id)
            bookingManager.add_booking(booking)



