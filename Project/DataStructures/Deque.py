import sys
import os
from typing import TypeVar, Generic, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = TypeVar("T") #for strict type hinting
class Node(Generic[T]):
    def __init__(self, val: T) -> None:
        self.val = val
        self.prev: Optional[Node[T]] = None #either node, or none
        self.next: Optional[Node[T]] = None

class Deque(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None #without optional, doing .next would report unknown type
        self.tail: Optional[Node[T]] = None
        self.len = 0

    def append_tail(self, val: T) -> None:
        node = Node(val)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = self.tail = node
        self.len += 1

    def append_head(self, val: T) -> None:
        node = Node(val)
        if self.head:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            self.head = self.tail = node
        self.len += 1

    def pop_tail(self) -> None | T:
        if not self.tail:
            print("pop from empty deque")
            return None
        val = self.tail.val
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None          # list now empty
        self.len -= 1
        return val

    def pop_head(self) -> None | T:
        if not self.head:
            print("pop from empty deque")
            return None
        val = self.head.val
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None          # list now empty
        self.len -= 1
        return val

    def peek_head(self) -> None | Node[T]:
        if not self.head:
            print("peek from empty deque")
            return None
        return self.head

    def peek_tail(self) -> None | Node[T]:
        if not self.tail:
            print("peek from empty deque")
            return None
        return self.tail

    def get_len(self) -> int:
        return self.len
    
    def peek_que(self, node:Node[T]) -> None | Node[T]:
        if node != self.tail:
            return node.next
        else:
            return None