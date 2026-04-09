import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import BookingSystem.room_booking
import random
import NavigationSystem.traversal as tv
from ServiceSystem.service_queue import ServiceRequest as requests
from ServiceSystem.service_queue import ServiceRequest
import DataStructures.AVL as avl

BOOKING_DAYS = 30

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
        self.service_queue = ServiceRequests()
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


        ROOM_TYPES = ["Lecture Hall", "Lab", "Office", "Study Room", "Conference Room", "Washroom"]
        self.pathways = [
            Pathway(0,   Location(125, 582)),
            Pathway(1,   Location(178, 596)),
            Pathway(2,   Location(167, 509)),
            Pathway(3,   Location(139, 455)),
            Pathway(4,   Location(196, 459)),
            Pathway(5,   Location(222, 586)),
            Pathway(6,   Location(208, 512)),
            Pathway(7,   Location(275, 449)),
            Pathway(8,   Location(267, 508)),
            Pathway(9,   Location(273, 577)),
            Pathway(10,  Location(325, 425)),
            Pathway(11,  Location(301, 528)),
            Pathway(12,  Location(347, 519)),
            Pathway(13,  Location(387, 519)),
            Pathway(14,  Location(409, 489)),
            Pathway(15,  Location(451, 489)),
            Pathway(16,  Location(492, 491)),
            Pathway(17,  Location(526, 466)),
            Pathway(18,  Location(515, 439)),
            Pathway(19,  Location(492, 417)),
            Pathway(20,  Location(563, 463)),
            Pathway(21,  Location(602, 449)),
            Pathway(22,  Location(633, 429)),
            Pathway(23,  Location(628, 410)),
            Pathway(24,  Location(609, 396)),
            Pathway(25,  Location(598, 378)),
            Pathway(26,  Location(589, 352)),
            Pathway(27,  Location(571, 321)),
            Pathway(28,  Location(656, 399)),
            Pathway(29,  Location(644, 382)),
            Pathway(30,  Location(633, 367)),
            Pathway(31,  Location(601, 300)),
            Pathway(32,  Location(596, 272)),
            Pathway(33,  Location(552, 277)),
            Pathway(34,  Location(609, 245)),
            Pathway(35,  Location(608, 218)),
            Pathway(36,  Location(653, 198)),
            Pathway(37,  Location(647, 229)),
            Pathway(38,  Location(668, 252)),
            Pathway(39,  Location(684, 223)),
            Pathway(40,  Location(682, 269)),
            Pathway(41,  Location(729, 280)),
            Pathway(42,  Location(735, 301)),
            Pathway(43,  Location(721, 329)),
            Pathway(44,  Location(689, 339)),
            Pathway(45,  Location(765, 315)),
            Pathway(46,  Location(770, 348)),
            Pathway(47,  Location(772, 375)),
            Pathway(48,  Location(803, 376)),
            Pathway(49,  Location(800, 293)),
            Pathway(50,  Location(858, 286)),
            Pathway(51,  Location(876, 258)),
            Pathway(52,  Location(889, 288)),
            Pathway(53,  Location(900, 315)),
            Pathway(54,  Location(889, 346)),
            Pathway(55,  Location(873, 371)),
            Pathway(56,  Location(918, 358)),
            Pathway(57,  Location(957, 358)),
            Pathway(58,  Location(973, 382)),
            Pathway(59,  Location(975, 410)),
            Pathway(60,  Location(962, 432)),
            Pathway(61,  Location(946, 464)),
            Pathway(62,  Location(917, 477)),
            Pathway(63,  Location(893, 467)),
            Pathway(64,  Location(888, 447)),
            Pathway(65,  Location(869, 434)),
            Pathway(66,  Location(799, 439)),
            Pathway(67,  Location(812, 466)),
            Pathway(68,  Location(791, 498)),
            Pathway(69,  Location(760, 523)),
            Pathway(70,  Location(731, 510)),
            Pathway(71,  Location(726, 481)),
            Pathway(72,  Location(771, 476)),
            Pathway(73,  Location(756, 459)),
            Pathway(74,  Location(506, 297)),
            Pathway(75,  Location(481, 316)),
            Pathway(76,  Location(449, 336)),
            Pathway(77,  Location(468, 369)),
            Pathway(78,  Location(419, 311)),
            Pathway(79,  Location(380, 306)),
            Pathway(80,  Location(351, 299)),
            Pathway(81,  Location(313, 315)),
            Pathway(82,  Location(279, 322)),
            Pathway(83,  Location(247, 323)),
            Pathway(84,  Location(219, 327)),
            Pathway(85,  Location(200, 354)),
            Pathway(86,  Location(198, 389)),
            Pathway(87,  Location(202, 423)),
            Pathway(88,  Location(371, 404)),
            Pathway(89,  Location(385, 365)),
            Pathway(90,  Location(412, 339)),
            Pathway(91,  Location(386, 450)),
            Pathway(92,  Location(478, 513)),
            Pathway(93,  Location(309, 588)),
            Pathway(94,  Location(365, 589)),
            Pathway(95,  Location(425, 591)),
            Pathway(96,  Location(467, 552)),
            Pathway(97,  Location(477, 589)),
            Pathway(98,  Location(522, 590)),
            Pathway(99,  Location(567, 590)),
            Pathway(100, Location(612, 576)),
            Pathway(101, Location(657, 588)),
            Pathway(102, Location(709, 581)),
            Pathway(103, Location(728, 552)),
            Pathway(104, Location(608, 536)),
            Pathway(105, Location(645, 512)),
            Pathway(106, Location(523, 540)),
            Pathway(107, Location(657, 161)),
            Pathway(108, Location(699, 167)),
            Pathway(109, Location(753, 240)),
            Pathway(110, Location(761, 189)),
            Pathway(111, Location(432, 280)),
            Pathway(112, Location(429, 253)),
            Pathway(113, Location(434, 228)),
            Pathway(114, Location(475, 223)),
            Pathway(115, Location(503, 198)),
            Pathway(116, Location(522, 160)),
            Pathway(117, Location(562, 128)),
            Pathway(118, Location(616, 123)),
        ]

        data = [
            ("AB",   "Art Building & Parkade",                      688, 534),
            ("AD",   "Administration",                              821, 335),
            ("AU",   "Aurora Hall",                                  510, 564),
            ("BI",   "Biological Sciences",                         886, 216),
            ("CC",   "Child Care Centre",                           932, 326),
            ("CCIT", "Calgary Centre for Innovative Technology",    539, 181),
            ("CD",   "Cascade Hall",                                362, 488),
            ("CDC",  "Child Development Centre",                     77, 571),
            ("CH",   "Craigie Hall",                                722, 454),
            ("CR",   "Crowsnest Hall",                              470, 276),
            ("CSSH", "Cenovus Spo'pi Solar House",                  536, 230),
            ("DC",   "Dining Centre",                               532, 502),
            ("EDC",  "Education Classrooms",                        839, 441),
            ("EDT",  "Education Tower",                             867, 417),
            ("EEEL", "Energy Environment Experiential Learning",    690, 142),
            ("ENA",  "Engineering Block A",                         631, 204),
            ("ENB",  "Engineering Block B",                         626, 164),
            ("ENC",  "Engineering Block C",                         605, 139),
            ("ES",   "Earth Sciences",                              733, 198),
            ("GL",   "Glacier Hall",                                425, 516),
            ("GR",   "Grounds Building",                            461, 481),
            ("GS",   "General Services Building",                    73, 474),
            ("HNSC", "Hunter Student Commons",                      731, 352),
            ("HP",   "Heating Plant",                               307, 555),
            ("ICT",  "Information & Communications Technology",     677, 194),
            ("KNA",  "Kinesiology Block A",                         565, 408),
            ("KNB",  "Kinesiology Block B",                         528, 354),
            ("MEB",  "Suncor Energy Centre for Applied Research",   685,  64),
            ("MF",   "Materials Handling",                          705, 318),
            ("MFH",  "Murray Fraser Hall",                          765, 415),
            ("MH",   "MacEwan Hall",                                672, 299),
            ("MS",   "Mathematical Sciences",                       781, 211),
            ("MSC",  "MacKimmie Library Block",                     616, 335),
            ("MTH",  "Mathison Hall",                               921, 431),
            ("OL",   "Olympus Hall",                                484, 395),
            ("OO",   "Olympic Oval",                                437, 416),
            ("PF",   "Professional Faculties",                      815, 401),
            ("PP",   "Physical Plant",                              99, 545),
            ("RC",   "Rozsa Centre",                                631, 462),
            ("RT",   "Reeve Theatre",                               658, 467),
            ("RU",   "Rundle Hall",                                 570, 561),
            ("SH",   "Scurfield Hall",                              916, 404),
            ("SS",   "Social Sciences",                             827, 275),
            ("ST",   "Science Theatres",                            818, 232),
            ("TFDL", "Taylor Family Digital Library",               688, 368),
            ("TI",   "Taylor Teaching Institute",                   639, 266),
        ]

        services_data = [
            ("Cafe",            ["MH", "TFDL", "HNSC", "ICT", "SH"]),
            ("Printing",        ["TFDL", "ICT", "MFH", "SS"]),
            ("ATM",             ["MH", "SH", "DC", "PF"]),
            ("Gym",             ["KNA", "KNB", "OO"]),
            ("Library",         ["TFDL", "MSC", "MFH"]),
            ("Food Court",      ["DC", "MH", "HNSC"]),
            ("Study Rooms",     ["TFDL", "ICT", "MS", "SS", "MFH"]),
            ("Bookstore",       ["MH"]),
            ("Health Centre",   ["MH", "PF"]),
            ("IT Support",      ["ICT", "CCIT", "TFDL"]),
            ("Bike Racks",      ["ICT", "BI", "ES", "KNA", "SS"]),
            ("Parking",         ["AB", "MSC", "OO", "KNA"]),
        ]
        self.buildings = {}
        for bid, name, lat, lon in data:
            new_building = Building(name,bid,Location(lat,lon))
            self.add_building(random.randint(2, 6),random.randint(5, 20),new_building)
            for sname, bids in services_data:
                if bid in bids:
                    new_building.services.append(sname)
            #self.buildings[bid] = b



        self.services = {}
        for sname, bids in services_data:
            self.services[sname] = [self.buildings[b] for b in bids]


    def init_graph(self):
        for i in self.pathways:
            self.campus_graph.append_node(i.node)
        for i in self.buildings.values():
            self.campus_graph.append_node(i.node)


        self.campus_graph.node_linker(self.campus_graph.get_node_id("AB"),[100,101,102,103,70,71,105,104])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("AD"),[46,47,48,45,49,55,50])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("AU"),[96,106,97,98,99])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("BI"),[51,110])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CC"),[54,56,57,53])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CCIT"),[116,115])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CD"),[12,13,14])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CDC"),[0])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CH"),[73,71])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CR"),[75,76,74,111,112])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("CSSH"),[33,115])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("DC"),[17,20,106,16,104])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("EDC"),[66,67,65])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("EDT"),[65,55])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("EEEL"),[107,108,110])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("ENA"),[35,37,36])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("ENB"),[107])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("ENC"),[118])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("ES"),[110,108,39])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("GL"),[13,14,15,92])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("GR"),[15,16,14])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("GS"),[3,2])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("HNSC"),[44,43,46,47])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("HP"),[93,9,11])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("ICT"),[107,108,36,39])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("KNA"),[19,18,23,24,25])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("KNB"),[77,75,27])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MEB"),[118,107])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MF"),[44])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MFH"),[66,47,73])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MH"),[44,43,40])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MS"),[110,109])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MSC"),[30,26,31])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("MTH"),[61,62,63,60])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("OL"),[77,19])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("OO"),[90,77,19])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("PF"),[48,66])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("PP"),[0,2])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("RC"),[22,21,105])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("RT"),[105,22])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("RU"),[99,106,100,104,98])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("SH"),[56,57,58,59,50])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("SS"),[49,50])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("ST"),[109,49])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("TFDL"),[44,30,29,28])
        self.campus_graph.node_linker(self.campus_graph.get_node_id("TI"),[31,32,38,40])


        self.campus_graph.node_linker(1,[0])
        self.campus_graph.node_linker(2,[3,2,6,4])
        self.campus_graph.node_linker(4,[3,2,87,7])
        self.campus_graph.node_linker(5,[8,6,1])
        self.campus_graph.node_linker(6,[2,8,4,3])
        self.campus_graph.node_linker(7,[87,4,10,8])
        self.campus_graph.node_linker(7,[87,4,10,8])
        self.campus_graph.node_linker(8,[1,9,6,5])
        self.campus_graph.node_linker(9,[11,5,8])
        self.campus_graph.node_linker(10,[88,7])
        self.campus_graph.node_linker(11,[8])
        self.campus_graph.node_linker(12,[11,93])
        self.campus_graph.node_linker(13,[12,95])
        self.campus_graph.node_linker(14,[13,91])
        self.campus_graph.node_linker(15,[14,92])
        self.campus_graph.node_linker(16,[15,92])
        self.campus_graph.node_linker(17,[16,20])
        self.campus_graph.node_linker(18,[17])
        self.campus_graph.node_linker(19,[18])
        self.campus_graph.node_linker(20,[17])
        self.campus_graph.node_linker(21,[20])
        self.campus_graph.node_linker(22,[21])
        self.campus_graph.node_linker(23,[22,24,28])
        self.campus_graph.node_linker(24,[23,29])
        self.campus_graph.node_linker(25,[26,24,23])
        self.campus_graph.node_linker(26,[27])
        self.campus_graph.node_linker(30,[25,24,29])
        self.campus_graph.node_linker(31,[27,32])
        self.campus_graph.node_linker(32,[31,33])
        self.campus_graph.node_linker(33,[74,27,36])
        self.campus_graph.node_linker(34,[35,32])
        self.campus_graph.node_linker(36,[37,107])
        self.campus_graph.node_linker(37,[34,35,36])
        self.campus_graph.node_linker(38,[39,37])
        self.campus_graph.node_linker(40,[38,39])
        self.campus_graph.node_linker(41,[42,40])
        self.campus_graph.node_linker(41,[42])
        self.campus_graph.node_linker(42,[43,45])
        self.campus_graph.node_linker(43,[44])
        self.campus_graph.node_linker(44,[43,73,30])
        self.campus_graph.node_linker(45,[49,46])
        self.campus_graph.node_linker(46,[47,48])
        self.campus_graph.node_linker(47,[48])
        self.campus_graph.node_linker(49,[50,55])
        self.campus_graph.node_linker(50,[51,52])
        self.campus_graph.node_linker(51,[110,52])
        self.campus_graph.node_linker(52,[53])
        self.campus_graph.node_linker(53,[54,56])
        self.campus_graph.node_linker(54,[56,55])
        self.campus_graph.node_linker(55,[64])
        self.campus_graph.node_linker(56,[57])
        self.campus_graph.node_linker(57,[58])
        self.campus_graph.node_linker(58,[59])
        self.campus_graph.node_linker(59,[60])
        self.campus_graph.node_linker(60,[61])
        self.campus_graph.node_linker(61,[62])
        self.campus_graph.node_linker(62,[63])
        self.campus_graph.node_linker(63,[67])
        self.campus_graph.node_linker(64,[63,65])
        self.campus_graph.node_linker(66,[73,72])
        self.campus_graph.node_linker(67,[66,68,72,73])
        self.campus_graph.node_linker(68,[69,70])
        self.campus_graph.node_linker(70,[103,71,69])
        self.campus_graph.node_linker(71,[73,70,105])
        self.campus_graph.node_linker(71,[105,70,69])
        self.campus_graph.node_linker(72,[68])
        self.campus_graph.node_linker(73,[71,72])
        self.campus_graph.node_linker(75,[111,74])
        self.campus_graph.node_linker(76,[75,77])
        self.campus_graph.node_linker(77,[19])
        self.campus_graph.node_linker(78,[111,90,76])
        self.campus_graph.node_linker(79,[80,78,90,89,111,112])
        self.campus_graph.node_linker(80,[8,113,112,111])
        self.campus_graph.node_linker(81,[82])
        self.campus_graph.node_linker(82,[83])
        self.campus_graph.node_linker(83,[84])
        self.campus_graph.node_linker(85,[84])
        self.campus_graph.node_linker(86,[85])
        self.campus_graph.node_linker(87,[86,7])
        self.campus_graph.node_linker(88,[91])
        self.campus_graph.node_linker(89,[88])
        self.campus_graph.node_linker(90,[89])
        self.campus_graph.node_linker(93,[9])
        self.campus_graph.node_linker(94,[93,12])
        self.campus_graph.node_linker(95,[94,13])
        self.campus_graph.node_linker(96,[92])
        self.campus_graph.node_linker(97,[96,95,106])
        self.campus_graph.node_linker(98,[106,99])
        self.campus_graph.node_linker(99,[100,104,98,106])
        self.campus_graph.node_linker(100,[104,101,99,105])
        self.campus_graph.node_linker(101,[100,102])
        self.campus_graph.node_linker(102,[101,103])
        self.campus_graph.node_linker(103,[102,70,69])
        self.campus_graph.node_linker(104,[105,11,106,99])
        self.campus_graph.node_linker(105,[71,104,20,21])
        self.campus_graph.node_linker(107,[108,36])
        self.campus_graph.node_linker(108,[110])
        self.campus_graph.node_linker(109,[41])
        self.campus_graph.node_linker(110,[109,51])
        self.campus_graph.node_linker(111,[112,78,75,76])
        self.campus_graph.node_linker(112,[113])
        self.campus_graph.node_linker(113,[114])
        self.campus_graph.node_linker(114,[115])
        self.campus_graph.node_linker(115,[74,116])
        self.campus_graph.node_linker(116,[117])
        self.campus_graph.node_linker(118,[117,107,108])
        




    

        








