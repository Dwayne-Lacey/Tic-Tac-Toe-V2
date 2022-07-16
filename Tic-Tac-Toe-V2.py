import tkinter
import random

# Node to contain X/O/Blank labels to display in the UI
class Node:
    def __init__(self, node_num, player_shape=None):
        self.value = None
        self.image = None
        self.node_num = node_num
        self.shape = player_shape
        self.edges = {}
    
    def add_edge(self, to_node, edge_weight):
        self.edges[to_node] = edge_weight

class Graph:
    def __init__(self, graph_size):
        self.graph_nodes = {}
        self.graph_size = graph_size
    
    def build_graph(self):
        for row in range(1, self.graph_size + 1):
            for col in range(1, self.graph_size + 1):
                new_node = Node((row, col))
                self.graph_nodes[(row, col)] = new_node
    
    def print_graph(self):
        for key in self.graph_nodes.keys():
            print(key)

        

new_graph = Graph(3)
new_graph.build_graph()
new_graph.print_graph()