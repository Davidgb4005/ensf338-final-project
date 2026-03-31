import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import DataStructures.FiFo_ringBuffer as fifo
import DataStructures.LiFo_ringBuffer as lifo
import random as rd


class Campus:
    def __init__(self):
        self.buildings = [Building] # building_id -> Building
        self.pathways = ... # your chosen network representationV


    def get_room_list(self):
        pass
    def get_floor_list(self):
        pass
    def get_building_list(self):
        pass
    
    def get_bookings(self,building_id,floor_id,room_id):
        return self.buildings[building_id].floors[floor_id].rooms[room_id].bookings

class Room: #Provided By Assignemnt
    def __init__(self):
        self.bookings = None
        self.info = "Blank"

class Floor:
    def __init__(self):
        self.rooms = [Room]
class Location:
    def __init__(self,x_position,y_position):
        self.x_position = x_position
        self.y_position = y_position

class Building:
    def __init__(self, building_id : int,building_name: str, name: str, location: Location):
        self.building_id = building_id # e.g. unique ID
        self.building_name = building_name.lower() #e.g. "ICT"
        self.name = name # "Information and Comm. Tech."
        self.location = location # (lat, lon) or grid coords
        self.floors = [Floor] # room_id -> Room
    

#Building Helping Functions
def find_floor(building:Building,floor_number) -> Floor:
    floor_number = (int)(floor_number)
    return building.floors[floor_number]
#Floor Helper Funcitons
def find_room(floor : Floor,room_number) -> Room:
    room_number = (int)(room_number)
    return floor.rooms[room_number]
#Campus Helper Functions    
def find_building(campus:Campus,building_name:str= None,building_id:int = None) -> Building:
    if building_id != None:
        return campus.buildings.values(building_id)
    elif building_name != None:
        return campus.buildings[building_name]

def room_finder(campus:Campus,floor_number:int = None, room_number :int = None,building_name:str= None,building_id:int = None) -> list:
    floor = None
    room = None
    building = find_building(campus=campus,building_name=building_name,building_id=None)
    if floor_number != None:
        floor = find_floor(building,floor_number=floor_number)
        if room_number != None:
            room = find_room(floor,room_number=room_number)
    return [building,floor,room]


if False:
    room_types = ["Study","Confrense","Meeting","Lecture"]

    building_list = {}
    building_name_list = ["TFDL","ENG","ICT","SCA","SCB","SCT","MUFR","ADM","HSKYN","MAC"]
    building_count = 10

    floor_list = [] 
    floor_count = 15
    room_count = 40
    for k in range(building_count):
        building_list[building_name_list[k]] = (Building(k,building_name_list[k],building_name_list[k],[0,0]))
        for j in range(floor_count):
            building_list[building_name_list[k]].floors.append(Floor())
            floor_list.append(Floor())
            for i in range(room_count):
                building_list[building_name_list[k]].floors[j].rooms.append(Room(rd.randint(0,30),room_types[rd.randint(0,len(room_types)-1)]))
    for i in (building_list):
        print(i)
    campus = Campus()
    campus.buildings = dict(building_list)
