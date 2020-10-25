
# Python3 Linked list based implementation of queue 
  
# A linked list (LL) node 
# to store a queue entry 
class Node: 
      
    def __init__(self, data): 
        self.data = data 
        self.next = None
  
# A class to represent a queue 
  
# The queue, front stores the front node 
# of LL and rear stores the last node of LL 
class Queue: 
      
    def __init__(self): 
        self.front = self.rear = None
        self.size = 0
  
    def isEmpty(self): 
        return self.front == None

    def EmptyQueue(self):
        self.__init__()
      
    # Method to add an item to the queue 
    def EnQueue(self, item): 
        temp = Node(item) 
          
        if self.rear == None: 
            self.front = self.rear = temp 
            self.size += 1
            return
        self.rear.next = temp 
        self.rear = temp 
        self.size += 1
  
    # Method to remove an item from queue 
    def DeQueue(self): 
        if self.isEmpty(): 
            return
        temp = self.front 
        self.front = temp.next
  
        if(self.front == None): 
            self.rear = None

        self.size -= 1

        return temp.data

    # Method to see value of front node
    def Peek(self):
        return self.front.data

    def Seek(self):
        return self.rear.data

    

