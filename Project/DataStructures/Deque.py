import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
class Node:
    def __init__(self, val):
        self.val = val
        self.prev = self.next = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0

    def append_tail(self, val):
        node = Node(val)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = self.tail = node
        self.len += 1

    def append_head(self, val):
        node = Node(val)
        if self.head:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            self.head = self.tail = node
        self.len += 1

    def pop_tail(self):
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

    def pop_head(self):
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

    def peek_head(self):
        if not self.head:
            print("peek from empty deque")
            return None
        return self.head

    def peek_tail(self):
        if not self.tail:
            print("peek from empty deque")
            return None
        return self.tail

    def get_len(self):
        return self.len
    
    def peak_que(self,node):
        if node != self.tail:
            return node.next
        else:
            return None
    


