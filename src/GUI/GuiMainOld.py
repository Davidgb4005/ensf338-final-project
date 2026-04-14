
import tkinter as tk
import numpy as np
from tkinter import ttk
import tkinter.messagebox as mb
from datetime import date
from datetime import datetime

from pathlib import Path                   

PROJECT_ROOT = Path(__file__).resolve().parent.parent
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import GlobalObjects.objects as obj
import RequestPipeline.request_pipeline as rp
import NavigationSystem.traversal as tv
import BookingSystem.room_booking as rb

root = tk.Tk()
root.geometry("600x400")



MAP_PATH = PROJECT_ROOT / "GUI" / "img" / "UCalgary-Main_Campus_Map-20230724.png"
# --- Pages ---
pages = {}
current_page = None
times = []


# Global Objects campus rooms building etc
single_block_modes = ["Auto","Demo","Manual"]
request_pipeline = rp.request_pipeline()
single_block = "Auto"
campus = obj.Campus()




def helper_build_times(total_increments):
    times = []
    splits = 24/total_increments
    for i in range(total_increments):
        miniutes = 0
        hours = i * splits
        if hours != 0:
            miniutes = (hours*60) % 60
        hours = np.floor(i * splits)
        times.append(f"{int(hours):02d}:{(int)(miniutes):02d}")
    print(times)
    return(times)
times = helper_build_times(48)



def time_str_to_float(t):
    h, m = map(int, t.split(":"))
    return h + m / 60  # 12:30 → 12.5, 13:00 → 13.0

def time_str_to_index(t):
    h, m = map(int, t.split(":"))
    return int((h + m / 60) * (len(times)/24)) # 12:30 → 12.5, 13:00 → 13.0

