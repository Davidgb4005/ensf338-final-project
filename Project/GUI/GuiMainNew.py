import tkinter as tk
import numpy as np
from tkinter import ttk
import tkinter.messagebox as mb
from datetime import date, datetime
import os
import sys
from pathlib import Path                   

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import GlobalObjects.objects as obj
import RequestPipeline.request_pipeline as rp
import NavigationSystem.traversal as tv
import BookingSystem.room_booking as rb

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MAP_PATH = PROJECT_ROOT / "GUI" / "img" / "UCalgary-Main_Campus_Map-20230724.png"
TIME_INCREMENTS = 48
BOOKING_DAYS    = 90

PIPELINE_MODES = ["Manual", "Demo", "Auto"]
PIPELINE_MODE_MESSAGES = {
    "Auto":   "Mode is Set to Auto — requests are processed instantly.",
    "Demo":   "Mode is Set to Demo — requests are processed every 5 seconds.",
    "Manual": "Mode is Set to Manual — requests must be processed manually.",
}

# ---------------------------------------------------------------------------
# Theme / palette
# ---------------------------------------------------------------------------
BG_DARK    = "#1e2228"
BG_MEDIUM  = "#272c35"
BG_LIGHT   = "#2f3542"
ACCENT     = "#4f8ef7"
ACCENT_HOV = "#6ba3ff"
DANGER     = "#e05c5c"
SUCCESS    = "#4caf82"
FG_PRIMARY = "#e8ecf2"
FG_MUTED   = "#8a93a6"
BORDER     = "#3a4150"

FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_LABEL  = ("Segoe UI", 9)
FONT_BODY   = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 9, "bold")
FONT_NAV    = ("Segoe UI", 10, "bold")

DD_WIDTH = 16

# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------
campus           = obj.Campus()
request_pipeline = rp.request_pipeline()
pipeline_mode    = "Auto"
pages: dict      = {}
current_page     = None

# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------

def build_times(total_increments: int) -> list[str]:
    result = []
    split = 24 / total_increments
    for i in range(total_increments):
        hours   = i * split
        minutes = (hours * 60) % 60 if hours != 0 else 0
        result.append(f"{int(np.floor(hours)):02d}:{int(minutes):02d}")
    return result


def time_str_to_index(t: str) -> int:
    h, m = map(int, t.split(":"))
    return int((h + m / 60) * (len(times) / 24))


times = build_times(TIME_INCREMENTS)

# ---------------------------------------------------------------------------
# Styling helpers
# ---------------------------------------------------------------------------

def apply_theme(root: tk.Tk):
    root.configure(bg=BG_DARK)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background=BG_LIGHT, foreground=FG_PRIMARY,
        fieldbackground=BG_LIGHT, rowheight=26,
        font=FONT_BODY, borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background=BG_DARK, foreground=FG_MUTED,
        font=FONT_LABEL, relief="flat",
    )
    style.map("Treeview",         background=[("selected", ACCENT)])
    style.map("Treeview.Heading", background=[("active",   BG_MEDIUM)])
    style.configure(
        "Vertical.TScrollbar",
        background=BG_LIGHT, troughcolor=BG_MEDIUM,
        arrowcolor=FG_MUTED, borderwidth=0,
    )


def _darken(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"#{max(0,r-30):02x}{max(0,g-30):02x}{max(0,b-30):02x}"


def styled_frame(parent, bg=BG_MEDIUM, padx=0, pady=0) -> tk.Frame:
    return tk.Frame(parent, bg=bg, padx=padx, pady=pady)


def styled_label(parent, text, font=FONT_BODY, fg=FG_PRIMARY, bg=BG_MEDIUM, **kw) -> tk.Label:
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)


def styled_button(parent, text, command, variant="default", **kw) -> tk.Button:
    colours = {
        "default": (BG_LIGHT, FG_PRIMARY),
        "primary": (ACCENT,   "#ffffff"),
        "danger":  (DANGER,   "#ffffff"),
        "success": (SUCCESS,  "#ffffff"),
    }
    bg, fg = colours.get(variant, colours["default"])
    btn = tk.Button(
        parent, text=text, command=command,
        font=FONT_BUTTON, bg=bg, fg=fg,
        activebackground=ACCENT_HOV, activeforeground="#ffffff",
        relief="flat", padx=10, pady=5,
        cursor="hand2", bd=0, **kw,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_HOV if variant == "primary" else _darken(bg)))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def styled_option_menu(parent, var, *values, width=DD_WIDTH) -> tk.OptionMenu:
    om = tk.OptionMenu(parent, var, *values)
    om.config(
        width=width, bg=BG_LIGHT, fg=FG_PRIMARY,
        activebackground=ACCENT, activeforeground="#ffffff",
        relief="flat", font=FONT_BODY, highlightthickness=0, bd=0,
    )
    om["menu"].config(
        bg=BG_LIGHT, fg=FG_PRIMARY,
        activebackground=ACCENT, activeforeground="#ffffff",
        font=FONT_BODY, bd=0,
    )
    return om


