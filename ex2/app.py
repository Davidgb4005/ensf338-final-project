import tkinter as tk
from tkinter import ttk
import random as rd
import main
import room_booking
import request_pipeline as rp
## Dummy Vars
building_list = {}
building_name_list = ["TFDL","ENG","ICT","SCA","SCB","SCT","MUFR","ADM","HSKYN","MAC"]
building_count = 10

room_types = ["Study","Confrense","Meeting","Lecture"]
floor_list = [] 
floor_count = 15
room_count = 40
for k in range(building_count):
    building_list[building_name_list[k]] = (main.Building(k,building_name_list[k],building_name_list[k],[0,0]))
    for j in range(floor_count):
        building_list[building_name_list[k]].floors.append(main.Floor())
        floor_list.append(main.Floor())
        for i in range(room_count):
            building_list[building_name_list[k]].floors[j].rooms.append(main.Room(rd.randint(0,30),room_types[rd.randint(0,len(room_types)-1)]))
for i in (building_list):
    print(i)
campus = main.Campus()
campus.buildings = dict(building_list)



return_val = main.room_finder(campus,4,23,building_name="ENG")
test_bookingSystem = return_val[2].bookings
print(return_val[0].name)

print(return_val[1])
print(return_val[2].bookings)
request_pipeline = rp.request_pipeline()

test_booking = room_booking.user_booking(535,"TEST", 12.5,"Dummy Comment")
test_booking1 = room_booking.user_booking(535,"TEST2", 12.5,"Dummy Comment")
test_booking2 = room_booking.user_booking(535,"TEST3", 13,"Dummy Comment")
request_pipeline.enque_function(lambda :return_val[2].bookings.book_room(3,test_booking))
request_pipeline.enque_function(lambda :return_val[2].bookings.book_room(4,test_booking1))
request_pipeline.enque_function(lambda :return_val[2].bookings.book_room(5,test_booking2))
request_pipeline.enque_function(lambda :return_val[2].bookings.print_daily_booking(3,0,15))
request_pipeline.enque_function(lambda :return_val[2].bookings.print_daily_booking(4,0,15))
request_pipeline.enque_function(lambda :return_val[2].bookings.print_daily_booking(5,0,15))

while request_pipeline.buffer.items > 0:
    request_pipeline.deque_function() 
    pass
# ── Helpers ───────────────────────────────────────────────────────────────────

def time_slots():
    slots = []
    for h in range(24):
        for m in (0, 30):
            slots.append(f"{h:02d}:{m:02d}")
    return slots


def search_rooms(building, floor, room,day, start, end):
    if floor != None:
        floor = (int)(floor)
    if room != None:
        room = (int)(room)
    day = (int)(day)
    print(building,floor,room)
    result = main.room_finder(campus,floor_number=floor,room_number=room,building_name=building)
    print(day,start,end)
    if result[2] is not None:
        result = result[2].bookings.get_daily_booking(day, start, end)
        return [2, result]
    elif result[1] is not None:
        result = result[1].rooms.copy()
        return [1, result]
    elif result[0] is not None:
        result = result[0].floors.copy()
        return [0, result]
    return None
def delete_booking(building, floor, room,day, start, end):
    if floor != None:
        floor = (int)(floor)
    if room != None:
        room = (int)(room)
    day = (int)(day)
    print(building,floor,room)
    result = main.room_finder(campus,floor_number=floor,room_number=room,building_name=building)
    print(day,start,end)
    if result[2] is not None:
        result = result[2].bookings.get_daily_booking(day, start, end)
        return [2, result]
    elif result[1] is not None:
        result = result[1].rooms.copy()
        return [1, result]
    elif result[0] is not None:
        result = result[0].floors.copy()
        return [0, result]
    return None


# ── Pages ─────────────────────────────────────────────────────────────────────

