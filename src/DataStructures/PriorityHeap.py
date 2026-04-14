import sys
import os
from typing import TypeVar, Iterable, Generic, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = TypeVar("T") #for strict type hinting

class PriorityHeap(Generic[T]):
    """
    A class that implements a min heap, and can be used as a priority queue.
    . . .
    Attributes
    -----------
    tree : list
        The array in which data objects of the heap is stored
    Methods
    --------
    _sort_down(index: int)
        Sorts specific item in the list into it's correct position to maintain min heap property.
    heapify(arr: list)
        Alternative method to instantiate an object of the class by providing an existing list of items.
    heapPush(item)
        Enqueues item into heap, and checks position of the item relative to it's parents, 
        moving the position of it to the appropriate spot to maintain min-heap property.
    heapPop()
        Dequeues item from first position of heap, then new head value is compared to it's children values,
        ensuring heap remains proper.
    isEmpty()
        Returns True if heap contains no values, otherwise returns False.
    """
    def __init__(self, data: Optional[Iterable[T]] = None) -> None:
        """
        Initializes a PriorityHeap object, creating an empty list initially.
        Optional 'data' arg to immediately enqueue items into the heap from, for example, a list or tuple. Individual objects work as well.
        """
        self.tree: list[T] = [] 
        if data:
            for x in data:
                self.heapPush(x)

    def _sort_down(self, index: int) -> None:
        """
        Private class method that finds the correct position of an item in the heap of the array.
        Checks the child value of the item, and then swap posititions if child is smaller.
        Repeats recursively until object is in the correct spot.

        Args:
            index(int): Position of the item to be sorted.
        """
        n = len(self.tree)
        current = index
        leftChildIndex = 2*index + 1
        rightChildIndex = 2*index + 2
        if leftChildIndex < n and self.tree[leftChildIndex] < self.tree[current]: # type: ignore
            current = leftChildIndex
        if rightChildIndex < n and self.tree[rightChildIndex] < self.tree[current]: # type: ignore
            current = rightChildIndex
        if current != index:
            self.tree[index], self.tree[current] = self.tree[current], self.tree[index]
            self._sort_down(current)

    def heapify(self, arr: list[T]) -> None:
        """
        Gets an array and copies it to the object's tree, then sorts each value to correct position in heap.

        Args:
            arr (list): Array to be copied over.
        """
        self.tree = arr
        for i in range(len(self.tree)//2 - 1, -1, -1):
            self._sort_down(i)
    
    def heapPush(self, item: T) -> None:
        '''
        Enqueues an item into the min heap, and ensures heap property remains by constantly
        checking parent values until the item is in the correct position of heap.
        
        Args:
            item: Object to be added to heap.
        '''
        self.tree.append(item)
        itemIndex = len(self.tree) - 1
        while itemIndex > 0:
            parentIndex = (itemIndex-1)//2
            if self.tree[itemIndex] < self.tree[parentIndex]:
                self.tree[itemIndex], self.tree[parentIndex] = self.tree[parentIndex], self.tree[itemIndex]
                itemIndex = parentIndex
            else:
                return None

    def heapPop(self) -> None | T:
        """
        Checks if heap is empty, returning none. If not empty, then pops and returns the value at top
        of heap, and sorts the heap from the new root, if necessary.
        """
        if not self.tree: # empty tree check
            return None
        if len(self.tree) == 1: #if only 1 element no need to do anything else
            return self.tree.pop()
        dequeued_val = self.tree[0]
        self.tree[0] = self.tree.pop()
        self._sort_down(0)
        return dequeued_val
    
    def isEmpty(self) -> bool:
        """
        Simple method that always returns False, unless there are no values in the heap, in which case it returns True.
        """
        return len(self.tree) == 0