def styled_entry(parent, width=18, **kw) -> tk.Entry:
    return tk.Entry(
        parent, width=width, bg=BG_LIGHT, fg=FG_PRIMARY,
        insertbackground=FG_PRIMARY, relief="flat", font=FONT_BODY,
        highlightthickness=1, highlightcolor=ACCENT,
        highlightbackground=BORDER, **kw,
    )


def labelled_control(parent, label_text: str, widget: tk.Widget, bg=BG_MEDIUM) -> tk.Frame:
    wrapper = styled_frame(parent, bg=bg)
    styled_label(wrapper, label_text, font=FONT_LABEL, fg=FG_MUTED, bg=bg).pack(anchor="w")
    widget.pack(anchor="w")
    return wrapper


def section_tag(parent, text: str, bg=BG_DARK) -> tk.Label:
    return tk.Label(
        parent, text=f"  {text}",
        font=("Segoe UI", 7, "bold"),
        fg=ACCENT, bg=bg, anchor="w",
    )


def separator(parent, bg=BORDER) -> tk.Frame:
    return tk.Frame(parent, bg=bg, height=1)


def popup_base(title: str) -> tk.Toplevel:
    popup = tk.Toplevel()
    popup.title(title)
    popup.configure(bg=BG_MEDIUM)
    popup.resizable(False, False)
    return popup


def popup_field(parent, label: str, prefill: str = "") -> tk.Entry:
    styled_label(parent, label, font=FONT_LABEL, fg=FG_MUTED, bg=BG_MEDIUM).pack(
        anchor="w", padx=16, pady=(10, 2)
    )
    entry = styled_entry(parent, width=28)
    entry.pack(anchor="w", padx=16, pady=(0, 4))
    if prefill:
        entry.insert(0, prefill)
    return entry

# ---------------------------------------------------------------------------
# Shared validation helpers
# ---------------------------------------------------------------------------

def validate_not_empty(value, error_title: str, error_msg: str) -> bool:
    if not value:
        mb.showinfo(error_title, error_msg)
        return False
    return True


def validate_date(date_str: str):
    today = datetime.today()
    try:
        selected = datetime.strptime(date_str, "%Y/%m/%d")
    except ValueError:
        mb.showinfo("Date Error", "Incorrect date format — use YYYY/MM/DD")
        return None
    delta = (selected - today).days
    if delta < -1:
        mb.showinfo("Date Error", "Date cannot be in the past.")
        return None
    if delta > BOOKING_DAYS:
        mb.showinfo("Date Error", f"Date cannot be more than {BOOKING_DAYS} days in the future.")
        return None
    return delta


def popup_single_field(title: str, label: str):
    popup = popup_base(title)
    entry = popup_field(popup, label)
    result = [None]

    def submit():
        result[0] = entry.get()
        popup.destroy()

    styled_button(popup, "Submit", submit, variant="primary").pack(pady=(8, 16), padx=16)
    popup.wait_window()
    return result[0]

# ---------------------------------------------------------------------------
# Treeview helper
# ---------------------------------------------------------------------------

def make_table(parent, cols: tuple, col_widths: dict) -> tuple[ttk.Treeview, ttk.Scrollbar]:
    frame = styled_frame(parent, bg=BG_MEDIUM)
    frame.pack(fill="both", expand=True, padx=8, pady=(4, 0))

    table = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
    for col in cols:
        table.heading(col, text=col)
        table.column(col, width=col_widths.get(col, 120), anchor="center")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    table.pack(fill="both", expand=True)

    table.tag_configure("odd",  background="#2a3040")
    table.tag_configure("even", background=BG_LIGHT)
    return table, vsb


def table_insert(table: ttk.Treeview, row_index: int, values: tuple):
    tag = "even" if row_index % 2 == 0 else "odd"
    table.insert("", "end", tags=(tag,), values=values)

# ---------------------------------------------------------------------------
# Page builder: Room Booking
# ---------------------------------------------------------------------------

