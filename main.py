from NavigationManager import Navigation
from Campus import Campus
from time import sleep
import json

with open('campus_map.json') as json_data:
    campus_map = json.load(json_data)
name_to_id = {}
# making a name to id dictionary so we only have to have O(n) once instead of multiple times
# to find the id given the name of the building by user
for building_id in campus_map['buildings'].keys():
    name_to_id[campus_map[building_id].name] = building_id
# AI Used for how display looks, prompt: Make this display look cooler. Don't change any of the code logic just the print statements
print("Campus Navigation and Event Manager System")
print("Starting program...")

sleep(1)
navigation = Navigation(campus_map)
campus = Campus(campus_map)
while True:
    choice = input("Main Menu\n1. Navigation\n2. Room Bookings\n3. Service Requests\nChoice: ")
    startup = True
    match choice:
        case "1":
            if startup:
                navigation.set_starting_point()
                startup = False
            while True:
                nav_choice = input("Navigation Menu\n1. GPS\n2. Movement\n3. Back\nChoice: ")
                match nav_choice:
                    case "1":
                        dest = input("Input Destination for shortest path: ")
                        path, time = campus.shortest_path(navigation.current_location(), name_to_id.get(dest, "error"))
                        if path == -1:
                            print('Invalid Destination')
                            continue
                        print(f'the shortest path to {dest} is', end=' ')
                        for node in path:
                            if node is not path[-1]:
                                print(f'{campus_map[node].name}->', end=' ')
                            else:
                                print(campus_map[node].name, end=' ')
                        print(f'which will take {time} minutes')
                    case "2":
                        connections = navigation.get_connections()
                        print('Available buildings (enter undo to undo previous movement):')
                        for connection in connections:
                            print(campus_map[connection].name, end=' ')
                        print('')
                        choice = input("Choice: ")
                        navigation.push(name_to_id.get(choice, "error"))
                    case "3":
                        break
        case '2':
            pass