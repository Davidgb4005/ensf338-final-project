import tkinter as tk
from tkinter import ttk
import main
import room_booking

# ── Helpers ──────────────────────────────────────────────────────────────────

def time_slots():
    """Return list of times from 00:00 to 23:30 in 30-min increments."""
    slots = []
    for h in range(24):
        for m in (0, 30):
            slots.append(f"{h:02d}:{m:02d}")
    return slots


# ── Sample Data ───────────────────────────────────────────────────────────────
# Format: (building, floor, room, booked_start, booked_end)
# booked_start/end are None if the room is fully available
SAMPLE_ROOMS = [
    ("Engineering",  "1", "101", "09:00", "10:30"),
    ("Engineering",  "1", "102", None,    None   ),
    ("Engineering",  "2", "201", "13:00", "14:00"),
    ("Engineering",  "2", "202", None,    None   ),
    ("Engineering",  "3", "301", "08:00", "09:30"),
    ("Science",      "1", "101", None,    None   ),
    ("Science",      "1", "102", "11:00", "12:30"),
    ("Science",      "2", "201", None,    None   ),
    ("Science",      "3", "301", "15:00", "16:00"),
    ("Library",      "1", "L01", None,    None   ),
    ("Library",      "1", "L02", "10:00", "11:00"),
    ("Library",      "2", "L11", None,    None   ),
    ("Admin Block",  "1", "A01", "09:00", "17:00"),
    ("Admin Block",  "2", "A21", None,    None   ),
]


def time_to_mins(t):
    """Convert HH:MM string to minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m


def ranges_overlap(s1, e1, s2, e2):
    """Return True if [s1,e1) overlaps [s2,e2)."""
    return time_to_mins(s1) < time_to_mins(e2) and time_to_mins(s2) < time_to_mins(e1)


def search_rooms(building, floor, room, start, end):

    result = main.room_finder(campus=main.campus,floor_number=floor,room_number=room,building_name=building)
    result[2].get_daily_booking()
    for building in result[0]:
        for floor in result[1]:
            for room in result[2]:

    return results


# ── Pages ─────────────────────────────────────────────────────────────────────

class RoomLookupPage(tk.Frame):
    BUILDINGS = ["Engineering", "Science", "Library", "Admin Block"]
    TIMES     = [""] + time_slots()   # blank = any

    def __init__(self, parent):
        super().__init__(parent)
        self._build()

    def _build(self):
        tk.Label(self, text="Room / Event Lookup & Book",
                 font=("Helvetica", 14, "bold")).pack(pady=(12, 8))

        # ── Filter form ──────────────────────────────────────────────────────
        form = tk.LabelFrame(self, text="Search Filters", padx=10, pady=8)
        form.pack(fill="x", padx=12, pady=(0, 8))

        # Row 0 – Building (required)
        tk.Label(form, text="Building Name *").grid(row=0, column=0, sticky="w", pady=3)
        self.building_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.building_var,
                     values=self.BUILDINGS, state="readonly",
                     width=20).grid(row=0, column=1, sticky="w", padx=(8, 20), pady=3)

        # Row 0 – Floor
        tk.Label(form, text="Floor").grid(row=0, column=2, sticky="w", pady=3)
        self.floor_var = tk.StringVar()
        tk.Entry(form, textvariable=self.floor_var, width=8).grid(
            row=0, column=3, sticky="w", padx=(8, 0), pady=3)

        # Row 1 – Room
        tk.Label(form, text="Room").grid(row=1, column=0, sticky="w", pady=3)
        self.room_var = tk.StringVar()
        tk.Entry(form, textvariable=self.room_var, width=10).grid(
            row=1, column=1, sticky="w", padx=(8, 20), pady=3)

        # Row 1 – Start time
        tk.Label(form, text="Start Time").grid(row=1, column=2, sticky="w", pady=3)
        self.start_var = tk.StringVar()
        ttk.Combobox(form, textvariable=self.start_var,
                     values=self.TIMES, state="readonly",
                     width=8).grid(row=1, column=3, sticky="w", padx=(8, 0), pady=3)

        # Row 2 – End time
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

        # ── Results table ────────────────────────────────────────────────────
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        cols = ("Building", "Floor", "Room","Time Slot","Booked By")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                 show="headings", selectmode="browse")
        for col in cols:
            self.tree.heading(col, text=col)
            #self.tree.column(col, width=120, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Book button below table
        tk.Button(self, text="Book Selected Room",
                  command=self._book_selected).pack(pady=(0, 10))
        self.book_feedback = tk.Label(self, text="")
        self.book_feedback.pack()

    # ── Actions ──────────────────────────────────────────────────────────────

    def _search(self):
        self.feedback.config(text="")
        self.book_feedback.config(text="")

        building = self.building_var.get().strip() or None
        floor    = self.floor_var.get().strip() or None
        room     = self.room_var.get().strip() or None
        start    = self.start_var.get().strip() or None
        end      = self.end_var.get().strip() or None

        # Validation
        if not building:
            self.feedback.config(text="Building Name is required.")
            return

        if (start and not end) or (end and not start):
            self.feedback.config(text="Please provide both Start and End time, or neither.")
            return

        if start and end:
            if time_to_mins(start) >= time_to_mins(end):
                self.feedback.config(text="Start time must be before End time.")
                return

        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = search_rooms(building, floor, room, start, end)

        if not results:
            self.feedback.config(text="No rooms found matching your criteria.")
            return

        for r in results:
            self.tree.insert("", "end",
                             values=(r["Building"], r["Floor"], r["Room"], r["Status"]))

        self.feedback.config(text=f"{len(results)} room(s) found.", fg="black")

    def _book_selected(self):
        selected = self.tree.focus()
        if not selected:
            self.book_feedback.config(text="Please select a room to book.", fg="red")
            return
        vals = self.tree.item(selected, "values")
        if vals[3] != "Available":
            self.book_feedback.config(
                text=f"Room {vals[2]} is already booked ({vals[3]}).", fg="red")
            return
        self.book_feedback.config(
            text=f"Room {vals[2]} in {vals[0]} Floor {vals[1]} booked successfully!",
            fg="green")


class NavigationPage(tk.Frame):
    LOCATIONS = [
        "Main Entrance", "Library", "Cafeteria", "Science Block",
        "Admin Office", "Gym", "Parking Lot A", "Parking Lot B",
        "Auditorium", "Medical Centre",
    ]

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

        # Navigation home button first
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
        self._pages["Navigation"]      = NavigationPage(self.container)
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