def build_booking_page(parent: tk.Frame) -> tk.Frame:
    page = styled_frame(parent, bg=BG_MEDIUM)

    building_var = tk.StringVar(value="Building")
    floor_var    = tk.StringVar(value="Floor")
    room_var     = tk.StringVar(value="Room")
    start_var    = tk.StringVar(value="Start Time")
    end_var      = tk.StringVar(value="End Time")

    def get_floor():
        v = floor_var.get()
        return int(v) if v != "Floor" else None

    def get_room():
        v = room_var.get()
        return int(v) if v != "Room" else None

    def get_selected_room():
        b, f, r = building_var.get(), get_floor(), get_room()
        if f is None or r is None:
            return None
        return campus.get_buildings()[b].floors[f].rooms[r]

    def refresh_floor_dd(*_):
        floor_var.set("Floor")
        room_var.set("Room")
        _repopulate(floor_dd, floor_var, [f.id for f in campus.get_floors(building_var.get())])

    def refresh_room_dd(*_):
        room_var.set("Room")
        f = floor_var.get()
        if f == "Floor":
            return
        _repopulate(room_dd, room_var, [r.id for r in campus.get_rooms(building_var.get(), f)])

    def _repopulate(widget, var, items):
        menu = widget["menu"]
        menu.delete(0, "end")
        for item in items:
            menu.add_command(label=item, command=lambda v=item: var.set(v))

    building_var.trace_add("write", refresh_floor_dd)
    floor_var.trace_add("write", refresh_room_dd)

    # ── Filter bar ───────────────────────────────────────────────────────────
    filter_bar = styled_frame(page, bg=BG_DARK, padx=10, pady=8)
    filter_bar.pack(side="top", fill="x")

    def grid_label(parent, text, col, row=0):
        """Place a muted label in a grid cell."""
        lbl = tk.Label(parent, text=text, font=FONT_LABEL, fg=FG_MUTED, bg=BG_DARK, anchor="w")
        lbl.grid(row=row, column=col, sticky="w", padx=(4, 4), pady=(0, 2))

    def grid_widget(widget, col, row=1, padx=(4, 4)):
        widget.grid(row=row, column=col, sticky="w", padx=padx, pady=(0, 4))

    # Row 1 — Location
    row1 = styled_frame(filter_bar, bg=BG_DARK)
    row1.pack(fill="x", pady=(0, 4))

    section_tag(row1, "LOCATION").grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 8))

    building_dd = styled_option_menu(row1, building_var, *campus.get_building_keys())
    grid_label(row1, "Building", col=1)
    grid_widget(building_dd, col=1)

    floor_dd = styled_option_menu(row1, floor_var, [])
    grid_label(row1, "Floor", col=2)
    grid_widget(floor_dd, col=2)

    room_dd = styled_option_menu(row1, room_var, [])
    grid_label(row1, "Room", col=3)
    grid_widget(room_dd, col=3)

    def _show_room_info():
        try:
            room = get_selected_room()
            if room is None:
                raise ValueError
            mb.showinfo("Room Info", room.get_info())
        except (ValueError, KeyError):
            mb.showinfo("Data Error", "Please select a building, floor, and room.")

    def _show_building_info():
        b = building_var.get()
        if b == "Building":
            mb.showinfo("Error", "Please select a building.")
            return
        mb.showinfo("Building Info", campus.get_buildings()[b].get_info())

    # Info buttons sit in column 4, aligned to widget row
    info_frame = styled_frame(row1, bg=BG_DARK)
    info_frame.grid(row=1, column=4, sticky="w", padx=(12, 0), pady=(0, 4))
    styled_button(info_frame, "Room Info",     _show_room_info,     variant="default").pack(side="left", padx=2)
    styled_button(info_frame, "Building Info", _show_building_info, variant="default").pack(side="left", padx=2)

    separator(filter_bar, bg=BORDER).pack(fill="x", pady=4)

    # Row 2 — Time filter
    row2 = styled_frame(filter_bar, bg=BG_DARK)
    row2.pack(fill="x")

    section_tag(row2, "TIME FILTER").grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 8))

    date_entry = styled_entry(row2, width=14)
    date_entry.insert(0, date.today().strftime("%Y/%m/%d"))
    grid_label(row2, "Date (YYYY/MM/DD)", col=1)
    grid_widget(date_entry, col=1)

    start_dd = styled_option_menu(row2, start_var, *times, width=12)
    grid_label(row2, "Start Time", col=2)
    grid_widget(start_dd, col=2)

    end_dd = styled_option_menu(row2, end_var, *times, width=12)
    grid_label(row2, "End Time", col=3)
    grid_widget(end_dd, col=3)

    # ── Table ─────────────────────────────────────────────────────────────────
    cols = ("Booked For", "Booked By", "Start Time", "End Time")
    table, _ = make_table(page, cols, {"Booked For": 200, "Booked By": 200, "Start Time": 120, "End Time": 120})

    def _refresh_table(*_):
        day = validate_date(date_entry.get())
        if day is None:
            return
        start = 0 if start_var.get() == "Start Time" else time_str_to_index(start_var.get())
        end   = TIME_INCREMENTS - 1 if end_var.get() == "End Time" else time_str_to_index(end_var.get())
        table.delete(*table.get_children())
        bookings = campus.get_bookings(
            building_var.get(), floor_var.get(), room_var.get(), day, start, end
        )
        if bookings is None:
            mb.showinfo("Display Error", "Room is deleted. Reinitialize via Edit Room.")
            return
        for i, b in enumerate(bookings):
            table_insert(table, i, (b.booking_type, b.booker_name, b.start_time, b.end_time))

    styled_button(row2, "⟳  Refresh", _refresh_table, variant="primary").grid(
        row=1, column=4, sticky="w", padx=(14, 4), pady=(0, 4)
    )

    # ── Action bar ────────────────────────────────────────────────────────────
    separator(page, bg=BORDER).pack(fill="x")

    action_bar = styled_frame(page, bg=BG_DARK, padx=10, pady=7)
    action_bar.pack(side="bottom", fill="x")

    def _get_selected_row():
        sel = table.focus()
        if not sel:
            mb.showinfo("Selection Error", "Please select a row in the table.")
            return None
        return table.item(sel, "values")

    def _resolve_booking(vals):
        day = validate_date(date_entry.get())
        return campus.get_bookings(
            building_var.get(), floor_var.get(), room_var.get(),
            day, time_str_to_index(vals[2]), time_str_to_index(vals[3]),
        )[0]

    def _require_building():
        b = building_var.get()
        if b == "Building":
            mb.showinfo("Error", "Please select a building.")
            return None
        return b

    def _require_building_and_floor():
        b, f = building_var.get(), floor_var.get()
        if b == "Building" or f == "Floor":
            mb.showinfo("Error", "Please select a building and floor.")
            return None, None
        return b, f

    # Booking actions
    def _add_booking():
        day = validate_date(date_entry.get())
        if day is None:
            return
        vals = _get_selected_row()
        if vals is None:
            return
        if vals[0] != "Vacant":
            mb.showinfo("Booking Error", f"Already booked for {vals[2]} – {vals[3]}.")
            return
        popup = popup_base("Add Booking")
        name_e = popup_field(popup, "Booker Name")
        type_e = popup_field(popup, "Booking Type")
        result = [None, None]

        def submit():
            result[0] = name_e.get()
            result[1] = type_e.get()
            popup.destroy()

        styled_button(popup, "Confirm Booking", submit, variant="primary").pack(pady=(8, 16), padx=16)
        popup.wait_window()
        if not result[0] or not result[1]:
            mb.showinfo("Booking Error", "Please fill in all fields.")
            return
        booking = _resolve_booking(vals)
        request_pipeline.enque_request(
            lambda: booking.update_booking(result[0], result[1]), _refresh_table, "Add Booking"
        )

    def _delete_booking():
        vals = _get_selected_row()
        if vals is None:
            return
        if vals[0] == "Vacant":
            mb.showinfo("Booking Error", f"No booking for {vals[2]} – {vals[3]}.")
            return
        booking = _resolve_booking(vals)
        request_pipeline.enque_request(
            lambda: booking.update_booking(None, "Vacant"), _refresh_table, "Delete Booking"
        )

    # Service actions
    def _add_service():
        b = _require_building()
        if b is None:
            return
        name = popup_single_field("Add Service", "Service Name")
        if not validate_not_empty(name, "Service Error", "Please enter a service name."):
            return
        campus.add_serivce(name, b)

    def _delete_service():
        b = _require_building()
        if b is None:
            return
        name = popup_single_field("Delete Service", "Service Name")
        if not validate_not_empty(name, "Service Error", "Please enter a service name."):
            return
        campus.delete_service(name, b)

    # Room actions
    def _append_room():
        b, f = _require_building_and_floor()
        if b is None:
            return
        popup = popup_base("Add Room")
        info_e = popup_field(popup, "Info")
        type_e = popup_field(popup, "Room Type")
        result = [None, None]

        def submit():
            result[0] = info_e.get()
            result[1] = type_e.get()
            popup.destroy()

        styled_button(popup, "Add Room", submit, variant="success").pack(pady=(8, 16), padx=16)
        popup.wait_window()
        if not all(result):
            mb.showinfo("Add Room Error", "Please fill in all fields.")
            return
        floor_rooms = campus.get_buildings()[b].floors[int(f)].rooms
        new_room = obj.Room(len(floor_rooms), result[1])
        new_room.info = result[0]
        floor_rooms.append(new_room)
        refresh_room_dd()

    def _delete_room():
        b, f = _require_building_and_floor()
        if b is None:
            return
        r = room_var.get()
        if r == "Room":
            mb.showinfo("Error", "Please select a room.")
            return
        room = campus.get_buildings()[b].floors[int(f)].rooms[int(r)]
        room.booking = room.room_type = room.info = None
        refresh_room_dd()

    def _edit_room():
        b, f = _require_building_and_floor()
        if b is None:
            return
        r = room_var.get()
        if r == "Room":
            mb.showinfo("Error", "Please select a room.")
            return
        room = campus.get_buildings()[b].floors[int(f)].rooms[int(r)]
        popup = popup_base("Edit Room")
        info_e = popup_field(popup, "Info",      prefill=room.info      or "")
        type_e = popup_field(popup, "Room Type", prefill=room.room_type or "")
        styled_label(popup, "Reinitialize Room Bookings", font=FONT_LABEL, fg=FG_MUTED, bg=BG_MEDIUM).pack(
            anchor="w", padx=16, pady=(10, 2)
        )
        reinit_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            popup, variable=reinit_var, bg=BG_MEDIUM, fg=FG_PRIMARY,
            selectcolor=BG_LIGHT, activebackground=BG_MEDIUM, activeforeground=FG_PRIMARY,
        ).pack(anchor="w", padx=16)
        result = [None, None, None]

        def submit():
            result[0] = info_e.get()
            result[1] = type_e.get()
            result[2] = reinit_var.get()
            popup.destroy()

        styled_button(popup, "Save Changes", submit, variant="primary").pack(pady=(8, 16), padx=16)
        popup.wait_window()
        if not result[0] or not result[1]:
            mb.showinfo("Edit Room Error", "Please fill in all fields.")
            return
        room.info = result[0]
        room.room_type = result[1]
        if result[2]:
            room.booking = rb.BookingSystem(BOOKING_DAYS)
        refresh_room_dd()
        _refresh_table()

    # Building actions
    def _add_building():
        popup = popup_base("Add Building")
        fields = [
            popup_field(popup, "Building Name (e.g. Eng A Block)"),
            popup_field(popup, "Building ID   (e.g. ENA)"),
            popup_field(popup, "Number of Floors"),
            popup_field(popup, "Rooms Per Floor"),
        ]
        result = [None] * 4

        def submit():
            for i, e in enumerate(fields):
                result[i] = e.get()
            popup.destroy()

        styled_button(popup, "Create Building", submit, variant="success").pack(pady=(8, 16), padx=16)
        popup.wait_window()
        if not all(result):
            mb.showinfo("Add Building Error", "Please fill in all fields.")
            return
        new_building = obj.Building(result[0], result[1], obj.Location(0, 0))
        campus.add_building(int(result[2]), int(result[3]), new_building)
        generate_pages()
        show_room_booking()

    def _delete_building():
        b = building_var.get()
        if b == "Building":
            mb.showinfo("Error", "Please select a building.")
            return
        campus.remove_building(campus.get_buildings()[b])
        generate_pages()
        show_room_booking()

    # ── Build grouped button bar ──────────────────────────────────────────────
    button_groups = [
        ("Bookings",  [("＋ Booking",  _add_booking,    "success"),
                       ("－ Booking",  _delete_booking, "danger")]),
        ("Services",  [("＋ Service",  _add_service,    "success"),
                       ("－ Service",  _delete_service, "danger")]),
        ("Rooms",     [("＋ Room",     _append_room,    "success"),
                       ("✎  Edit",    _edit_room,      "default"),
                       ("－ Room",     _delete_room,    "danger")]),
        ("Buildings", [("＋ Building", _add_building,   "success"),
                       ("－ Building", _delete_building,"danger")]),
    ]
    for group_name, btns in button_groups:
        grp = styled_frame(action_bar, bg=BG_DARK)
        grp.pack(side="left", padx=(0, 14))
        styled_label(grp, group_name, font=("Segoe UI", 7, "bold"), fg=FG_MUTED, bg=BG_DARK).pack(anchor="w")
        row = styled_frame(grp, bg=BG_DARK)
        row.pack()
        for label, cmd, variant in btns:
            styled_button(row, label, cmd, variant=variant).pack(side="left", padx=2)

    return page