def build_booking_page(parent):
    global times,campus
    page = tk.Frame(parent)
    end_times = []
    # --- Dropdowns ---
    dd_frame = tk.Frame(page)
    dd_frame.pack(side="top", fill="x")

    
    def refresh_floor_dd(*args):
        print("REFRESH")
        floor_var.set("Floor")
        room_var.set("Room")
        selected_building = building_var.get()


        new_floors = [f.id for f in campus.get_floors(selected_building)]
        menu = floor_dd["menu"]
        menu.delete(0, "end")
        for item in new_floors:
            menu.add_command(label=item, command=lambda v=item: floor_var.set(v))
        

    def refresh_room_dd(*args):
        print("REFRESH")
        room_var.set("Room")
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        menu = room_dd["menu"]
        menu.delete(0, "end")
            
        if selected_floor != "Floor":
            new_rooms = [r.id for r in campus.get_rooms(selected_building,selected_floor)]
            for item in new_rooms:
                menu.add_command(label=item, command=lambda v=item: room_var.set(v))

    def refresh_date(*args):
        print(date_var_entry.get())
        today = today = datetime.today()
        try:
            selected_date = datetime.strptime(date_var_entry.get(), "%Y/%m/%d");
        except ValueError:
            mb.showinfo("Date Error", f"Incorrect Date Format - YYYY/MM/DD")
            return
        delta = selected_date - today
        if delta.days < -1:
            mb.showinfo("Date Error", f"Dates Have Cannot Be In The Past")
            return None
        if delta.days > 90:
            mb.showinfo("Date Error", f"Dates Have Cannot Be More Than 90 Days In The Future")
            return None
        return delta.days

    def refresh_table(*args):
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        selected_room = room_var.get()
        selected_start = start_var.get()
        selected_end = end_var.get()
        selected_day = refresh_date()
        if selected_day == None:
            return
        if (end_var.get() == "End Time"):
            selected_end = 47
        else:
            selected_end = time_str_to_index(end_var.get())
        if (start_var.get() == "Start Time"):
            selected_start = 0
        else:
            selected_start = time_str_to_index(start_var.get())

        table.delete(*table.get_children())
        if campus.get_bookings(selected_building,selected_floor,selected_room,selected_day,selected_start,selected_end) == None:
            mb.showinfo("Display Error","Room Is Deleted, Reinitizle in edit page")
            return
        for booking in campus.get_bookings(selected_building,selected_floor,selected_room,selected_day,selected_start,selected_end):
            table.insert("", "end", values=(booking.booking_type, booking.booker_name, booking.start_time, booking.end_time))           

    def building_info(*args):
        selected_building = building_var.get()
        building = campus.get_buildings()[selected_building]
        mb.showinfo("Building Info", building.get_info())
    def room_info(*args):
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        selected_room = room_var.get()
        try:
            room = campus.get_buildings()[selected_building].floors[int(selected_floor)].rooms[int(selected_room)]
            mb.showinfo("Room Info",room.get_info())
        except ValueError:
            mb.showinfo("Data Error","Please Select A Building, Floor And Room")

    building_var = tk.StringVar(value="Building")
    building_var.trace_add("write", refresh_floor_dd)
    building_dd =tk.OptionMenu(dd_frame, building_var, *campus.get_building_keys())
    building_dd.config(width=20)
    building_dd.pack(side="left")

    

    floor_var = tk.StringVar(value="Floor")
    floor_var.trace_add("write", refresh_room_dd)
    floor_dd = tk.OptionMenu(dd_frame, floor_var, [])
    floor_dd.config(width=20)
    floor_dd.pack(side="left")


    room_var = tk.StringVar(value="Room")
    room_var.trace_add("write", None)
    room_dd = tk.OptionMenu(dd_frame, room_var, [])
    room_dd.config(width=20)
    room_dd.pack(side="left")



    date_var_entry = tk.Entry(dd_frame)
    date_var_entry.insert(0,date.today().strftime("%Y/%m/%d"))
    date_var_entry.config(width=20)
    date_var_entry.pack(side="left")


    start_var = tk.StringVar(value="Start Time")
    start_var.trace_add("write", None)
    start_time_dd = tk.OptionMenu(dd_frame, start_var, *times)
    start_time_dd.config(width=20)
    start_time_dd.pack(side="left")


    end_var = tk.StringVar(value="End Time")
    end_var.trace_add("write", None)
    end_time_dd = tk.OptionMenu(dd_frame, end_var, *times)
    end_time_dd.config(width=20)
    end_time_dd.pack(side="left")


    tk.Button(dd_frame, text="Submit", command=refresh_table).pack(side="left")

    tk.Button(dd_frame, text="Room Info", command=room_info).pack(side="left")
    tk.Button(dd_frame, text="Building Info", command=building_info).pack(side="left")

  
    # --- Table ---
    cols = ("Booked For", "Booked By", "Start Time", "End Time")
    table = ttk.Treeview(page, columns=cols, show="headings")
    for col in cols:
        table.heading(col, text=col)
        table.column(col, width=100)
    table.pack(fill="both", expand=True)

    def add_booking():
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        selected_room = room_var.get()
        selected_start = start_var.get()
        selected_end = end_var.get()
        selected_day = refresh_date()
        if selected_day == None:
            return



        selected = table.focus()
        vals = table.item(selected,"values")
        if not(selected):
            mb.showinfo("Booking Error", f"Please Select A Valid Time Slot")
            return
        if vals[0] != "Vacant":
            mb.showinfo("Booking Error", f"Room Is Already Booked For {vals[2]} - {vals[3]}")
            return
        
        def open_popup():
            popup = tk.Toplevel()
            
            tk.Label(popup, text="Name").pack()
            entry1 = tk.Entry(popup)
            entry1.pack()

            tk.Label(popup, text="Booking Type").pack()
            entry2 = tk.Entry(popup)
            entry2.pack()
            values = [None]*2
            def submit():
                values[0] = entry1.get() 
                values[1] = entry2.get()
                popup.destroy()

            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values

        values = open_popup()
        if values[0] == "" or values[1] == "" or values[0] == None or values[1] == None:
            mb.showinfo("Booking Error", f"Please Insert A Name And Booking Type")
            return
        booking = campus.get_bookings(selected_building,selected_floor,selected_room,selected_day,time_str_to_index(vals[2]),time_str_to_index(vals[3]))[0]
        request_pipeline.enque_request(lambda:booking.update_booking(values[0],values[1]),lambda:refresh_table(),"Add Booking")
        print("Add:", vals)

    def delete_booking():
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        selected_room = room_var.get()
        selected_start = start_var.get()
        selected_end = end_var.get()
        selected_day = refresh_date()
        selected = table.focus()
        if not(selected):
            mb.showinfo("Booking Error", f"Please Select A Valid Time Slot")
            return
        vals = table.item(selected,"values")
        if vals[0] == "Vacant":
            mb.showinfo("Booking Error", f"Room Has No Booking For {vals[2]} - {vals[3]}")
            return
        if selected:
            vals = table.item(selected, "values")
            print("Delete:", vals)
        booking = campus.get_bookings(selected_building,selected_floor,selected_room,selected_day,time_str_to_index(vals[2]),time_str_to_index(vals[3]))[0]
        request_pipeline.enque_request(lambda:booking.update_booking(None,"Vacant"),lambda:refresh_table(),"Add Booking")

        

    def add_service():
        selected_building = building_var.get()
        if selected_building == "Building" or selected_building == None :
            mb.showinfo("Booking Error", f"Please Select A Building")
            return
        
        def open_popup():
            popup = tk.Toplevel()
            
            tk.Label(popup, text="Service Name").pack()
            entry1 = tk.Entry(popup)
            entry1.pack()

            values = [None]*2
            def submit():
                values[0] = entry1.get() 
                popup.destroy()

            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values

        values = open_popup()
        if values[0] == "" or values[0] == None :
            mb.showinfo("Booking Error", f"Please Insert A Name And Booking Type")
            return
        campus.add_serivce(values[0],selected_building)
        #func = lambda:campus.add_serivce(values[0],selected_building)
        #request_pipeline.enque_request(func,lambda:refresh_table(),"Add Service")
        print("Add:", values[0])

    def delete_service():
        selected_building = building_var.get()
        if selected_building == "Building" or selected_building == None :
            mb.showinfo("Booking Error", f"Please Select A Building")
            return
        
        def open_popup():
            popup = tk.Toplevel()
            
            tk.Label(popup, text="Service Name").pack()
            entry1 = tk.Entry(popup)
            entry1.pack()

            values = [None]*2
            def submit():
                values[0] = entry1.get() 
                popup.destroy()

            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values

        values = open_popup()
        if values[0] == "" or values[0] == None :
            mb.showinfo("Service Error", f"Please Insert Service Name")
            return
        campus.delete_service(values[0],selected_building)
        #func = lambda:campus.delete_service(values[0],selected_building)
        #request_pipeline.enque_request(func,lambda:refresh_table(),"Delete Service")
        print("Delete Service:", values[0])


    def add_service():
        selected_building = building_var.get()
        if selected_building == "Building" or selected_building == None :
            mb.showinfo("Booking Error", f"Please Select A Building")
            return
        
        def open_popup():
            popup = tk.Toplevel()
            
            tk.Label(popup, text="Service Name").pack()
            entry1 = tk.Entry(popup)
            entry1.pack()

            values = [None]*2
            def submit():
                values[0] = entry1.get() 
                popup.destroy()

            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values

        values = open_popup()
        if values[0] == "" or values[0] == None :
            mb.showinfo("Booking Error", f"Please Insert A Name And Booking Type")
            return
        campus.add_serivce(values[0],selected_building)
        #func = lambda:campus.add_serivce(values[0],selected_building)
        #request_pipeline.enque_request(func,lambda:refresh_table(),"Add Service")
        print("Add:", values[0])

    def delete_service():
        selected_building = building_var.get()
        if selected_building == "Building" or selected_building == None :
            mb.showinfo("Booking Error", f"Please Select A Building")
            return
        
        def open_popup():
            popup = tk.Toplevel()
            
            tk.Label(popup, text="Service Name").pack()
            entry1 = tk.Entry(popup)
            entry1.pack()

            values = [None]*1
            def submit():
                values[0] = entry1.get() 
                popup.destroy()

            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values

        values = open_popup()
        if values[0] == "" or values[0] == None :
            mb.showinfo("Service Error", f"Please Insert Service Name")
            return
        campus.delete_service(values[0],selected_building)
        #func = lambda:campus.delete_service(values[0],selected_building)
        #request_pipeline.enque_request(func,lambda:refresh_table(),"Delete Service")
        print("Delete Service:", values[0])

    def add_building():

        def open_popup():
            popup = tk.Toplevel()
            
            tk.Label(popup, text="Building Name(Eg: Eng A Block)").pack()
            entry1 = tk.Entry(popup)
            entry1.pack()
            tk.Label(popup, text="Building Id(Eg: ENA)").pack()
            entry2 = tk.Entry(popup)
            entry2.pack()
            tk.Label(popup, text="Floors").pack()
            entry3 = tk.Entry(popup)
            entry3.pack()
            tk.Label(popup, text="Rooms Per Floor").pack()
            entry4 = tk.Entry(popup)
            entry4.pack()


            values = [None]*4
        
            def submit():
                values[0] = entry1.get() 
                values[1] = entry2.get() 
                values[2] = entry3.get() 
                values[3] = entry4.get() 
                popup.destroy()
                    
            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values
                
        values = open_popup()
        for  i in values:
            if i == None or i == "":
                mb.showinfo("Add Building Error", f"Please Fill in all Fields")
        new_building = obj.Building(values[0],values[1],obj.Location(0,0))
        campus.add_building(int(values[2]),int(values[3]),new_building)
        generate_pages()
        show_room_booking()
        return values
        
    def delete_building():
       
        selected_building = building_var.get()
        deleted_building = campus.get_buildings()[selected_building]
        campus.remove_building(deleted_building)
        #func = lambda:campus.delete_service(values[0],selected_building)
        #request_pipeline.enque_request(func,lambda:refresh_table(),"Delete Service")
        print("deleted building:", deleted_building)
        generate_pages()
        show_room_booking()



    def append_room():
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        if selected_floor == "Floor" or selected_building == "Building":
            mb.showinfo("Add Room Error, Please Select Floor and Building")
            return
        def open_popup():
            popup = tk.Toplevel()
            

            tk.Label(popup, text="Info").pack()
            entry2 = tk.Entry(popup)
            entry2.pack()
            tk.Label(popup, text="Type").pack()
            entry3 = tk.Entry(popup)
            entry3.pack()



            values = [None]*2
        
            def submit(): 
                values[0] = entry2.get() 
                values[1] = entry3.get() 
                popup.destroy()
                    
            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values
                
        values = open_popup()
        for  i in values:
            if i == None or i == "":
                mb.showinfo("Add Room Error", f"Please Fill in all Fields")
                return
        id = len(campus.get_buildings()[selected_building].floors[int(selected_floor)].rooms)
        new_room = obj.Room(id,values[1])
        new_room.info = values[0]
        campus.get_buildings()[selected_building].floors[int(selected_floor)].rooms.append(new_room)
        refresh_room_dd()
        return values
        
    def delete_room():
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        selected_room = room_var.get()
        deleted_room = campus.get_buildings()[selected_building].floors[int(selected_floor)].rooms[int(selected_room)]

        deleted_room.booking = None
        deleted_room.room_type = None
        deleted_room.room_type = None
        #func = lambda:campus.delete_service(values[0],selected_building)
        #request_pipeline.enque_request(func,lambda:refresh_table(),"Delete Service")
        print("Delete Room:", deleted_room)
        refresh_room_dd()

    def edit_room():
        selected_building = building_var.get()
        selected_floor = floor_var.get()
        if selected_floor == "Floor" or selected_building == "Building":
            mb.showinfo("Add Room Error, Please Select Floor and Building")
            return
        def open_popup():
            popup = tk.Toplevel()
            room = campus.get_buildings()[selected_building].floors[int(selected_floor)].rooms[int(room_var.get())]
            
            tk.Label(popup, text="Info").pack()
            entry2 = tk.Entry(popup)
            if room.info != None:
                entry2.insert(0, room.info)
            entry2.pack()
            
            tk.Label(popup, text="Type").pack()
            entry3 = tk.Entry(popup)
            if room.room_type != None:
                entry3.insert(0, room.room_type)
            entry3.pack()
            
            tk.Label(popup, text="Reinitialize Room Bookings").pack()
            reinit_var = tk.BooleanVar(value=False)        
            cb = tk.Checkbutton(popup, variable=reinit_var)  
            cb.pack()
            
            values = [None] * 3

            def submit():
                values[0] = entry2.get()
                values[1] = entry3.get()
                values[2] = reinit_var.get()  # ← was values[3], out of range on a size-3 list
                popup.destroy()

            tk.Button(popup, text="Submit", command=submit).pack()
            popup.wait_window()
            return values
                
        values = open_popup()
        for  i in values:
            if i == None or i == "":
                mb.showinfo("Add Room Error", f"Please Fill in all Fields")
                return

        room = campus.get_buildings()[selected_building].floors[int(selected_floor)].rooms[int(room_var.get())]
        room.room_type = values[1]
        room.info = values[0]
        if values[2]:
            room.booking = rb.BookingSystem(90)
        refresh_room_dd()
        refresh_table()
        return values

    btn_frame = tk.Frame(page)
    btn_frame.pack(fill="x")
    tk.Button(btn_frame, text="Add Booking", command=add_booking).pack(side="left")
    tk.Button(btn_frame, text="Delete Booking", command=delete_booking).pack(side="left")
    tk.Button(btn_frame, text="Add Service", command=add_service).pack(side="left")
    tk.Button(btn_frame, text="Delete Service", command=delete_service).pack(side="left")
    tk.Button(btn_frame, text="Add Room", command=append_room).pack(side="left")
    tk.Button(btn_frame, text="Edit Room", command=edit_room).pack(side="left")
    tk.Button(btn_frame, text="Delete Room", command=delete_room).pack(side="left")
    tk.Button(btn_frame, text="Add Building", command=add_building).pack(side="left")
    tk.Button(btn_frame, text="Delete Building", command=delete_building).pack(side="left")
    return page


