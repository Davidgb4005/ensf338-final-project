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
from Config import config


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
times = helper_build_times(config.TIME_INCREMENTS)


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
        booking_search.insert_visu(avl.Node(avl.hash_str_to_int(booker_name),self))
    def book_avl_room(self,index,start_time,booker_name,booking_type):
        booking = self.daily_bookings.access_at_index(index).hourly_booking[start_time]
        booking.booker_name = booker_name
        booking.booking_type = booking_type
        booking_search.insert(avl.Node(avl.hash_str_to_int(booker_name),self))
    def delete_booking(self,index,start_time):
        booking = self.daily_bookings.access_at_index(index).hourly_booking[start_time]
        booking_search.delete(avl.hash_str_to_int(booking.booker_name))
        booking.booker_name = "None"
        booking.booking_type = "Vacant"
    def delete_avl_booking(self,index,start_time):
        booking = self.daily_bookings.access_at_index(index).hourly_booking[start_time]
        booking_search.delete_visu(avl.hash_str_to_int(booking.booker_name))
        booking.booker_name = "None"
        booking.booking_type = "Vacant"


class HourlyBooking:
    def __init__(self,start_time,end_time,booker_name = "None",booking_type="Vacant"):
        self.start_time = start_time
        self.end_time =end_time
        self.booker_name = booker_name
        self.booking_type = booking_type
    def update_booking(self,booker_name, booking_type,campus_info,booking=None):
        if booker_name == None:
            booking_search.delete(avl.hash_str_to_int(self.booker_name),booking)
        else:
            campus_info.data = self
            booking_search.insert(avl.Node(avl.hash_str_to_int(booker_name),campus_info))
        self.booker_name = booker_name
        self.booking_type = booking_type
    def update_booking_avl(self,booker_name, booking_type,campus_info,booking=None):
        if booker_name == None:
            booking_search.delete_visu(avl.hash_str_to_int(self.booker_name),booking)
        else:
            campus_info.data = self
            booking_search.insert_visu(avl.Node(avl.hash_str_to_int(booker_name),campus_info))
        self.booker_name = booker_name
        self.booking_type = booking_type


BOOKER_NAMES = [
    "Alice Johnson", "Bob Smith", "Carol White", "David Lee", "Emma Davis",
    "Frank Miller", "Grace Wilson", "Henry Moore", "Isabel Taylor", "Jack Brown",
    "Karen Clark", "Liam Harris", "Mia Lewis", "Noah Walker", "Olivia Hall",
    "Paul Allen", "Quinn Young", "Rachel King", "Sam Wright", "Tina Scott",
    "Uma Patel", "Victor Chen", "Wendy Adams", "Xavier Brooks", "Yara Nasser",
    "Zane Cooper", "Amy Turner", "Ben Foster", "Chloe Reed", "Dylan Morgan",
    "Ella Barnes", "Finn Hughes", "Gina Powell", "Hank Russell", "Iris Jenkins",
    "Jake Perry", "Lily Sanders", "Max Coleman", "Nina Bryant", "Oscar Diaz",
    "Petra Flynn", "Quincy Moss", "Rosa Chambers", "Seth Nguyen", "Tara Fleming",
    "Ulric Stone", "Vera Haynes", "Wade Griffith", "Xena Caldwell", "Yusuf Okafor",
    "Zara Whitfield", "Aaron Simmons", "Bella Cross", "Carlos Vega", "Diana Hunt",
    "Ethan Long", "Fiona Marsh", "Gareth Price", "Hannah Gore", "Ivan Dean"
]
BOOKING_TYPES = ["Study", "Conference", "Lecture", "Lab Session", "Office Hours", "Meeting", "Exam Review"]

class DailyBooking:
    def __init__(self, fill_random=True, campus_info=None):
        global times
        self.hourly_bookings = []
        available_names = BOOKER_NAMES.copy()
        rd.shuffle(available_names)
        for i in range(len(times) - 1):
            if fill_random and available_names and rd.random() < config.BOOKING_DENSITY:
                name = available_names.pop()
                btype = rd.choice(BOOKING_TYPES)
                self.hourly_bookings.append(HourlyBooking(times[i], times[i+1], name, btype))
                if config.DEMO_POPULATE_AVL:
                    booking_search.insert(avl.Node(avl.hash_str_to_int(name), campus_info))
            else:
                self.hourly_bookings.append(HourlyBooking(times[i], times[i+1], None, "Vacant"))
    
def print_daily_booking(booking:CampusWraper):
    print("Building: ",booking.building," Floor: ",booking.floor," Room: ",booking.room)
    print("Name: ",booking.data.booker_name," Type: ",booking.data.booking_type," Start Time: ",booking.data.start_time," End Time: ",booking.data.end_time)