# Youssef Ibrahim
#doing this via a linked list implementation of a queue

class RequestNode:
    """
    Represents a single node in the request queue, holding the contents of an individual request.
    """
    def __init__(self, data : str):
        """
        Initializes a new RequestNode with the provided data.

        Parameters:
            data (str): the value of the request to hold in the RequestNode
        """
        self.data = data
        self.next = None

class RequestQueue:
    """
    A FIFO queue for processing incoming requests.
    Has a head and tail pointer for O(1) complexity on both enqueue and dequeue.
    """
    def __init__(self):
        """
        Initializes an empty RequestQueue.
        """
        self.head : RequestNode = None
        self.tail : RequestNode = None
    
    def enqueue(self, data : str):
        """
        Adds a new request with the provided data to the request queue (added at the end).

        Parameters:
            data (str): the content of the request to hold in the queue as a RequestNode
        """
        new_node : RequestNode = RequestNode(data)

        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node

    def dequeue(self):
        """
        Dequeues and returns request data at the front of the queue.

        Returns:
            The data inside the RequestNode at the head, detailing the request
        """
        if self.head is None:
            print("Queue is empty.")
            return None
            
        temp : RequestNode = self.head

        self.head = self.head.next
        if self.head is None:
            self.tail = None
        
        return temp.data
    
    def peek(self):
        """
        Returns request data at the front of the queue without dequeueing.

        Returns:
            The data inside the RequestNode at the head, detailing the request
        """
        if self.head is None:
            print("Queue is empty.")
            return None
        return self.head.data


#testing

new_queue : RequestQueue = RequestQueue()

for i in range(20):
    print("queued: request " + str(i))
    new_queue.enqueue("request " + str(i))

for i in range(20):
    print("dequeued: " + new_queue.dequeue())
