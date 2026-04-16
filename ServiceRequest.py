class ServiceRequest:
    def __init__(self, description, priority):
        self.description = description
        self.priority = priority 

    def __repr__(self):
        levels = {1: "Emergency", 2: "Standard", 3: "Low"}
        return f"[{levels[self.priority]}] {self.description}"


class ServiceRequestQueue:
        def __init__(self):
            self.heap = []

        def insert_request(self, request):
            self.heap.append(request)
            self.heapify_up(len(self.heap) - 1)

        def process_request(self):
            if not self.heap:
                return None
            top_request = self.heap[0]
            last_request = self.heap.pop()
            if self.heap:
                self.heap[0] = last_request
                self.heapify_down(0)
            return top_request

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

#demo
if __name__ == "__main__":
    queue = ServiceRequestQueue()
    queue.insert_request(ServiceRequest("Fix leaky toilet", 2))
    queue.insert_request(ServiceRequest("Power outage in building", 1))
    queue.insert_request(ServiceRequest("Replace light bulb", 3))
    queue.insert_request(ServiceRequest("Projector broken", 2))
    queue.insert_request(ServiceRequest("Air conditioning not working", 1))

    print("Current Queue:")
    print(queue)

    print("\nProcessing requests:")
    while True:
        request = queue.process_request()
        if not request:
            break
        print(f"Processed: {request}")
