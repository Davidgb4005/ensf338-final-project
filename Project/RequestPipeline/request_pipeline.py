
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk 
from DataStructures import Deque as dq
import threading
import time
class request_lambda_wrapper:
    def __init__(self ,position,function ,request_data):
        self.position = position
        self.function = function
        self.request_data = request_data


class request_pipeline:
    def __init__(self):
        self.buffer = dq.Deque()
        self.position_index = 1
        self.auto_service = 0 
    
    def enque_request(self,function,request_data):
        new_lambda = request_lambda_wrapper(self.position_index,function,request_data)
        self.position_index += 1
        self.buffer.append_tail(new_lambda)

    def toggle_single_block(self):
        self.auto_service = (self.auto_service + 1) % 3
        match self.auto_service:
            case 1:
                print("Request Pipeline in Auto")
            case 0:
                print("Request Pipeline in Slow Mode")
            case 2:
                print("Request Pipeline in Disabled")
    def deque_request(self):
        current_requet = self.buffer.pop_head()
        if current_requet != None:
            current_requet.function()
            print(current_requet.request_data)

pipeline_init = False
thread_handle = threading.Event()
global_refresh = None
rp = request_pipeline()
def get_request_pipeline():
    global pipeline_init,rp
    if pipeline_init == False:
        pipeline_init = True
    return rp

def auto_handle_request():
    global thread_handle,global_refresh
    rp = get_request_pipeline()
    prev_len = 0
    while not thread_handle.is_set():
        if rp.auto_service == 1 and rp.buffer.get_len()>0:
            rp.deque_request()
        elif rp.auto_service == 0:
            rp.deque_request()
            if global_refresh != None:
                global_refresh()
            time.sleep(2)
        else:
            if global_refresh != None and rp.buffer.get_len() != prev_len:
                prev_len = rp.buffer.get_len()
                global_refresh()




def refresh_closure(fn,refresh):
    if fn != None:
        fn()
    if refresh != None and (rp.toggle_single_block() != 1 or rp.buffer.get_len()==0):
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

def start_thread():
    thread_handle.clear()
    t = threading.Thread(target=lambda:auto_handle_request())
    t.start()

def kill_pipeline_thread():
    global thread_handle
    print("Killing pipelineThread")
    thread_handle.set()

if __name__ == "__main__":

    rp = get_request_pipeline()
    rp.start_request_pipeline()
    open_request_pipeline_window()