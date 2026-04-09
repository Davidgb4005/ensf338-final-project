
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk 
from DataStructures import Deque as dq
import threading
import time
class request_lambda_wrapper:
    def __init__(self ,position,function,refresh ,request_data):
        self.position = position
        self.function = function
        self.refresh = refresh
        self.request_data = request_data


class request_pipeline:
    def __init__(self):
        self.buffer = dq.Deque()
        self.position_index = 1
        self.auto_service = 0 
    
    def enque_request(self,function,refresh,request_data):
        new_lambda = request_lambda_wrapper(self.position_index,function,refresh,request_data)
        self.position_index += 1
        self.buffer.append_tail(new_lambda)

    def deque_request(self):
        current_requet = self.buffer.pop_head()
        if current_requet.function != None:
            current_requet.function()
        if current_requet.refresh() != None:
            current_requet.refresh()
        print(current_requet.request_data)







def refresh_closure(fn,refresh):
        fn()
        refresh()