# ---------------------------------------------------------------------------
# Page builder: Navigation
# ---------------------------------------------------------------------------

def build_nav_page(parent: tk.Frame) -> tk.Frame:
    page = styled_frame(parent, bg=BG_MEDIUM)

    ctrl_bar = styled_frame(page, bg=BG_DARK, padx=10, pady=10)
    ctrl_bar.pack(side="top", fill="x")

    start_var = tk.StringVar(value="Start Location")
    end_var   = tk.StringVar(value="End Location")

    start_dd = styled_option_menu(ctrl_bar, start_var, *campus.get_building_keys(), width=20)
    tk.Label(ctrl_bar, text="From", font=FONT_LABEL, fg=FG_MUTED, bg=BG_DARK).grid(row=0, column=0, sticky="w", padx=(4,4), pady=(0,2))
    start_dd.grid(row=1, column=0, sticky="w", padx=(4,4), pady=(0,4))

    end_dd = styled_option_menu(ctrl_bar, end_var, *campus.get_building_keys(), width=20)
    tk.Label(ctrl_bar, text="To", font=FONT_LABEL, fg=FG_MUTED, bg=BG_DARK).grid(row=0, column=1, sticky="w", padx=(4,4), pady=(0,2))
    end_dd.grid(row=1, column=1, sticky="w", padx=(4,4), pady=(0,4))

    def _get_node_ids():
        s = campus.campus_graph.get_node_id(start_var.get())
        e = campus.campus_graph.get_node_id(end_var.get())
        if s == e:
            mb.showinfo("Navigation Error", "Start and end cannot be the same location.")
            return None
        return s, e

    def submit():
        nodes = _get_node_ids()
        if nodes is None:
            return
        path = campus.campus_graph.find_path(*nodes)
        closure = lambda: tv.draw_graph(path, MAP_PATH)
        request_pipeline.enque_request(closure, lambda: None, "Navigation Rendering")
        request_pipeline.enque_request(
            lambda: campus.campus_graph.undo_buffer.append(closure),
            lambda: None, "Navigation Undo Enqueue",
        )

    def animate():
        nodes = _get_node_ids()
        if nodes is None:
            return
        path, steps = campus.campus_graph.find_path_steps(*nodes)
        closure = tv.animate_search(campus.campus_graph.nodes, steps, MAP_PATH)
        request_pipeline.enque_request(closure, lambda: None, "Navigation Rendering")
        request_pipeline.enque_request(
            lambda: campus.campus_graph.undo_buffer.append(closure),
            lambda: None, "Navigation Undo Enqueue",
        )

    def undo():
        request_pipeline.enque_request(
            lambda: campus.campus_graph.undo(), lambda: None, "Navigation Undo"
        )

    btn_area = styled_frame(ctrl_bar, bg=BG_DARK)
    btn_area.grid(row=1, column=2, sticky="w", padx=(14, 4), pady=(0, 4))
    styled_button(btn_area, "Find Path", submit,  variant="primary").pack(side="left", padx=3)
    styled_button(btn_area, "Animate",   animate, variant="default").pack(side="left", padx=3)
    styled_button(btn_area, "Undo",      undo,    variant="default").pack(side="left", padx=3)

    separator(page, bg=BORDER).pack(fill="x")

    map_frame = styled_frame(page, bg=BG_MEDIUM)
    map_frame.pack(fill="both", expand=True)
    try:
        photo = tk.PhotoImage(file=MAP_PATH)
        img_label = tk.Label(map_frame, image=photo, bg=BG_MEDIUM)
        img_label.image = photo
        img_label.pack(expand=True)
    except tk.TclError:
        styled_label(map_frame, "[ Map image not found ]", fg=FG_MUTED, bg=BG_MEDIUM).pack(expand=True)

    return page

