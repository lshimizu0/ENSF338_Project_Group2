import json
from Manager import Manager
from Campus import Campus

with open('campus_map.json', 'r') as file:
    campus_map = json.load(file)

campus = Campus(campus_map)
print(campus.shortest_path("B1", "B4"))