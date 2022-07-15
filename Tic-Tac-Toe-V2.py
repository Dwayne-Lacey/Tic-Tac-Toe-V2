import tkinter
import random

# Node to contain X/O/Blank labels to display in the UI
class Node:
    def __init__(self, node_number, player_shape=None):
        self.value = None
        self.image = None
        self.node_number = node_number
        self.shape = player_shape
        self.edges = {}
    
    def add_edge(self, to_node, edge_weight):
        self.edges[to_node] = edge_weight

class Graph:
    def __init__(self):
        graph_nodes = {}
    
    # Connects nodes within graph
    def add_node(self, from_node, to_node, edge_weight):
        from_node.add_node(to_node, edge_weight)
        to_node.add_node(from_node, edge_weight)

    def build_graph(self):
        node_queue = []
        

