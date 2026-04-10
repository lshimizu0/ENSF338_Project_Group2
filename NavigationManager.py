import json
with open("campus_map.json") as f:
    campus_map_dict = json.load(f)

class NavigationManager:
    def __init__(self, campus_map_dict, max_undo=10):
        self.history = []
        self.max_undo = max_undo
        self.campus_map = campus_map_dict
        self.current_location = None


    def get_connections(self, location_id):
        try:
            connections = self.campus_map["buildings"][location_id]["connections"]
            return list(connections.keys())
        except KeyError:
            print(f"{location_id} is not a valid location ID")
            return -1

        
    def set_starting_point(self, building_id):
        self.current_location = building_id
        self.history.append(building_id) 

    # Push (append)
    def push(self, building_id):

        if building_id == "undo":
            self.pop()
            return

        if self.current_location is None:
            if building_id not in self.campus_map["buildings"]:
                print(f"{building_id} is not a valid location ID")
                return -1
            self.current_location = building_id
            self.history.append(building_id)
            return

        valid_connections = self.get_connections(self.current_location)

        if valid_connections == -1:
            print(
                f"Cannot move from {self.current_location} to {building_id}. "
                f"Valid options: {valid_connections}"
            )
            return -1

        # If we're at capacity, remove the oldest element
        if len(self.history) >= self.max_undo:
            self.history.pop(0)  # removes oldest (bottom of stack)
            
        self.current_location = building_id
        self.history.append(building_id)
        return
        
    # Pop (undo)
    def pop(self):
        if not self.history:
            return None
        popped = self.history.pop()
        if not self.history:
            self.current_location = None
        else:
            self.current_location = self.history[-1]
        return popped


    # Peek (view last without removing)
    def peek(self):
        if not self.history:
            return None
        return self.history[-1]

    # check if empty
    def is_empty(self):
        return len(self.history) == 0
    