import copy
from Building import Building

class Campus:
    def __init__(self, campus_map_dict):
        if not campus_map_dict:
            raise Exception("Campus map dictionary is empty")

        self.buildings = {}      # building_id -> Building
        self.name_to_id = {}     # building_name.lower() -> building_id

        self.capacity = len(campus_map_dict.get('buildings', {}).keys())
        self.pathways = [[0] * self.capacity for _ in range(self.capacity)]
        self.vertex_data = [''] * self.capacity
        self.size = 0

        self.setup(campus_map_dict)

    def add_edge(self, start, end, weight):
        u = self.vertex_data.index(start)
        v = self.vertex_data.index(end)
        self.pathways[u][v] = weight
        self.pathways[v][u] = weight

    def add_vertex_data(self, data):
        self.vertex_data[self.size] = data
        self.size += 1

    def setup(self, campus_map_dict):
        buildings_dict = campus_map_dict.get('buildings', {})

        # register building ids for graph
        for building_id in buildings_dict.keys():
            self.add_vertex_data(building_id)

        for building_id, building_data in buildings_dict.items():
            name = building_data.get('name')
            location = building_data.get('location', (0, 0))

            new_building = Building(building_id, name, location)

            # build fast name -> id map once
            self.name_to_id[name.lower()] = building_id

            # add rooms from JSON
            rooms_dict = building_data.get('rooms', {})
            for room_id, room_info in rooms_dict.items():
                new_building.insert_room(
                    room_id,
                    room_info['capacity'],
                    room_info['room_type']
                )

            self.buildings[building_id] = new_building

            # add graph edges
            for connection, weight in building_data.get('connections', {}).items():
                self.add_edge(building_id, connection, weight)

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