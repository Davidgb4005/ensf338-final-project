import sys
import os
import itertools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DataStructures.PriorityHeap import PriorityHeap


class ServiceRequest(PriorityHeap[tuple[int, int, str]]):
    """
    A service request priority queue where requests are served in order of urgency, stored in a min heap.
    Inherits from PriorityHeap class, as it implements much of its functionality.
    . . .
    Attributes:
        tree : list
            The array in which data objects of the heap is stored. Each item is a tuple with a priority int, itertools counter, and description string.
    Methods:
        addRequest(priority: int, desc: str): Method to enqueue service requests. Uses the heapPush from PriorityQueue to do it. Priority is an integer, between 1-3, with lower int values being higher priority. counter is to track the order of items added. String is a description of the service request.
        popRequest() -> str | None: Implements heapPop in order to return a description of current highest priority request.
        showRequests() -> list: Returns shallow copy of the list of requests in queue.
    """

    def __init__(self) -> None:
        """
        Initializes an object, creating an empty list that will be used as the min heap.
        Uses super init in order to inherit the __init__ method of the PriorityHeap class.
        """
        super().__init__()
        self.counter = itertools.count()

    def addRequest(self, priority, desc, building=None, service=None):
        """
        Enqueues a request into the service queue priority heap. Each request is a tuple,
        with the first field being an int that represents the priority value of the request,
        and second field a string of a description of the request.
        Sorts the item in the heap by comparing the priority values of each object. 
        If priority values are equal, then counter value is compared to prioritize older requests.

        Args:
            priority (int): Priority level of the request to add. 1 = Emergency, 2 = Standard, 3 = Low.
            desc (str): A description of the campus service to be added to the queue.
        """
        if priority < 1 or priority > 3:
            print("Priority Error")
            return None
        if desc == None or desc == "":
            print("Description Error")
            return None

        item = {
            "priority": priority,
            "order": next(self.counter),
            "description": desc,
            "building": building,
            "service": service
        }
        self.heapPush((priority, item["order"], item))
        
    def popRequest(self):
        """
        Method to return current highest priority request.
        Returns a string with a description of the current highest priority.
        Does NOT return priority level.
        """
        if self.isEmpty():
            return None
        request = self.heapPop()
        if request == None:
            return None
        return request[2]

    def peakRequest(self):
        if self.isEmpty():
            return None
        return self.tree[0][2]
    
    def showRequests(self):
        """
        Returns a copy of the list of service requests in the queue currently.
        """
        values = []
        for i in self.tree:
            values.append(i[2])
        return values
