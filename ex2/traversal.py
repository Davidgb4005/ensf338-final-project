import numpy as np
import heapq  ## THIS NEEDS OT BE A PYTHON IMPLEMENTAION
import itertools
import undo
class node:
    x = 0
    y = 0
    id = 0
    name = None
    linked_nodes = []

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.linked_nodes = []
    def print_info(self):
        print("Name : ",self.name," - ID : ",self.id)
    def print_linked_nodes(self):
        for i in self.linked_nodes:
            print(self.name," Linked To : ",i.name)


def get_node_vector(origin_node: node, target_node: node):
    distance = np.sqrt((origin_node.x - target_node.x)**2 + (origin_node.y - target_node.y)**2)  # fix: missing **2
    angle = np.arctan2((origin_node.y - target_node.y), (origin_node.x - target_node.x)) * (180 / np.pi)
    return distance


def link_node(node_1: node, node_2: node):
    if node_1 == node_2 or node_1 in node_2.linked_nodes:
        exit("Dont Try To Make Multiple Edges Between The Same Node")
    node_1.linked_nodes.append(node_2)
    node_2.linked_nodes.append(node_1)


class graph:
    def __init__(self):
        self.nodes = []       
        self.id_name_pair = {}
        self.total_nodes = 0
        self.undo_buffer = undo.ring_buffer(10,list)

    def append_node(self, n: node):
        n.id = self.total_nodes
        self.nodes.append(n)              
        self.id_name_pair[n.name] = n.id   
        self.total_nodes += 1

    def get_node_id(self, name: str):
        return self.id_name_pair[name]

    def get_node_name(self, id: int):
        return self.nodes[id]


    def find_path(self, start_node: int, end_node: int):
        start = self.nodes[start_node]
        end   = self.nodes[end_node]


        g_score = {n: float("inf") for n in self.nodes}
        g_score[start] = 0
        came_from = {}

        counter = itertools.count()  
        open_set = [(get_node_vector(start,end), next(counter), start)]  

        while open_set:
            _, _, current = heapq.heappop(open_set) 
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                self.undo_buffer.append_buffer(list(reversed(path)))
                return list(reversed(path))

            for neighbour in current.linked_nodes:
                edge_cost = get_node_vector(current, neighbour)
                tentative_g = g_score[current] + edge_cost

                if tentative_g < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g
                    f_score = tentative_g + get_node_vector(neighbour,end)
                    heapq.heappush(open_set, (f_score, next(counter), neighbour))

        return None

    def node_linker(self, origin_node: int, node_list: list[int]):
        for i in node_list:
            link_node(self.nodes[origin_node], self.nodes[i])

g = graph()
g.append_node(node("A", 0, 0))
g.append_node(node("B", 10, 1))
g.append_node(node("C", 0, 10))
g.append_node(node("D", 5, 9))
g.append_node(node("E", 4, 7))
g.append_node(node("F", 9, 17))
g.append_node(node("G", 5, 6))
g.append_node(node("H", 22, 21))

g.node_linker(0, [1,3,4])   # A -> B, A -> C
g.node_linker(1, [3,4,5,6])      # B -> D
g.node_linker(2, [3,4,7])      # C -> D

for i in g.nodes:
    i.print_linked_nodes()

path = g.find_path(0, 0)
if True: 
    path = g.find_path(0, 2)
    path = g.find_path(0, 1)
    path = g.find_path(0, 1)
    path = g.find_path(0, 1)
    path = g.find_path(0, 7)
#print(g.undo_buffer.peak())
while g.undo_buffer.items > 0:
    print([n.name for n in g.undo_buffer.pop()])  # ['A', 'C', 'D']

