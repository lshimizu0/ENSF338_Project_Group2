import copy
from Building import Building

class Campus:
    def __init__(self, campus_map_dict):
        if not campus_map_dict:
            raise Exception("Campus map dictionary is empty")
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
        
        # register all buildings
        for building_id in buildings_dict.keys():
            self.add_vertex_data(building_id)

        # build the objects and pathways
        for building_id, building_data in buildings_dict.items():
            # Create the Building Object
            new_building = Building(building_id, building_data.get('name'), building_data.get('location', (0,0)))
            
            # Add Rooms to that Building
            rooms_dict = building_data.get('rooms', {})
            for r_id, r_info in rooms_dict.items():
                new_building.insert_room(r_id, 
                    r_info['capacity'], 
                    r_info['room_type']
                )
                
            # 3. Store in the Dictionary
            self.buildings[building_id] = new_building
            
            # 4. Create the Pathways (Edges)
            for connection, weight in building_data.get('connections', {}).items():
                self.add_edge(building_id, connection, weight)


    def shortest_path(self, start_vertex_data, end):
        start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [float('inf')] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size
        path = [self.vertex_data[start_vertex]]
        paths = [[] for _ in range(self.size)]


        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
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
                        paths[v] = copy.deepcopy(path)
                    else:
                        path.pop()

            path = [self.vertex_data[start_vertex]]

        return paths, distances
    
    def add_building(self, building):
        self.buildings[building.building_id] = building

    def lookup_resource(self, b_id, r_id=None):
        
        building = self.buildings.get(b_id)
        if not building:
            return None
        if r_id:
            return building.get_room(r_id) # O(1) room lookup
        return building