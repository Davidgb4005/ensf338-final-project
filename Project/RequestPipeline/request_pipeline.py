
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


def build(self,rp:request_pipeline):
    global global_refresh

    def execute_request(tk,rp):
        rp.deque_request()
        refresh(tk)

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        temp_node = rp.buffer.head
        for i in range(rp.buffer.get_len()):
            self.tree.insert("", "end", values=(temp_node.val.position,temp_node.val.function,temp_node.val.request_data))            
            temp_node = rp.buffer.peak_que(temp_node)
    global_refresh = lambda:refresh(self)
    style = ttk.Style()
    style.configure("Treeview", rowheight=40)  # pixels
    btn_row = tk.Frame(self)
    btn_row.pack(fill="x", padx=12, pady=(0, 8))
    tk.Button(btn_row, text="Process Next", command=lambda:execute_request(self,rp)).pack(side="left")
    tk.Button(btn_row, text="Refresh", command=lambda:refresh(self)).pack(side="left", padx=(8, 0))
    tk.Button(btn_row, text="Toggle Single Block", command=rp.toggle_single_block).pack(side="left", padx=(8, 0))
    self.feedback = tk.Label(btn_row, text="")
    self.feedback.pack(side="left", padx=10)

    table_frame = tk.Frame(self)
    table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

    self.tree = ttk.Treeview(table_frame, columns=("Position", "Function","Description"),
                                show="headings", selectmode="browse")
    self.tree.heading("Position", text="Position")
    self.tree.heading("Function", text="Function")
    self.tree.heading("Description", text="Description")
    self.tree.column("Position", width=60, anchor="center")
    self.tree.column("Function", width=100, anchor="center")
    self.tree.column("Description", width=100, anchor="center")

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
    self.tree.configure(yscrollcommand=vsb.set)
    self.tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    refresh(self)



def on_close(root):
    global global_refresh
    global_refresh = None
    root.destroy()   # properly shuts down the app

def open_request_pipeline_window():
    root = tk.Tk()


    root.protocol("WM_DELETE_WINDOW", lambda:on_close(root))

    build(root,rp)
    root.mainloop()

