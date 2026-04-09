import sys
import os
from typing import TypeVar, Generic, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = TypeVar("T")

class FifoRingBuffer(Generic[T]):
    def __init__(self, capacity: int = 0) -> None: # removed the data_types since using generics should make it redundant
        self.read_index = -1
        self.write_index = 0
        self.capacity = capacity
        self.buffer: list[Optional[T]] = [None] * capacity
        self.items = 0

    def append_buffer(self, data: T) -> None:
        if self.items < self.capacity:
            self.items += 1 
        self.buffer[self.write_index] = data
        self.write_index += 1
        self.write_index %= self.capacity 

    def pop(self) -> None | T:
        if self.items > 0:
            self.items -= 1
            self.read_index += 1
            self.read_index %= self.capacity
            return_value = self.buffer[self.read_index]
            return(return_value)
        else:
            return None

    def peek(self) -> None | T:
        if self.items > 0:
            return(self.buffer[self.read_index]) # may potentially not work to look at next item in buffer. would only look at current, right?
        else:
            return None
        
    def read_at_index(self, index: int) -> None | T:
        if index > self.capacity:
            return None
        return self.buffer[(self.write_index + index)% self.capacity]

    def write_at_index(self, index: int) -> None | T:
        if index > self.capacity:
            return None
        return self.buffer[(self.write_index + index)% self.capacity]
