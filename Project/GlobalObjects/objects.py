import sys
import os
from pathlib import Path                   
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
import BookingSystem.room_booking
import random
import NavigationSystem.traversal as tv
from ServiceSystem.service_queue import ServiceRequest as requests
from ServiceSystem.service_queue import ServiceRequest
import DataStructures.AVL as avl
import json
BOOKING_DAYS = 30

CAMPUS_DATA = PROJECT_ROOT / "GlobalObjects"  / "campus_data.json"
class Room:
    def __init__(self,id,room_type):
        self.id = id
        self.booking = BookingSystem.room_booking.BookingSystem(BOOKING_DAYS)
        self.info = "Blank"
        self.room_type = room_type
    def edit_booking(self,booking,info):
        pass
    def get_info(self):
        return f"Room :{self.id} is of type {self.room_type}. Additional Info: {self.info}"

class Floor:

    def __init__(self,id):
        self.rooms = []
        self.id = id

class Location:
    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
 
class Building:
    def __init__(self, name: str,bid :str, location: Location):
        self.name = name
        self.bid = bid
        self.floors = []
        self.node = tv.Node(bid,location.x_position,location.y_position)
        self.node = tv.Node(bid,location.x_position,location.y_position)
        self.services = []
    def get_info(self):
        return f"Building Name:{self.name} - ID:{self.bid}. Has {len(self.floors)} Floors With Avaiable Serives {self.services}"
 
class Pathway:
    def __init__(self,id,location:Location):
        self.node = tv.Node(id,location.x_position,location.y_position)
        self.node = tv.Node(id,location.x_position,location.y_position)

class Campus:
    def __init__(self):
        self.buildings = {}
        self.pathways = None
        self.services = {}
        self.init_ucalgary()
        self.campus_graph = tv.graph()
        self.init_graph()
        self.requests = requests
        self.lookup = avl.AVLTree()
        self.service_queue = ServiceRequest()
        self.completed_services = []

    def get_building_keys(self):
        return self.buildings.keys()
    def get_buildings(self):
        return self.buildings
    def get_service_keys(self):
        return self.services.keys()
    def get_services(self):
        return self.services
    def get_floors(self,key):
        return self.buildings[key].floors
    def get_rooms(self,building_key,floor_id):
        floor_id = (int)(floor_id)
        print(floor_id)
        return (self.buildings[building_key].floors)[int(floor_id)].rooms
    



    def get_bookings(self,building_key,floor_id,room_id,day,start_time,end_time):
        bookings = ((self.buildings[building_key].floors)[int(floor_id)].rooms)[int(room_id)].booking
        if bookings == None:
            return None
        daily_bookings = bookings.get_daily_booking(day)
        print(start_time," ",end_time)
        return daily_bookings.hourly_bookings[start_time:end_time]
    
    def add_serivce(self,service,building):
        if service not in self.services.keys():
            self.services[service] = []
        
        if building not in self.services[service] and building in self.buildings.keys():
            instance = self.get_buildings()[building]
            self.services[service].append(instance)
            self.buildings[building].services.append(service)
        else:
            print("Add Service Error")
            return None
        
    def delete_service(self,service,building):
        if service not in self.services.keys():
            print("Service Does Not Exist")
            return
        print(self.services[service])
        instance = self.get_buildings()[building]
        self.services[service].remove(instance)
        print(self.services[service])
        self.buildings[building].services.remove(service)
 
    def add_building(self,floors,rooms,building:Building):
        room_choices = ["Study","Confrense","Washroom","ClassRoom","Janitorial"]
        for i in range(floors):
            f = Floor(i)
            for k in range(rooms):
                f.rooms.append(Room(k,random.choice(room_choices)))
            building.floors.append(f)
        self.buildings[building.bid] = building



    def remove_building(self,building:Building):
        deleted_building = self.get_buildings()[building.bid]
        self.buildings.pop(building.bid)


    def init_ucalgary(self):
        with open(CAMPUS_DATA, "r") as f:
            data = json.load(f)

        ROOM_TYPES = ["Lecture Hall", "Lab", "Office", "Study Room", "Conference Room", "Washroom"]

        self.pathways = [
            Pathway(p["id"], Location(p["x"], p["y"]))
            for p in data["pathways"]
        ]

        self.buildings = {}
        for b in data["buildings"]:
            new_building = Building(b["name"], b["bid"], Location(b["x"], b["y"]))
            self.add_building(random.randint(2, 6), random.randint(5, 20), new_building)
            new_building.services = b["services"]

        self.services = {}
        for sname, bids in data["services"].items():
            self.services[sname] = [self.buildings[bid] for bid in bids]


    def init_graph(self):
        for i in self.pathways:
            self.campus_graph.append_node(i.node)
        for i in self.buildings.values():
            self.campus_graph.append_node(i.node)

        with open(CAMPUS_DATA, "r") as f:
            data = json.load(f)

        for entry in data["edges"]:
            node_id = entry["node"] if isinstance(entry["node"], int) else self.campus_graph.get_node_id(entry["node"])
            self.campus_graph.node_linker(node_id, entry["links"])