def build_nav_page(parent):
    page = tk.Frame(parent)
 
    # --- Dropdowns ---
    dd_frame = tk.Frame(page)
    dd_frame.pack(side="top", fill="x")
 
    start_var = tk.StringVar(value="Start Location")
    start_dd = tk.OptionMenu(dd_frame, start_var, *campus.get_building_keys())
    start_dd.config(width=20)
    start_dd.pack(side="left")

    end_var = tk.StringVar(value="End Location")
    end_dd = tk.OptionMenu(dd_frame, end_var, *campus.get_building_keys())
    end_dd.config(width=20)
    end_dd.pack(side="left")


    def submit():
        if campus.campus_graph.get_node_id(start_var.get()) == campus.campus_graph.get_node_id(end_var.get()):
            mb.showinfo("Navigation Error", f"Start and End cannot be same place")
            return
        path = campus.campus_graph.find_path(campus.campus_graph.get_node_id(start_var.get()),campus.campus_graph.get_node_id(end_var.get()))
        closure = lambda:tv.draw_graph(path,"Project\\GUI\\img\\UCalgary-Main_Campus_Map-20230724.png")
        undo_closure = lambda : campus.campus_graph.undo_buffer.append(closure)
        request_pipeline.enque_request(closure,lambda:None,"Navigation Rendering")
        request_pipeline.enque_request(undo_closure,lambda:None,"Navigation Undo Enqueing")


    def undo():
        undo_closure = lambda : campus.campus_graph.undo()
        request_pipeline.enque_request(undo_closure,lambda:None,"Navigation Undo DeQueing")
        
    def animate():


        if campus.campus_graph.get_node_id(start_var.get()) == campus.campus_graph.get_node_id(end_var.get()):
            mb.showinfo("Navigation Error", f"Start and End cannot be same place")
            return
        path,steps = campus.campus_graph.find_path_steps(campus.campus_graph.get_node_id(start_var.get()),campus.campus_graph.get_node_id(end_var.get()))
        closure = tv.animate_search(campus.campus_graph.nodes, steps, "Project\\GUI\\img\\UCalgary-Main_Campus_Map-20230724.png")
        undo_closure = lambda : campus.campus_graph.undo_buffer.append(closure)
        request_pipeline.enque_request(closure,lambda:None,"Navigation Rendering")
        request_pipeline.enque_request(undo_closure,lambda:None,"Navigation Undo Enqueing")

    tk.Button(dd_frame, text="Submit", command=submit).pack(side="left")
    tk.Button(dd_frame, text="Animate", command=animate).pack(side="left")
    tk.Button(dd_frame, text="Undo", command=undo).pack(side="left")


    photo = tk.PhotoImage(file=MAP_PATH)
    img_label = tk.Label(page, image=photo)
    img_label.image = photo
    img_label.pack(pady=10)
    return page


