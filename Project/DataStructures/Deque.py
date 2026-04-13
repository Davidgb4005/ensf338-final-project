import sys
import os
from typing import TypeVar, Generic, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = TypeVar("T") #for strict type hinting

class Node(Generic[T]):
    """
    A container class that holds the information of an individual node in a queue, along with pointers to previous and next node.
    . . .
    Attributes
    ----------
    val: T
        The information that the node stores.
    prev: Optional[Node[T]]
        Reference to previous node in queue. Optionally None if it doesn't exist
    next: Optional[Node[T]]
        Reference to next node in queue. Optionally None if it doesn't exist
    """
    def __init__(self, val: T) -> None:
        self.val = val
        self.prev: Optional[Node[T]] = None #either node, or none
        self.next: Optional[Node[T]] = None

class Deque(Generic[T]):
    """
    Class that handles objects of Node class in a queue, implemented with a linked list.
    . . .
    Attributes
    ----------
    head: Optional[Node[T]]
        Reference to the head of the queue. Optionally None if no nodes in queue.
    tail: Optional[Node[T]]
        Reference to the tail end of the queue. Optionally None if no nodes in queue.
    len: int
        Current length of the queue. Starts at 0 to indicate no nodes in queue.
    
    Methods
    -------
    append_tail(val: T)
        Enqueues a node containing the data of arg 'val' into the tail end of the linked list.
    append_head(val: T)
        Enqueues a node containing the data of arg 'val' into the head of the linked list.
    pop_tail()
        Dequeues, removes, and returns the node from the end of the linked list.
    pop_head()
        Dequeues, removes, and returns the node from the head of the linked list.
    peek_head()
        Returns reference to the node at head of queue.
    peek_tail()
        Returns reference to the node at tail of queue.
    get_len()
        Returns int value of self.len
    peek_que
        Returns the node currently at self.next
    """
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None #without optional, doing .next would report unknown type
        self.tail: Optional[Node[T]] = None
        self.len = 0

    def append_tail(self, val: T) -> None:
        """
        Enqueues a node to the tail end of the linked list, then increases len of queue by 1.
        Args:
            val(T): Information to be stored in the node.
        """
        node = Node(val)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = self.tail = node
        self.len += 1

    def append_head(self, val: T) -> None:
        """
        Enqueues a node to the top head of the linked list queue, then increases len of queue by 1.
        Args:
            val(T): Information to be stored in the node.
        """
        node = Node(val)
        if self.head:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            self.head = self.tail = node
        self.len += 1

    def pop_tail(self) -> None | T:
        """
        Dequeues, removes, and returns the node at the tail end of the linked list. Decrements len by 1.
        """
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
        """
        Dequeues, removes, and returns the node at the top head of the linked list. Decrements len by 1.
        """
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
        """
        Returns reference to the current node at head of the queue, or None if empty.
        """
        if not self.head:
            print("peek from empty deque")
            return None
        return self.head

    def peek_tail(self) -> None | Node[T]:
        """
        Returns reference to the current node at tail of the queue, or None if empty.
        """
        if not self.tail:
            print("peek from empty deque")
            return None
        return self.tail

    def get_len(self) -> int:
        """
        Returns int value of queue length.
        """
        return self.len
    
    def peek_que(self, node:Node[T]) -> None | Node[T]:
        """
        Returns reference to the node after arg 'node'. If next node is tail, returns None.
        Args:
            node(Node[T]): The node who's next node is being looked at.
        """
        if node != self.tail:
            return node.next
        else:
            return None