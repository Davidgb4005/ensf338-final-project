import sys
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from DataStructures.PriorityHeap import PriorityHeap as heapq
import itertools
import DataStructures.LifoRingBuffer as LiFo
import matplotlib.cm as cm

class Node:
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


def get_node_vector(origin_node: Node, target_node: Node):
    distance = np.sqrt((origin_node.x - target_node.x)**2 + (origin_node.y - target_node.y)**2)  # fix: missing **2
    angle = np.arctan2((origin_node.y - target_node.y), (origin_node.x - target_node.x)) * (180 / np.pi)
    return distance


def link_node(node_1: Node, node_2: Node):
    if node_1 == node_2 or node_1 in node_2.linked_nodes:
        print(f"Dont Try To Make Multiple Edges Between The Same Node {node_1.id} - {node_2.id}")
        return
        exit("Dont Try To Make Multiple Edges Between The Same Node")
    node_1.linked_nodes.append(node_2)
    node_2.linked_nodes.append(node_1)


class graph:
    def __init__(self):
        self.nodes = []       
        self.id_name_pair = {}
        self.total_nodes = 0
        self.undo_buffer = LiFo.LifoRingBuffer(10,None)

    def append_node(self, n: Node):
        n.id = self.total_nodes
        self.nodes.append(n)              
        self.id_name_pair[n.name] = n.id   
        self.total_nodes += 1

    def undo(self):
        if self.undo_buffer.items>0:
            fn = self.undo_buffer.pop()
            if fn != None:
                fn()
        else:
            print("Undo Que Empty")

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
        open_set = heapq()
        open_set.heapPush((get_node_vector(start,end), next(counter), start)) 

        while not open_set.isEmpty():
            result = open_set.heapPop()
            if result is None:
                break
            _, _, current = result
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return list(reversed(path))

            for neighbour in current.linked_nodes:
                edge_cost = get_node_vector(current, neighbour)
                tentative_g = g_score[current] + edge_cost

                if tentative_g < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g
                    f_score = tentative_g + get_node_vector(neighbour,end)
                    open_set.heapPush((f_score, next(counter), neighbour))

        return None

    def node_linker(self, origin_node: int, node_list: list[int]):
        for i in node_list:
            link_node(self.nodes[origin_node], self.nodes[i])

    def find_path_steps(self, start_node: int, end_node: int):
        start = self.nodes[start_node]
        end   = self.nodes[end_node]

        g_score = {n: float("inf") for n in self.nodes}
        g_score[start] = 0
        came_from = {}

        counter = itertools.count()
        open_set = heapq()
        open_set.heapPush((get_node_vector(start, end), next(counter), start))

        steps = []

        while not open_set.isEmpty():
            result = open_set.heapPop()
            if result is None:
                break
            _, _, current = result

            # compute f explicitly for clarity
            f_score_current = g_score[current] + get_node_vector(current, end)
            h_current = get_node_vector(current, end)

            steps.append({
                "current": current,
                "came_from": dict(came_from),
                "g": g_score[current],
                "h": h_current,
                "f": f_score_current
            })
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()

                final_g = g_score[end]
                final_f = final_g  # since h(end) = 0

                final_g = g_score[end]
                final_h = 0  # heuristic at goal is 0
                final_f = final_g

                steps.append({
                    "final_path": path,
                    "g": final_g,
                    "h": final_h,
                    "f": final_f
                })

                return path, steps

            for neighbour in current.linked_nodes:
                edge_cost = get_node_vector(current, neighbour)
                tentative_g = g_score[current] + edge_cost

                if tentative_g < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g
                    f_score = tentative_g + get_node_vector(neighbour, end)
                    open_set.heapPush((f_score, next(counter), neighbour))

        return None, steps
    

def draw_graph(nodes, img_path):
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.plot(nodes[0].x, nodes[0].y, "h", markersize=6,color="green")
    for i in range(len(nodes)-1):
        ax.annotate("", 
        xy=(nodes[i].x, nodes[i].y), 
        xytext=(nodes[i+1].x, nodes[i+1].y),
        arrowprops=dict(arrowstyle="-", color="black"))

        ax.plot(nodes[i+1].x, nodes[i+1].y, "bo", markersize=5)
        if nodes[i].name:
            ax.text(nodes[i].x, nodes[i].y, nodes[i].name, fontsize=6, color="blue")
    ax.plot(nodes[i+1].x, nodes[i+1].y, "*", markersize=6,color="yellow")

    plt.axis("off")
    plt.show()



def draw_graph_animated(nodes, img_path):
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)

    plt.axis("off")

    def update(frame):
        ax.clear()
        ax.imshow(img)
        plt.axis("off")

        # draw start node
        ax.plot(nodes[0].x, nodes[0].y, "h", markersize=6, color="green")

        # draw up to current frame
        for i in range(frame):
            ax.annotate("",
                xy=(nodes[i].x, nodes[i].y),
                xytext=(nodes[i+1].x, nodes[i+1].y),
                arrowprops=dict(arrowstyle="-", color="black")
            )
            ax.plot(nodes[i+1].x, nodes[i+1].y, "bo", markersize=5)

            if nodes[i].name:
                ax.text(nodes[i].x, nodes[i].y, nodes[i].name,
                        fontsize=6, color="blue")

        # final node highlight
        if frame > 0:
            ax.plot(nodes[frame].x, nodes[frame].y, "*",
                    markersize=6, color="yellow")

    ani = FuncAnimation(
        fig,
        update,
        frames=len(nodes),
        interval=300,   # ms between frames
        repeat=False
    )

    plt.show()



def animate_search(nodes, steps, img_path):
    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()

    def draw_path(came_from):
        for node, parent in came_from.items():
            ax.plot([node.x, parent.x], [node.y, parent.y], color="gray")

    def update(frame):
        ax.clear()
        ax.imshow(img)
        plt.axis("off")

        step = steps[frame]

        # draw explored tree
        if "came_from" in step:
            draw_path(step["came_from"])

        # current node
        if "current" in step:
            n = step["current"]
            h_val = step["h"]
            ax.plot(n.x, n.y, "ro", markersize=6)
            color = cm.viridis(h_val / 1000)  # normalize based on your scale

            ax.text(
                n.x + 5, n.y + 5,
                f"g={step['g']:.1f}\nh={step['h']:.1f}\nf={step['f']:.1f}",
                fontsize=7
            )
            
            ax.plot(n.x, n.y, "o", color=color, markersize=6)
            # display g and f near node
            ax.text(
                n.x + 5, n.y + 5,
                f"g={step['g']:.1f}\nf={step['f']:.1f}",
                fontsize=7,
                color="black"
            )

        # global counter (top-left)
        if "g" in step and "f" in step:
            ax.text(
                10, 20,
                f"Step: {frame}\n"
                f"g: {step['g']:.2f}\n"
                f"h: {step['h']:.2f}\n"
                f"f: {step['f']:.2f}",
                fontsize=10,
                bbox=dict(facecolor="white", alpha=0.7)
            )
        # final path
        if "final_path" in step:
            path = step["final_path"]
            for i in range(len(path) - 1):
                ax.plot(
                    [path[i].x, path[i+1].x],
                    [path[i].y, path[i+1].y],
                    color="yellow",
                    linewidth=2
                )



    ani = FuncAnimation(fig, update, frames=len(steps), interval=200, repeat=False)
    plt.show()
