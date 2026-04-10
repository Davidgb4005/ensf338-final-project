import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class FifoRingBuffer:
    capacity= 0
    items = 0
    read_index = -1
    write_index = 0
    data_type = None
    buffer = []
    def __init__(self,capacity,data_type):
        self.data_type = type(data_type)
        self.capacity = capacity
        for i in range(capacity):
            self.buffer.append(None)
        self.index = capacity
        self.items = 0
        pass

    def append_buffer(self,data):
        if self.items < self.capacity:
            self.items += 1 

        self.buffer[self.write_index] = data
        self.write_index += 1
        self.write_index %= self.capacity 

    def pop(self):
        if self.items>0:
            self.items -= 1
            self.read_index += 1
            self.read_index %= self.capacity
            return_value = self.buffer[self.read_index]
            return(return_value)
        else:
            return None

    def peak(self):
        if self.items>0:
            return(self.buffer[self.read_index])
        else:
            return None
        
        
    def read_at_index(self,index):
        if index > self.capacity:
            return None
        return self.buffer[(self.write_index + index )% self.capacity]
    def write_at_index(self,index):
        if index > self.capacity:
            return None
        return self.buffer[(self.write_index + index )% self.capacity]