class RoomLookupPage(tk.Frame):
    
    BUILDINGS =  ["TFDL","ENG","ICT","SCA","SCB","SCT","MUFR","ADM","HSKYN","MAC"]
    TIMES     = [""] + time_slots()

    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        tk.Label(self, text="Room / Event Lookup & Book",
                 font=("Helvetica", 14, "bold")).pack(pady=(12, 8))

        form = tk.LabelFrame(self, text="Search Filters", padx=10, pady=8)
        form.pack(fill="x", padx=12, pady=(0, 8))
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)  # increase from default ~20
        tk.Label(form, text="Building Name *").grid(row=0, column=0, sticky="w", pady=3)
        self.building_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.building_var,
                     values=self.BUILDINGS, state="readonly",
                     width=20).grid(row=0, column=1, sticky="w", padx=(8, 20), pady=3)

        tk.Label(form, text="Day *").grid(row=0, column=2, sticky="w", pady=3)
        self.day_var = tk.StringVar()
        tk.Entry(form, textvariable=self.day_var,
                 width=6).grid(row=0, column=3, sticky="w", padx=(8, 0), pady=3)

        # Row 1 – Floor, Room
        tk.Label(form, text="Floor").grid(row=1, column=0, sticky="w", pady=3)
        self.floor_var = tk.StringVar()
        tk.Entry(form, textvariable=self.floor_var,
                 width=8).grid(row=1, column=1, sticky="w", padx=(8, 20), pady=3)

        tk.Label(form, text="Room").grid(row=1, column=2, sticky="w", pady=3)
        self.room_var = tk.StringVar()
        tk.Entry(form, textvariable=self.room_var,
                 width=10).grid(row=1, column=3, sticky="w", padx=(8, 0), pady=3)

        # Row 2 – Start time, End time
        tk.Label(form, text="Start Time").grid(row=2, column=0, sticky="w", pady=3)
        self.start_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.start_var,
                     values=self.TIMES, state="readonly",
                     width=8).grid(row=2, column=1, sticky="w", padx=(8, 20), pady=3)

        tk.Label(form, text="End Time").grid(row=2, column=2, sticky="w", pady=3)
        self.end_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.end_var,
                     values=self.TIMES, state="readonly",
                     width=8).grid(row=2, column=3, sticky="w", padx=(8, 0), pady=3)

        # Search button + feedback
        btn_row = tk.Frame(form)
        btn_row.grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))
        tk.Button(btn_row, text="Search", command=self._search).pack(side="left")
        self.feedback = tk.Label(btn_row, text="", fg="red")
        self.feedback.pack(side="left", padx=10)

        # Results table
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        cols = ("Building", "Floor", "Room", "Day", "Start Time", "End Time", "Status")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                 show="headings", selectmode="browse")
        widths = {"Building": 120, "Floor": 60, "Room": 80,
                  "Day": 60, "Start Time": 90, "End Time": 90, "Status": 130}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100), anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        tk.Button(self, text="Book Selected Room",
                  command=self._book_selected).pack(pady=(0, 6))
        self.book_feedback = tk.Label(self, text="")
        self.book_feedback.pack()
        tk.Button(self, text="Delete Selected Booking",
                  command=self._delete_selected).pack(pady=(0, 6))
        self.book_feedback = tk.Label(self, text="")
        self.book_feedback.pack()

    def _search(self):
        self.feedback.config(text="", fg="red")
        self.book_feedback.config(text="")

        building = self.building_var.get().strip()
        day_raw  = self.day_var.get().strip()
        floor    = self.floor_var.get().strip() or None
        room     = self.room_var.get().strip() or None
        start    = self.start_var.get().strip() or None
        end      = self.end_var.get().strip() or None

        # Validate required fields
        if building is None:
            self.feedback.config(text="Building Name is required.")
            return
        if not day_raw:
            self.feedback.config(text="Day is required.")
            return
        if not day_raw.isdigit():
            self.feedback.config(text="Day must be a whole number (e.g. 1, 2, 15).")
            return
        day = int(day_raw)


        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = search_rooms(building, floor, room, day_raw, start, end)

        if results is None:
            self.feedback.config(text="Invalid Result Contact An Adult", fg="red")
            return

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        match results[0]:
            case 2:
                bookings = results[1]
                # Update columns for booking view
                self.tree["columns"] = ("Time", "Name", "User ID", "Comments")
                for col in ("Time", "Name", "User ID", "Comments"):
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="center")

                for b in bookings:
                    if b.name == "":  # open slot from your get_daily_booking
                        self.tree.insert("", "end", values=(b.time, "Open", "", ""))
                    else:
                        self.tree.insert("", "end", values=(b.time, b.name, b.id, b.comments))

                self.feedback.config(text=f"{len(bookings)} slot(s) found.", fg="black")

            case 1:
                rooms = results[1]
                self.tree["columns"] = ("Room #", "Type", "Capacity", "Split Room")
                for col in ("Room #", "Type", "Capacity", "Split Room"):
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="center")

                for i, room in enumerate(rooms):
                    split = "Yes" if room.split_room else "No"
                    self.tree.insert("", "end", values=(i, room.room_type, room.capacity, split))

                self.feedback.config(text=f"{len(rooms)} room(s) found.", fg="black")
            case 0:
                floors = results[1]
                self.tree["columns"] = ("Floor #", "Room Count")
                for col in ("Floor #", "Room Count"):
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="center")
                for i, f in enumerate(floors):
                    self.tree.insert("", "end", values=(i, len(f.rooms)))
                self.feedback.config(text=f"{len(floors)} floor(s) found.", fg="black")

        self.feedback.config(text=f"{len(results)} room(s) found.", fg="black")

    def _book_selected(self):
        selected = self.tree.focus()
        if not selected:
            self.book_feedback.config(text="Please select a room to book.", fg="red")
            return
        vals = self.tree.item(selected, "values")
        self.book_feedback.config(text="")

        building = self.building_var.get().strip()
        day_raw  = self.day_var.get().strip()
        floor    = self.floor_var.get().strip() or None
        room     = self.room_var.get().strip() or None

        # Validate required fields
        if building is None:
            self.feedback.config(text="Building Name is required.")
            return
        if not day_raw:
            self.feedback.config(text="Day is required.")
            return
        if not floor:
            self.feedback.config(text="Floor is required.")
            return
        if not room:
            self.feedback.config(text="Room is required.")
            return
        if not day_raw.isdigit():
            self.feedback.config(text="Day must be a whole number (e.g. 1, 2, 15).")
            return
        day = int(day_raw)


        # Clear table
        print(vals)
        results = main.room_finder(campus,floor,room,building)
        temp_user_booking = room_booking.user_booking(rd.randint(0,10),"A dummy name",(float)(vals[0]),"Dummy Comments")
        result = results[2].bookings.book_room(day,temp_user_booking)
        if result == None:
            print("room Already Booked")
        self._search()

    def _delete_selected(self):
        selected = self.tree.focus()
        if not selected:
            self.book_feedback.config(text="Please select a room to book.", fg="red")
            return
        vals = self.tree.item(selected, "values")
        self.book_feedback.config(text="")

        building = self.building_var.get().strip()
        day_raw  = self.day_var.get().strip()
        floor    = self.floor_var.get().strip() or None
        room     = self.room_var.get().strip() or None

        # Validate required fields
        if building is None:
            self.feedback.config(text="Building Name is required.")
            return
        if not day_raw:
            self.feedback.config(text="Day is required.")
            return
        if not floor:
            self.feedback.config(text="Floor is required.")
            return
        if not room:
            self.feedback.config(text="Room is required.")
            return
        if not day_raw.isdigit():
            self.feedback.config(text="Day must be a whole number (e.g. 1, 2, 15).")
            return
        day = int(day_raw)


        # Clear table
        print(vals)
        results = main.room_finder(campus,floor,room,building)
        temp_user_booking = room_booking.user_booking(rd.randint(0,10),"A dummy name",(float)(vals[0]),"Dummy Comments")
        result = results[2].bookings.delete_booking(day,temp_user_booking)
        if result == None:
            print("room Already Booked")
        self._search()




