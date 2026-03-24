class Node:
    __slots__ = ('val', 'prev', 'next')
    def __init__(self, val):
        self.val = val
        self.prev = self.next = None

class Deque:
    def __init__(self):
        self._head = self._tail = None
        self._len = 0

    def append_tail(self, val):
        node = Node(val)
        if self._tail:
            self._tail.next = node
            node.prev = self._tail
            self._tail = node
        else:
            self._head = self._tail = node
        self._len += 1

    def append_head(self, val):
        node = Node(val)
        if self._head:
            node.next = self._head
            self._head.prev = node
            self._head = node
        else:
            self._head = self._tail = node
        self._len += 1

    def pop_tail(self):
        if not self._tail:
            raise IndexError("pop from empty deque")
        val = self._tail.val
        self._tail = self._tail.prev
        if self._tail:
            self._tail.next = None
        else:
            self._head = None          # list now empty
        self._len -= 1
        return val

    def pop_head(self):
        if not self._head:
            raise IndexError("pop from empty deque")
        val = self._head.val
        self._head = self._head.next
        if self._head:
            self._head.prev = None
        else:
            self._tail = None          # list now empty
        self._len -= 1
        return val

    def peek_head(self):
        if not self._head:
            raise IndexError("peek from empty deque")
        return self._head.val

    def peek_tail(self):
        if not self._tail:
            raise IndexError("peek from empty deque")
        return self._tail.val

    def get_len(self):
        return self._len

    def __bool__(self):
        return self._len > 0