def build_request_processing_page(parent):
    page = tk.Frame(parent)
 
    dd_frame = tk.Frame(page)
    dd_frame.pack(side="top", fill="x")

    cols = ("Request Id", "Function Handle","Refresh Handle", "Description")
    table = ttk.Treeview(page, columns=cols, show="headings")
    for col in cols:
        table.heading(col, text=col)
        table.column(col, width=100)
    table.pack(fill="both", expand=True)

    def process_next():
        request_pipeline.deque_request()
        refresh_table()

    def refresh():
        refresh_table()

    def refresh_table(*args):

        table.delete(*table.get_children())
        tail = request_pipeline.buffer.peek_tail()
        head = request_pipeline.buffer.peek_head()
        while tail != head:
            table.insert("", "end", values=(tail.val.position, tail.val.function, tail.val.refresh, tail.val.request_data))   
            tail = tail.prev    




    tk.Button(dd_frame, text="Process Next", command=process_next).pack(side="left")
    tk.Button(dd_frame, text="Refresh", command=refresh).pack(side="left")

    return page





def show_page(name):
    global current_page
    if current_page:
        current_page.pack_forget()
    current_page = pages[name]
    current_page.pack(fill="both", expand=True)

# --- Main frame ---
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

def generate_pages():
    global pages
    for name in ["room_booking", "service_queue", "completed_operation","bonus"]:
        p = tk.Frame(frame)
        tk.Label(p, text=name).pack()
        pages["navigation"] = build_nav_page(frame)
        pages["room_booking"] = build_booking_page(frame)
        pages["request_processing"] = build_request_processing_page(frame)
        pages[name] = p



