import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        
    def enque_function(self,function,floor,room,building,operation):
        class lambda_wraper:
            def __init__(self):
                self.function = function
                self.floor = floor
                self.room = room
                self.operation = operation
                self.building = building
        self.buffer.append_buffer(lambda_wraper())
