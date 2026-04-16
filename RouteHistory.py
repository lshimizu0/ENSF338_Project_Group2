class RouteHistory:
    def __init__(self, max_undo=10):
        self.history = []
        self.max_undo = max_undo

    def add_route(self, origin, destination, path, total_distance):
        route_record = {
            "origin": origin,
            "destination": destination,
            "path": path,
            "total_distance": total_distance
        }

        self.history.append(route_record)
        return route_record

    def undo(self):
        if len(self.history) <= 1:
            return None

        self.history.pop()
        return self.history[-1]

    def get_current_route(self):
        if not self.history:
            return None
        return self.history[-1]

    def can_undo(self):
        return len(self.history) > 1

    def show_history(self):
        return self.history