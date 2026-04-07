class ServiceRequest:
    def __init__(self, description, priority):
        self.description = description
        self.priority = priority 

    def __repr__(self):
        levels = {1: "High", 2: "Standard", 3: "Low"}
        return f"[{levels[self.priority]}] {self.description}"


    class ServiceRequestQueue:
        def __init__(self):
            self.heap = []

        def insert_request(self, request):
            self.heap.append(request)
            self.heapify_up(len(self.heap) - 1)

        def heapify_up(self, index):
            parent_index = (index - 1) // 2
            if index > 0 and self.heap[index].priority < self.heap[parent_index].priority:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                self.heapify_up(parent_index)

        def heapify_down(self, index):
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2

            if left_child < len(self.heap) and self.heap[left_child].priority < self.heap[smallest].priority:
                smallest = left_child
            if right_child < len(self.heap) and self.heap[right_child].priority < self.heap[smallest].priority:
                smallest = right_child
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                self.heapify_down(smallest)
            

        def __repr__(self):
            return "\n".join(str(request) for request in self.heap)

