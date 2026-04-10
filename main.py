from NavigationManager import NavigationManager
from Campus import Campus
from time import sleep
import json

with open('campus_map.json') as json_data:
    campus_map = json.load(json_data)
name_to_id = {}
# making a name to id dictionary so we only have to have O(n) once instead of multiple times
# to find the id given the name of the building by user
for building_id in campus_map['buildings'].keys():
    name_to_id[campus_map['buildings'][building_id]['name']] = building_id
# AI Used for how display looks, prompt: Make this display look cooler. Don't change any of the code logic just the print statements
print("Campus Navigation and Event Manager System")
print("Starting program...")

sleep(1)
navigation = NavigationManager(campus_map)
campus = Campus(campus_map)
while True:
    choice = input("Main Menu\n1. Navigation\n2. Room Bookings\n3. Service Requests\nChoice: ").strip()
    startup = True
    match choice:
        case "1":
            if startup:
                current_location = input("what is your current location?: ").strip()
                if current_location in name_to_id.keys():
                    navigation.set_starting_point(name_to_id[current_location])
                    startup = False
                else:
                    print("Not a valid building name")
                    continue
            while True:
                print("Current Location: ", campus_map['buildings'][navigation.current_location]['name'])
                nav_choice = input("Navigation Menu\n1. GPS\n2. Movement\n3. Back\nChoice: ").strip()
                match nav_choice:
                    case "1":
                        dest = input("Input Destination for shortest path: ").strip()
                        path, time = campus.shortest_path(navigation.peek(), name_to_id.get(dest, "error"))
                        if path == -1:
                            print('Invalid Destination')
                            continue
                        print(f'The shortest path to {dest} is', end=' ')
                        for node in path:
                            if node is not path[-1]:
                                print(f'{campus_map['buildings'][node]['name']}->', end=' ')
                            else:
                                print(campus_map['buildings'][node]['name'], end=' ')
                        print(f'which will take {time} minutes')
                    case "2":
                        connections = navigation.get_connections()
                        print('Available buildings (enter undo to undo previous movement):')
                        for connection in connections:
                            print(campus_map['buildings'][connection]['name'], end=' ')
                        print('')
                        choice = input("Choice: ").strip()
                        if choice != 'undo':
                            navigation.push(name_to_id.get(choice, "error"))
                        else:
                            if navigation.push('undo') ==-1:
                                continue

                    case "3":
                        break
        case '2':
            pass