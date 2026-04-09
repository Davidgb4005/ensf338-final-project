import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import tkinter as tk
from tkinter import ttk
import random as rd
from DataStructures.LifoRingBuffer import LifoRingBuffer as lifo
import RequestPipeline.request_pipeline as rp


def helper_build_times(total_increments: int) -> list[str]:
    times: list[str] = []
    splits = 24/total_increments
    for i in range(total_increments):
        minutes = 0
        hours: float = i * splits
        if hours != 0:
            minutes = (hours*60) % 60
        hours = np.floor(i * splits)
        times.append(f"{int(hours):02d}:{(int)(minutes):02d}")
    return(times)

def time_str_to_float(t: str) -> float:
    h, m = map(int, t.split(":"))
    return h + m / 60  # 12:30 → 12.5, 13:00 → 13.0

class BookingSystem:
    def __init__(self, capacity: int) -> None:
        self.daily_bookings: lifo[DailyBooking] = lifo(capacity, DailyBooking) #90 day capacity
        self.capacity = capacity

    def get_daily_booking(self, index: int) -> "DailyBooking | None": # the quotes are there because dailybooking is defined later in the program, but setting it as return type now shows a warning when type hinting.
        return self.daily_bookings.access_at_index(index)
    
    def book_room(self, index: int, start_time: int, booker_name: str, booking_type: str) -> None:
        roomToBook = self.daily_bookings.access_at_index(index)
        if roomToBook is not None: #access_at_index method has return type -> T | None. This is to ensure it accounts for that.
            roomToBook.hourly_bookings[start_time].booker_name = booker_name
            roomToBook.hourly_bookings[start_time].booking_type = booking_type
    
    def delete_booking(self, index: int, start_time: int) -> None:
        roomToDelete = self.daily_bookings.access_at_index(index)
        if roomToDelete is not None: #same as above
            roomToDelete.hourly_bookings[start_time].booker_name = "None"
            roomToDelete.hourly_bookings[start_time].booking_type = "Vacant"

class HourlyBooking:
    def __init__(self, start_time: int, end_time: int, booker_name: str = "None", booking_type: str = "Vacant") -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.booker_name = booker_name
        self.booking_type = booking_type
    
    def update_booking(self, booker_name: str, booking_type: str) -> None:
        self.booker_name = booker_name
        self.booking_type = booking_type

class DailyBooking:
    times: list[str] = helper_build_times(48) # made times a class attribute of dailybooking instead of a global variable
    def __init__(self) -> None:
        self.hourly_bookings:list[HourlyBooking] = []
        for i in range(len(DailyBooking.times)-1): # 24/48 gives half hour incrmeents
            startTime = time_str_to_float(DailyBooking.times[i])
            endTime = time_str_to_float(DailyBooking.times[i+1])
            self.hourly_bookings.append(HourlyBooking(int(startTime), int(endTime)))
