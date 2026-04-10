# Youssef Ibrahim
#doing this via a linked list implementation of a queue

class RequestNode:
    def __init__(self, data : str):
        self.data = data
        self.next = None

class RequestQueue:
    def __init__(self):
        self.head : RequestNode = None
        self.tail : RequestNode = None
    
    def enqueue(self, data : str):
        new_node : RequestNode = RequestNode(data)

        if self.tail is not None:
            self.tail.next = new_node
        self.tail = new_node
        if self.head is None:
            self.head = new_node

    def dequeue(self):
        if self.head is None:
            return None
        temp = self.head

        self.head = self.head.next
        if self.head is None:
            self.tail = None
        
        return temp.data
    
    def peek(self):
        return self.head.data


#testing

