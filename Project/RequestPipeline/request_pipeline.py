
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk 
from DataStructures import Deque as dq
import threading
import time
from typing import TypeVar, Generic, Optional, Callable, Any
T = TypeVar("T")

#what is self.auto_service ?

class request_lambda_wrapper(Generic[T]):
    """
    A class that stores the individual data of a queued request. 
    . . .
    Attributes
    ----------
    position: int
        The order of the request in the buffer.
    function: Optional[Callable[[], Any]]
        A callable function to handle request processing. Defaults to None if no argument given.
    refresh: Optional[Callable[[], Any]]
        post-execution function to call once a request has finished processing. Defaults to None if no argument given.
    request_data: T
        The information of the request itself and describes the request.
    """
    def __init__(self, position: int, request_data: T, function: Optional[Callable[[], Any]] = None, refresh: Optional[Callable[[], Any]] = None) -> None:
        """
        Initializes an object of the class, each object being one specific task that will later 
        be used by the request_pipeline class to enqueue into it's request buffer queue.
        """
        self.position = position
        self.function = function
        self.refresh = refresh
        self.request_data = request_data


class request_pipeline(Generic[T]):
    """
    A class that holds the pipeline of requests, and manages the flow ot requests with a queue.
    . . .
    Attributes
    ----------
    buffer: Deque[request_lambda_wrapper]
        The queue that stores all the requests.
    position_index: int
        Internal tracker for the number of items queued, assigning each sequential request with +1 position to the previous request.
    auto_service: int
        ?Placeholder attribute?
    
    Methods
    -------
    enque_request(function: function, refresh: function, request_data: T)
        Method that takes the details of a request as it's arguments, and then enqueues it into self.buffer
    deque_request()
        Method that dequeues the oldest request in the queue, then calls a request processing function, then a post-processing function is called.
    refresh_closure(function: function, refresh: function)
        Helper function to perform a request's function and refresh operations without dequeuing.
    """
    def __init__(self) -> None:
        """
        Initializes request pipeline, creating the buffer queue, and setting initial position index to 1.
        """
        self.buffer: dq.Deque[request_lambda_wrapper[T]] = dq.Deque()
        self.position_index = 1
        self.auto_service = 0 
    
    def enque_request(self, function: Optional[Callable[[], Any]], refresh: Optional[Callable[[], Any]], request_data: T) -> None:
        """
        Function to enqueue a request into the pipeline. Each subsequent request has it's position index + 1 to track the age of each request.

        Args
        ----
        function: Optional[Callable[[], Any]]
            The callable function to be performed upon request processing. Can optionally be None.
        refresh: Optional[Callable[[], Any]]
            The callable function to be performed after processing a request. Can optionally be None.
        request_data: T
            The details of the request itself.
        """
        new_lambda: request_lambda_wrapper[T] = request_lambda_wrapper(self.position_index, request_data, function, refresh)
        self.position_index += 1
        self.buffer.append_tail(new_lambda)

    def deque_request(self): #This should have a return type of current_request, yea?
        """
        Dequeues the oldest request from the pipeline, then performs the request processing and request post-processing functions, if they exist.
        """
        current_request = self.buffer.pop_head()
        if current_request is not None:
            if current_request.function is not None:
                current_request.function()
            if current_request.refresh is not None:
                current_request.refresh()
            print(current_request.request_data)

def refresh_closure(function: Callable[[], Any], refresh: Callable[[], Any]) -> None:
    """
    Performs request processing and post-processing functions without the need to dequeue a request.
    """
    function()
    refresh()
