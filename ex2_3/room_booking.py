import DataStructures.LiFo_ringBuffer as lifo
import numpy as np

def time_str_to_float(t):
    h, m = map(int, t.split(":"))
    return h + m / 60  # 12:30 → 12.5, 13:00 → 13.0
class user_booking:
    def __init__(self,user_id,name,time,comments):
        self.id = user_id
        self.name = name
        self.time = time
        self.comments = comments
        pass

class daily_booking:
    def __init__(self):
        self.buffer = [None] * 48
        pass
    def add_booking(self,user_booking:user_booking):
        if self.buffer[(int)(np.floor(user_booking.time * 2))] != None:
            print("room Already Booked")
            return None   
        self.buffer[(int)(np.floor(user_booking.time * 2))] = user_booking
        return (int)(np.floor(user_booking.time * 2))

    def remove_booking(self,time):
        if self.buffer[(int)(np.floor(time * 2))] == None:
            print("No Booking Exists")
            return None   
        self.buffer[(int)(np.floor(time * 2))] = None
        return (int)(np.floor(time * 2))

    def get_booking_with_user_booking(self,user_booking):
        if self.buffer[(int)(np.floor(user_booking.time * 2))] != None:
            print("No Booking exists")
            return None   
        return self.buffer[(int)(np.floor(user_booking.time * 2))]

    def get_booking_with_time(self,time):
        if self.buffer[(int)(np.floor(time * 2))] != None:
            print("No Booking Exists")
            return None   
        return self.buffer[(int)(np.floor(time * 2))]
    def get_all_bookings(self):
        return self.buffer.copy()
    
class booking_system:
    def __init__(self,size):
        self.buffer = lifo.ring_buffer(size,daily_booking)
        pass

    def book_room(self,day,id,name,time,comments):
        temp_user_booking = user_booking(id,name,time,comments)
        if day > self.buffer.capacity:
            print("The System Can Only Book ",self.buffer.capacity," Days In The Future")
            return None
        buffer_cell:daily_booking = self.buffer.access_at_index(day)
        return buffer_cell.add_booking(temp_user_booking)
    
    def delete_booking(self,day,time):
        buffer_cell:daily_booking = self.buffer.access_at_index(day)
        return buffer_cell.remove_booking(time)
    
    def get_daily_booking(self,day,start_time:float = 0.0,end_time:float = 24.0):
        if start_time == None:
            start_time = 0.0
        else:
            start_time = time_str_to_float(start_time)
        if end_time == None:
            end_time = 24.0
        else:
            end_time = time_str_to_float(end_time)

        buffer_cell:daily_booking = self.buffer.access_at_index(day)
        all_bookings = buffer_cell.get_all_bookings()
        return_val = []
        for i in range((int)(np.round(start_time*2)),(int)(np.round(end_time*2))):
            if type(all_bookings[i]) == user_booking:
                return_val.append(all_bookings[i])
            else:
                return_val.append(user_booking(None,None,i/2,""))
                pass
        return return_val
    def print_daily_booking(self,day,start_time:float = 0.0,end_time:float = 24.0):
        if start_time == None:
            start_time = 0.0
        if end_time == None:
            end_time = 24.0
        buffer_cell:daily_booking = self.buffer.access_at_index(day)
        all_bookings = buffer_cell.get_all_bookings()
        for i in range((int)(np.round(start_time*2)),(int)(np.round(end_time*2))):
            if type(all_bookings[i]) == user_booking:
                print("Day : ",day," - Time :",all_bookings[i].time," Is Booked By : ",all_bookings[i].name,)
            else:
                print("Day : ",day," - Time :",i/2, " Is Open")
                pass


if False:
    test_bookingSystem = booking_system(90)

    test_booking = user_booking(535,"TEST", 12.5,"Dummy Comment")
    test_booking1 = user_booking(535,"TEST2", 12.5,"Dummy Comment")
    test_booking2 = user_booking(535,"TEST3", 13,"Dummy Comment")
    test_booking2 = user_booking(535,"TEST3", 23.5,"Dummy Comment")
    test_bookingSystem.book_room(5,test_booking)
    test_bookingSystem.book_room(5,test_booking1)
    test_bookingSystem.book_room(5,test_booking2)
    test_bookingSystem.print_daily_booking(5)
    test_bookingSystem.print_daily_booking(10)