import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import tkinter as tk
from tkinter import ttk
import random as rd
import DataStructures.LifoRingBuffer as lifo
import RequestPipeline.request_pipeline as rp
import DataStructures.AVL as avl


def helper_build_times(total_increments):
    times = []
    splits = 24/total_increments
    for i in range(total_increments+1):
        miniutes = 0
        hours = i * splits
        if hours != 0:
            miniutes = (hours*60) % 60
        hours = np.floor(i * splits)
        times.append(f"{int(hours):02d}:{(int)(miniutes):02d}")
    return(times)
times = helper_build_times(48)


class CampusWraper():
    def __init__(self,building,floor,room,data = FileNotFoundError):
        self.building = building
        self.floor = floor
        self.room = room
        self.data = data

def time_str_to_float(t):
    h, m = map(int, t.split(":"))
    return h + m / 60  # 12:30 → 12.5, 13:00 → 13.0

booking_search = avl.AVLTree()

class BookingSystem:
    def __init__(self,capacity):
        self.daily_bookings = lifo.LifoRingBuffer(capacity,DailyBooking) #90 day capacity
        self.capacity = capacity
    
    def get_daily_booking(self,index):
        return self.daily_bookings.access_at_index(index)
    
    def book_room(self,index,start_time,booker_name,booking_type):
        booking = self.daily_bookings.access_at_index(index).hourly_booking[start_time]
        booking.booker_name = booker_name
        booking.booking_type = booking_type
        booking_search.insert(avl.Node(avl.hash_str_to_int(booker_name),self))
    def delete_booking(self,index,start_time):
        booking = self.daily_bookings.access_at_index(index).hourly_booking[start_time]
        booking_search.delete(avl.hash_str_to_int(booking.booker_name))
        booking.booker_name = "None"
        booking.booking_type = "Vacant"


class HourlyBooking:
    def __init__(self,start_time,end_time,booker_name = "None",booking_type="Vacant"):
        self.start_time = start_time
        self.end_time =end_time
        self.booker_name = booker_name
        self.booking_type = booking_type
    def update_booking(self,booker_name, booking_type,campus_info):
        if booker_name == None:
            booking_search.delete(avl.hash_str_to_int(self.booker_name))
        else:
            campus_info.data = self
            booking_search.insert(avl.Node(avl.hash_str_to_int(booker_name),campus_info))
        self.booker_name = booker_name
        self.booking_type = booking_type
class DailyBooking:
    def __init__(self):
        global times
        self.hourly_bookings = []
        for i in range(len(times)-1): # 24/48 gives half hour incrmeents
            self.hourly_bookings.append(HourlyBooking(times[i],times[i+1],None))