# --- Dummy page functions ---
def show_navigation(): show_page("navigation")
def show_room_booking(): show_page("room_booking")
def show_service_queue(): show_page("service_queue")
def show_request_processing(): show_page("request_processing")
def show_competed_operation(): show_page("completed_operation")
def show_bonus(): show_page("bonus")



# --- Cyclic functions ---
def toggle_request_pipeline():
    global single_block
    match single_block:
        case "Auto":
            single_block = "Manual"
            mb.showinfo("Single Block", f"Mode is Set to Manual, No Auto Processing Of Request")
        case "Manual":
            single_block = "Demo"
            mb.showinfo("Single Block", f"Mode is Set to Demo, Auto Processing Of Request Will Happen Onces Every 5 Seconds")
        case "Demo":
            single_block = "Auto"
            mb.showinfo("Single Block", f"Mode is Set to Auto, Auto Processing Of Request Will Happen Instantly")
# --- Nav bar ---
nav = tk.Frame(root)
nav.pack(fill="x", side="bottom")

tk.Button(nav, text="Build Navigation", command=show_navigation).pack(side="left", expand=True)
tk.Button(nav, text="Room/Event Booking", command=show_room_booking).pack(side="left", expand=True)
tk.Button(nav, text="Service Queue", command=show_service_queue).pack(side="left", expand=True)
tk.Button(nav, text="Request Processing", command=show_request_processing).pack(side="left", expand=True)
tk.Button(nav, text="Completed Operation", command=show_competed_operation).pack(side="left", expand=True)
tk.Button(nav, text="Bonus", command=show_bonus).pack(side="left", expand=True)
tk.Button(nav, text="Toggle Single Block", command=toggle_request_pipeline).pack(side="left", expand=True)



def request_pipeline_caller():
    global request_pipeline,single_block

    while request_pipeline.buffer.get_len()>0 and single_block == "Auto":
        request_pipeline.deque_request()
        print("Request Pipeline Executed")

    if single_block == "Auto": 
        root.after(500, request_pipeline_caller)
    elif single_block == "Demo":
        if request_pipeline.buffer.get_len()>0:
            request_pipeline.deque_request()
            print("Request Pipeline Executed")
        root.after(5000, request_pipeline_caller)
    else:
        root.after(5000, request_pipeline_caller)
def every_5s():
    print("5s tick")
    root.after(5000, every_5s)

# --- Init ---
generate_pages()
show_page("navigation")
request_pipeline_caller()
every_5s()

root.mainloop()