# ---------------------------------------------------------------------------
# Page builder: Request Processing
# ---------------------------------------------------------------------------

_DEMO_REQUESTS = [
    (1, "Emergency – Fire alarm trigger in ICT"),
    (1, "Emergency – Medical assistance at Library"),
    (2, "Navigate: AB → TFDL"),
    (2, "Navigate: ICT → SH"),
    (2, "Navigate: KNA → DC"),
    (2, "Navigate: MFH → ENA"),
    (2, "Navigate: BI → MH"),
    (2, "Navigate: HNSC → OO"),
    (2, "Navigate: CCIT → MSC"),
    (2, "Navigate: EDC → AU"),
    (3, "Room booking – ICT 201 for study session"),
    (3, "Room booking – TFDL L3-12 for group project"),
    (3, "Room booking – MS 405 for exam review"),
    (3, "IT support ticket – projector in ICT-121 offline"),
    (3, "IT support ticket – wifi down in Craigie Hall"),
    (3, "Maintenance – broken heater in Residence"),
    (3, "Maintenance – elevator fault in Science A"),
    (3, "Maintenance – parking gate malfunction"),
    (3, "Info lookup – room capacity for ENA 301"),
    (3, "Info lookup – services available at MacEwan Hall"),
    (3, "Info lookup – events today in Social Sciences"),
    (3, "Low priority – general feedback submission"),
]