class NavigationPage(tk.Frame):
    LOCATIONS = ["TFDL","ENG","ICT","SCA","SCB","SCT","MUFR","ADM","HSKYN","MAC"]

    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        tk.Label(self, text="Navigation",
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

        tk.Label(self, text="Starting Location").pack(anchor="w", padx=30)
        self.start_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.start_var, values=self.LOCATIONS,
                     state="readonly", width=35).pack(padx=30, pady=(2, 12))

        tk.Label(self, text="End Location").pack(anchor="w", padx=30)
        self.end_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.end_var, values=self.LOCATIONS,
                     state="readonly", width=35).pack(padx=30, pady=(2, 20))

        tk.Button(self, text="Submit Request", command=self._on_submit).pack()

        self.feedback = tk.Label(self, text="")
        self.feedback.pack(pady=(10, 0))

    def _on_submit(self):
        start = self.start_var.get()
        end   = self.end_var.get()
        if not start or not end:
            self.feedback.config(text="Please select both locations.")
        elif start == end:
            self.feedback.config(text="Start and end cannot be the same.")
        else:
            self.feedback.config(text=f"Route requested: {start} -> {end}")


class PlaceholderPage(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        tk.Label(self, text=title,
                 font=("Helvetica", 14, "bold")).pack(pady=(20, 10))
        tk.Label(self, text="This page is under construction.").pack()


# ── Main Application ──────────────────────────────────────────────────────────

class App(tk.Tk):
    NAV_BUTTONS = [
        "Room/Event Lookup",
        "Find Building",
        "Route History",
        "Pending Requests",
        "Service Requests",
    ]

    def __init__(self):
        super().__init__()
        self.title("Campus Navigator")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        self._pages    = {}
        self._nav_btns = {}

        self._build_shell()
        self._build_pages()
        self._show_page("Navigation")

    def _build_shell(self):
        self.container = tk.Frame(self, bd=1, relief="sunken")
        self.container.pack(fill="both", expand=True, padx=8, pady=8)

        navbar = tk.Frame(self, bd=1, relief="raised")
        navbar.pack(fill="x", side="bottom")

        home_btn = tk.Button(navbar, text="Navigation",
                             command=lambda: self._show_page("Navigation"))
        home_btn.grid(row=0, column=0, sticky="nsew", padx=2, pady=4)
        navbar.columnconfigure(0, weight=1)
        self._nav_btns["Navigation"] = home_btn

        for i, label in enumerate(self.NAV_BUTTONS, start=1):
            btn = tk.Button(navbar, text=label, wraplength=90,
                            command=lambda l=label: self._show_page(l))
            btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=4)
            navbar.columnconfigure(i, weight=1)
            self._nav_btns[label] = btn

    def _build_pages(self):
        self._pages["Navigation"]        = NavigationPage(self.container)
        self._pages["Room/Event Lookup"] = RoomLookupPage(self.container)

        for name in self.NAV_BUTTONS:
            if name not in self._pages:
                self._pages[name] = PlaceholderPage(self.container, name)

        for page in self._pages.values():
            page.place(relwidth=1, relheight=1)

    def _show_page(self, name):
        page = self._pages.get(name)
        if page:
            page.lift()
        for label, btn in self._nav_btns.items():
            btn.config(relief="sunken" if label == name else "raised")


if __name__ == "__main__":
    app = App()
    app.mainloop()