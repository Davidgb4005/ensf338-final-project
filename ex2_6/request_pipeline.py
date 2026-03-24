import DataStructures.FiFo_ringBuffer as fifo

class request_pipeline:
    def __init__(self):
        self.buffer = fifo.ring_buffer(1024,None)
        pass

    def deque_function(self):
        current_function = self.buffer.pop()
        if current_function != None:
            current_function()
            print("dequeWorked")
        else:
            print("que Empty")
            return None
        
    def enque_function(self,function):
        self.buffer.append_buffer(function)