def build_request_processing_page(parent: tk.Frame) -> tk.Frame:
    page = styled_frame(parent, bg=BG_MEDIUM)

    # ── Control bar ────────────────────────────────────────────────────────────
    ctrl_bar = styled_frame(page, bg=BG_DARK, padx=10, pady=8)
    ctrl_bar.pack(side="top", fill="x")

    # ── Queue table ────────────────────────────────────────────────────────────
    section_tag(page, "PENDING QUEUE").pack(anchor="w", padx=10, pady=(6, 0))
    cols = ("Request Id", "Priority", "Description")
    table, _ = make_table(page, cols, {
        "Request Id": 90, "Priority": 110, "Description": 430,
    })

    # ── Processing log ─────────────────────────────────────────────────────────
    section_tag(page, "PROCESSING LOG").pack(anchor="w", padx=10, pady=(8, 0))
    log_frame = styled_frame(page, bg=BG_MEDIUM)
    log_frame.pack(fill="both", expand=True, padx=8, pady=(2, 6))

    log_box = tk.Text(
        log_frame,
        height=8,
        bg=BG_LIGHT, fg=FG_PRIMARY,
        font=("Consolas", 9),
        relief="flat",
        state="disabled",
        wrap="word",
        highlightthickness=1,
        highlightbackground=BORDER,
    )
    log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=log_box.yview)
    log_box.configure(yscrollcommand=log_scroll.set)
    log_scroll.pack(side="right", fill="y")
    log_box.pack(fill="both", expand=True)

    log_box.tag_configure("ts",    foreground=FG_MUTED)
    log_box.tag_configure("ok",    foreground=SUCCESS)
    log_box.tag_configure("emerg", foreground=DANGER)
    log_box.tag_configure("std",   foreground=ACCENT)

    _demo_running = [False]

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _log(text: str, tag: str = "ok"):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        log_box.configure(state="normal")
        log_box.insert("end", f"[{ts}]  ", "ts")
        log_box.insert("end", text + "\n", tag)
        log_box.see("end")
        log_box.configure(state="disabled")

    def _priority_label(p: int) -> str:
        return {1: "🔴 Emergency", 2: "🟡 Standard", 3: "⚪ Low"}.get(p, str(p))

    def refresh_table(*_):
        table.delete(*table.get_children())
        node = request_pipeline.buffer.peek_tail()
        i = 0
        while node is not None:
            r = node.val
            if isinstance(r.request_data, tuple):
                pri, desc = r.request_data
                prio_text = _priority_label(pri)
            else:
                prio_text = "—"
                desc = str(r.request_data)
            table_insert(table, i, (r.position, prio_text, desc))
            node = node.prev
            i += 1

    def _enqueue_demo_requests():
        for priority, desc in _DEMO_REQUESTS:
            request_pipeline.enque_request(
                lambda p=priority, d=desc: _log(
                    f"Processed [{_priority_label(p)}] – {d}",
                    tag="emerg" if p == 1 else ("std" if p == 2 else "ok"),
                ),
                lambda: None,
                (priority, desc),
            )
        _log(f"Enqueued {len(_DEMO_REQUESTS)} demo requests.", "ts")
        refresh_table()

    def process_next():
        if request_pipeline.buffer.get_len() == 0:
            _log("Queue is empty – nothing to process.", "ts")
            return
        request_pipeline.deque_request()
        refresh_table()

    def process_all():
        count = 0
        while request_pipeline.buffer.get_len() > 0:
            request_pipeline.deque_request()
            count += 1
        _log(f"Processed all {count} remaining requests." if count else "Queue was already empty.", "ts")
        refresh_table()

    def _demo_step(remaining: int, saved_mode: str):
        if remaining <= 0 or request_pipeline.buffer.get_len() == 0:
            _demo_running[0] = False
            # Restore the pipeline mode that was active before the demo
            global pipeline_mode
            pipeline_mode = saved_mode
            mode_label.config(text=f"Pipeline: {pipeline_mode}")
            _log(f"─── Demo complete — pipeline restored to '{saved_mode}' mode ───", "ts")
            refresh_table()
            return
        request_pipeline.deque_request()
        refresh_table()
        page.after(250, lambda: _demo_step(remaining - 1, saved_mode))

    def run_demo():
        global pipeline_mode
        if _demo_running[0]:
            _log("Demo already running – please wait.", "ts")
            return
        log_box.configure(state="normal")
        log_box.delete("1.0", "end")
        log_box.configure(state="disabled")
        # Switch to Manual so the auto-drainer doesn't consume requests
        saved_mode = pipeline_mode
        pipeline_mode = "Manual"
        mode_label.config(text="Pipeline: Manual")
        _log("═══ Starting Pipeline Demo (22 requests) ═══", "ts")
        _log(f"Pipeline switched to Manual (was {saved_mode}) — requests will not auto-drain.", "ts")
        _enqueue_demo_requests()
        _demo_running[0] = True
        page.after(300, lambda: _demo_step(len(_DEMO_REQUESTS), saved_mode))

    def load_dummies():
        global pipeline_mode
        if _demo_running[0]:
            _log("Demo is currently running. Wait for it to finish.", "ts")
            return
        pipeline_mode = "Manual"
        mode_label.config(text="Pipeline: Manual")
        _log("═══ Loading Dummy Data ═══", "ts")
        _log("Pipeline switched to Manual — you can now process requests manually.", "ts")
        _enqueue_demo_requests()

    # ── Buttons ────────────────────────────────────────────────────────────────
    styled_button(ctrl_bar, "🚀  Run Demo",       run_demo,      variant="primary").pack(side="left", padx=4)
    styled_button(ctrl_bar, "📥  Load Dummies",  load_dummies,  variant="default").pack(side="left", padx=4)
    styled_button(ctrl_bar, "▶  Process Next",   process_next,  variant="default").pack(side="left", padx=4)
    styled_button(ctrl_bar, "⏩  Process All",    process_all,   variant="default").pack(side="left", padx=4)
    styled_button(ctrl_bar, "⟳  Refresh",        refresh_table, variant="default").pack(side="left", padx=4)

    return page

