from NavigationManager import NavigationManager
from Campus import Campus
from service_queue import ServiceRequest, ServiceRequestQueue
import json

# ---------------------------Setup---------------------------
with open('campus_map.json') as json_data:
    campus_map = json.load(json_data)

# making a name to id dictionary so we only have to have O(n) once instead of multiple times
# to find the id given the name of the building by user
name_to_id = {}
for building_id in campus_map['buildings'].keys():
    name_to_id[campus_map['buildings'][building_id]['name'].lower()] = building_id

navigation = NavigationManager(campus_map)
campus = Campus(campus_map)
startup = True

priority_map = {
    "high": 1,
    "medium": 2,
    "low": 3
}
service_queue = ServiceRequestQueue()
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
            building = input("What building would you like to book a room in?: ").strip().lower()
            if name_to_id.get(building, None) is None:
                print("Not a valid building name")
                continue





        case "3":
            while True:
                lookup_choice = input(
                    "\nFast Lookup Menu\n"
                    "1. Look up building\n"
                    "2. Look up room\n"
                    "3. Service Request\n"
                    "4. View Service Queue\n"
                    "5. Back\n"
                    "Choice: "
                ).strip()

                match lookup_choice:
                    case "1":
                        building_name = input("Enter building name: ").strip()
                        building = campus.lookup_building_by_name(building_name)

                        if building is None:
                            print("Building not found.")
                            continue

                        print("\nBuilding found:")
                        print("Name:", building.name)
                        print("Internal ID:", building.building_id)
                        print("Rooms:")
                        for room_id in building.get_room_ids():
                            print(room_id)

                    case "2":
                        building_name = input("Enter building name: ").strip()
                        room_ids = campus.get_room_ids_by_building_name(building_name)

                        if room_ids is None:
                            print("Building not found.")
                            continue

                        print("Available rooms:")
                        for room_id in room_ids:
                            print(room_id)

                        room_id = input("Enter room ID: ").strip()
                        room = campus.lookup_room_by_building_name(building_name, room_id)

                        if room is None:
                            print("Room not found.")
                            continue

                        print("\nRoom found:")
                        print("Room ID:", room.room_id)
                        print("Capacity:", room.capacity)
                        print("Type:", room.room_type)

                    case "3":
                        description = input("Enter your problem: ").strip()
                        severity_input = input("Enter severity (low, medium, high): ").strip().lower()

                        priority = priority_map.get(severity_input)

                        if priority is None:
                            print("Invalid severity. Please enter low, medium, or high.")
                            continue

                        request = ServiceRequest(description, priority)
                        service_queue.insert_request(request)

                        print("Request added to queue.")

                    case "4":
                        if not service_queue.heap:
                            print("Service queue is empty.")
                        else:
                            print("\nCurrent Service Queue:")
                            print(service_queue)

                    case "5":
                        break
                    case _:
                        print("Invalid choice.")