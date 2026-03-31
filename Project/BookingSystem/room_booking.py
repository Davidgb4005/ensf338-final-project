import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import tkinter as tk
from tkinter import ttk
import random as rd
import DataStructures.LifoRingBuffer as lifo
import RequestPipeline.request_pipeline as rp

single_block = False
rp.start_thread()
def time_str_to_float(t):
    h, m = map(int, t.split(":"))
    return h + m / 60  # 12:30 → 12.5, 13:00 → 13.0

class BookingSystem:
    def __init__(self):
        self.daily_bookings = lifo.LifoRingBuffer(90,DailyBooking) #90 day capacity

class HourlyBooking:
    def __init__(self,start_time,end_time,booker_name = "None",booking_type="Vacant"):
        self.start_time = start_time
        self.end_time =end_time
        self.booker_name = booker_name
        self.booking_type = booking_type

class DailyBooking:
    def __init__(self):
        self.hourly_bookings = []
        for i in range(48): # 24/48 gives half hour incrmeents
            self.hourly_bookings.append(HourlyBooking(i*0.5,(i*0.5)+0.5,rd.randint(0,10)))

def build_hourly_booking_gui(root, descriptor ,bookings:DailyBooking):

    def refresh():
        for row in tree.get_children():
            tree.delete(row)

        for b in bookings.hourly_bookings:
            tree.insert(
                "", "end",
                values=(b.start_time, b.end_time, b.booker_name, b.booking_type)
            )
    def delete_booking():
        current_item = tree.focus()
        print((int)((float)(tree.item(current_item)['values'][0])*2))
        bookings.hourly_bookings[(int)((float)(tree.item(current_item)['values'][0])*2)].booker_name = "None"
        bookings.hourly_bookings[(int)((float)(tree.item(current_item)['values'][0])*2)].booking_type = "Vacant"
        print(tree.item(current_item))
        refresh()
            
    def delete_booking():
        def delete_booking_closure(booking):
            booking.booker_name = "None"
            booking.booking_type = "Vacant"
        current_item = tree.focus()
        print((int)((float)(tree.item(current_item)['values'][0])*2))
        booking = bookings.hourly_bookings[(int)((float)(tree.item(current_item)['values'][0])*2)]
        print(tree.item(current_item))
        if rp.get_request_pipeline().auto_service == 1:
            delete_booking_closure(booking)
            refresh()
        else:
            rp.get_request_pipeline().enque_request(lambda:rp.refresh_closure(delete_booking_closure(booking),refresh()),f"Delete Booking {tree.item(current_item)['values'][0]} : {tree.item(current_item)['values'][1]} - User :{tree.item(current_item)['values'][2]}")

    # --- STYLE ---
    style = ttk.Style()
    style.configure("Treeview", rowheight=40)
    root.title(descriptor)
    # --- BUTTON ROW ---
    btn_row = tk.Frame(root)
    btn_row.pack(fill="x", padx=12, pady=(0, 8))

    tk.Button(btn_row, text="Delete Booking", command=delete_booking).pack(side="left")
    tk.Button(btn_row, text="Add Booking", command=refresh).pack(side="left")
    tk.Button(btn_row, text="Toggle Single Block", command=rp.open_request_pipeline_window).pack(side="left")
    feedback = tk.Label(btn_row, text="")
    feedback.pack(side="left", padx=10)

    # --- TABLE ---
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 10))

    cols = ("Start Time", "End Time", "Booker", "Status")

    tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        selectmode="browse"
    )

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    refresh()



root = tk.Tk()
build_hourly_booking_gui(root,"ensf 14324",DailyBooking())
root.mainloop()