# ---------------------------------------------------------------------------
# Placeholder pages
# ---------------------------------------------------------------------------

def build_placeholder_page(parent: tk.Frame, name: str) -> tk.Frame:
    page = styled_frame(parent, bg=BG_MEDIUM)
    styled_label(
        page, name.replace("_", " ").title(),
        font=FONT_TITLE, fg=FG_MUTED, bg=BG_MEDIUM,
    ).pack(expand=True)
    return page

# ---------------------------------------------------------------------------
# Page management
# ---------------------------------------------------------------------------

def generate_pages():
    global pages
    pages["navigation"]         = build_nav_page(frame)
    pages["room_booking"]       = build_booking_page(frame)
    pages["request_processing"] = build_request_processing_page(frame)
    for name in ("service_queue", "completed_operation", "bonus"):
        pages[name] = build_placeholder_page(frame, name)


def show_page(name: str):
    global current_page
    if current_page:
        current_page.pack_forget()
    current_page = pages[name]
    current_page.pack(fill="both", expand=True)


def show_navigation():          show_page("navigation")
def show_room_booking():        show_page("room_booking")
def show_service_queue():       show_page("service_queue")
def show_request_processing():  show_page("request_processing")
def show_completed_operation(): show_page("completed_operation")
def show_bonus():               show_page("bonus")

