import copy
from Building import Building
from Room import Room

class Campus:
    def __init__(self, campus_map_dict):
        if not campus_map_dict:
            raise Exception("Campus map dictionary is empty")
        self.name_to_id = {}
        self.buildings = {} # building_id -> Building
        self.capacity = len(campus_map_dict.get('buildings').keys())
        self.pathways = [[0] * self.capacity for _ in range(self.capacity)]
        self.vertex_data = [''] * self.capacity
        self.size = 0
        self.setup(campus_map_dict)


    # u -> v, weight = weight
    def add_edge(self, start, end, weight):
        u = self.vertex_data.index(start)
        v = self.vertex_data.index(end)
        self.pathways[u][v] = weight
        self.pathways[v][u] = weight

    def add_vertex_data(self, data):
        self.vertex_data[self.size] = data
        self.size+=1

    def setup(self, campus_map_dict):
        buildings_dict = campus_map_dict.get('buildings')
        for building_id in buildings_dict.keys():
            self.add_vertex_data(building_id)
            building = Building(building_id, buildings_dict[building_id]['name'], (0, 0))
            for room_id in buildings_dict[building_id]['rooms'].keys():
                room = Room(room_id, buildings_dict[building_id]['rooms'][room_id]['capacity'], buildings_dict[building_id]['rooms'][room_id]['room_type'])
                building.rooms[room_id] = copy.deepcopy(room)
            self.buildings[building_id] = copy.deepcopy(building)
            self.name_to_id[building.name.strip().lower()] = building_id 
        for building_id, building_data in buildings_dict.items():
            # building = Building(building_id, building_data)
            for connection, weight in building_data.get('connections', {}).items():
                self.add_edge(building_id, connection, weight)



    def shortest_path(self, start_vertex_data, end_vertex_data):
        try:
            start_vertex = self.vertex_data.index(start_vertex_data)
            end_vertex = self.vertex_data.index(end_vertex_data)
        except ValueError:
            return -1, -1

        distances = [float('inf')] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size
        path = []
        paths = [[] for _ in range(self.size)]


        for _ in range(self.size):

            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    path = [self.vertex_data[i]]
                    u = i

            if u is None:
                break

            visited[u] = True

            for v in range(self.size):
                if self.pathways[u][v] != 0 and not visited[v]:
                    path.append(self.vertex_data[v])
                    alt = distances[u] + self.pathways[u][v]
                    if alt < distances[v]:
                        distances[v] = alt
                        if path and path[0] != start_vertex_data:
                            path.pop(0)
                        paths[v] = paths[u]+copy.deepcopy(path)
                        if path and path[0] == start_vertex_data:
                            path.pop()
                    else:
                        path.pop()
        return paths[end_vertex], distances[end_vertex]

    def get_building_id_by_name(self, building_name):
        if building_name is None:
            return None
        return self.name_to_id.get(building_name.strip().lower())

    def lookup_building_by_name(self, building_name):
        building_id = self.get_building_id_by_name(building_name)
        if building_id is None:
            return None
        return self.buildings.get(building_id)

    def lookup_room_by_building_name(self, building_name, room_id):
        building = self.lookup_building_by_name(building_name)
        if building is None:
            return None
        return building.lookup_room(room_id)

    def get_room_ids_by_building_name(self, building_name):
        building = self.lookup_building_by_name(building_name)
        if building is None:
            return None
        return building.get_room_ids()