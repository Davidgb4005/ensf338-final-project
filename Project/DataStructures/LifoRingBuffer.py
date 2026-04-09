import sys
import os
from typing import TypeVar, Generic, Optional, Type
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = TypeVar("T")

class LifoRingBuffer(Generic[T]):
    def __init__(self, capacity: int, data_type: Optional[Type[T]]) -> None:
        self.data_type = data_type
        self.capacity = capacity
        self.index = capacity
        self.items = 0
        if self.data_type is not None:
            self.buffer: list[Optional[T]] = [self.data_type() for _ in range(capacity)]
        else:
            self.buffer = [None] * capacity

    def append(self, data: T) -> None:
        if self.items < self.capacity:
            self.items += 1 
        self.index += 1
        self.index %= self.capacity
        self.buffer[self.index] = data

    def pop(self) -> Optional[T]:
        if self.items > 0:
            return_value = self.buffer[self.index]
            self.items -= 1
            self.index -= 1
            self.index %= self.capacity
            return(return_value)
        else:
            return None

    def peek(self) -> Optional[T]:
        if self.items > 0:
            return(self.buffer[self.index])
        else:
            return None
        
    def access_at_index(self, index: int) -> Optional[T]:
        if index > self.capacity:
            return None
        return self.buffer[(self.index + index) % self.capacity]