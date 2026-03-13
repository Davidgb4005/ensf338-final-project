'''This is the implementaion for the undo feature used in the traversal
This implementaion can only store 1 type of data'''


class ring_buffer:
    capacity= 0
    items = 0
    index = 0
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

    def append(self,data):
        if self.items < self.capacity:
            self.items += 1 
        self.index %= self.capacity
        self.buffer[self.index] = data

    def pop(self):
        if self.items>0:
            self.items -= 1
            self.index -= 1
            self.index %= self.capacity
            return(self.buffer[self.index])
        else:
            return None

    def peak(self):
        if self.items>0:
            return(self.buffer[self.index])
        else:
            return None