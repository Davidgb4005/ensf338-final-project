import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class LifoRingBuffer:
    def __init__(self,capacity,data_type):
        self.buffer = []
        self.data_type = data_type
        self.capacity = capacity
        if self.data_type != None:
            for i in range(capacity):
                self.buffer.append(data_type())
        else:
            for i in range(capacity):
                self.buffer.append(None)
        self.index = capacity
        self.items = 0
        pass

    def append(self,data):
        if self.items < self.capacity:
            self.items += 1 
        self.index += 1
        self.index %= self.capacity
        self.buffer[self.index] = data

    def pop(self):
        if self.items>0:
            return_value = self.buffer[self.index]
            self.items -= 1
            self.index -= 1
            self.index %= self.capacity
            return(return_value)
        else:
            return None

    def peak(self):
        if self.items>0:
            return(self.buffer[self.index])
        else:
            return None
        
    def access_at_index(self,index):
        if index > self.capacity:
            return None
        return self.buffer[(self.index + index )% self.capacity]