# ---------------------------------------------------------------------------
# Request pipeline
# ---------------------------------------------------------------------------

def toggle_pipeline_mode():
    global pipeline_mode
    idx = PIPELINE_MODES.index(pipeline_mode)
    pipeline_mode = PIPELINE_MODES[(idx + 1) % len(PIPELINE_MODES)]
    mb.showinfo("Pipeline Mode", PIPELINE_MODE_MESSAGES[pipeline_mode])
    mode_label.config(text=f"Pipeline: {pipeline_mode}")


def request_pipeline_caller():
    global pipeline_mode
    if pipeline_mode == "Auto":
        while request_pipeline.buffer.get_len() > 0:
            request_pipeline.deque_request()
        root.after(500, request_pipeline_caller)
    elif pipeline_mode == "Demo":
        if request_pipeline.buffer.get_len() > 0:
            request_pipeline.deque_request()
        root.after(5000, request_pipeline_caller)
    else:
        root.after(5000, request_pipeline_caller)

# ---------------------------------------------------------------------------
# Root window
# ---------------------------------------------------------------------------

root = tk.Tk()
root.title("UCalgary Campus Manager")
root.geometry("1100x700")
root.minsize(900, 580)
apply_theme(root)

# Title bar
title_bar = tk.Frame(root, bg=BG_DARK, height=48)
title_bar.pack(side="top", fill="x")
title_bar.pack_propagate(False)
tk.Label(
    title_bar, text="  UCalgary Campus Manager",
    font=("Segoe UI", 12, "bold"), fg=FG_PRIMARY, bg=BG_DARK, anchor="w",
).pack(side="left", fill="y")
mode_label = tk.Label(
    title_bar, text=f"Pipeline: {pipeline_mode}",
    font=FONT_LABEL, fg=ACCENT, bg=BG_DARK,
)
mode_label.pack(side="right", padx=14)

# Accent line under title
tk.Frame(root, bg=ACCENT, height=2).pack(fill="x")

# Body — sidebar + content
body = tk.Frame(root, bg=BG_DARK)
body.pack(fill="both", expand=True)

# Sidebar
sidebar = tk.Frame(body, bg=BG_DARK, width=160)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
tk.Frame(sidebar, bg=BORDER, width=1).pack(side="right", fill="y")

_nav_btns = []

nav_items = [
    ("🗺  Navigation",     show_navigation),
    ("📅  Room Booking",   show_room_booking),
    ("🔧  Service Queue",  show_service_queue),
    ("⚙  Requests",       show_request_processing),
    ("✔  Completed Ops",  show_completed_operation),
    ("★  Bonus",           show_bonus),
]


def _make_nav_btn(label: str, cmd):
    btn = tk.Button(
        sidebar, text=label, font=FONT_NAV,
        fg=FG_MUTED, bg=BG_DARK,
        activebackground=BG_LIGHT, activeforeground=FG_PRIMARY,
        relief="flat", anchor="w", padx=16, pady=10,
        cursor="hand2", bd=0,
    )
    btn.pack(fill="x")
    _nav_btns.append(btn)

    def on_click():
        for b in _nav_btns:
            b.config(fg=FG_MUTED, bg=BG_DARK)
        btn.config(fg=FG_PRIMARY, bg=BG_LIGHT)
        cmd()

    btn.config(command=on_click)
    return btn


for lbl, fn in nav_items:
    _make_nav_btn(lbl, fn)

tk.Frame(sidebar, bg=BG_DARK).pack(fill="both", expand=True)
tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x")
styled_button(sidebar, "⇄  Toggle Mode", toggle_pipeline_mode, variant="default").pack(
    fill="x", padx=8, pady=8
)

# Content frame
frame = tk.Frame(body, bg=BG_MEDIUM)
frame.pack(side="left", fill="both", expand=True)

# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------

generate_pages()
show_page("navigation")
_nav_btns[0].config(fg=FG_PRIMARY, bg=BG_LIGHT)
request_pipeline_caller()

root.mainloop()
