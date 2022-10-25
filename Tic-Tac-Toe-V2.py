import tkinter as tk
import random

class Player():
    def __init__(self, name, avatar, marker, image):
        self.name = name
        self.avatar = avatar
        self.marker = marker
        self.win = False

class LLNode():
    def __init__(self, value):
        self.value = value
        self.next_node = None

class LinkedList():
    def __init__(self):
        self.head_node = None
        self.tail_node = None
    
    # Add node onto bottom of linked list
    def add_tail_node(self, value):
        if self.head_node == None:
            self.head_node = LLNode(value)
            self.tail_node = self.head_node
        
        else:
            node_to_add = LLNode(value)
            self.tail_node.next_node = node_to_add
            self.tail_node = node_to_add

    # Method to merge two linked lists into one linked list
    def merge_lists(self, secondary):
        self.tail_node.next_node = secondary.head_node
        self.tail_node = secondary.tail_node
    
    # Method to return and remove the head of a linked list
    def pop_node(self):
        if self.head_node == None:
            return None
        
        elif self.head_node == self.tail_node:
            node_to_return = self.head_node.value
            self.head_node, self.tail_node = None, None
            return node_to_return
        
        else:
            node_to_return = self.head_node.value
            self.head_node = self.head_node.next_node
            return node_to_return

class GNode():
    def __init__(self, coordinate):
        self.value = None
        self.image = None
        self.coordinate = coordinate

class Grid():
    def __init__(self):
        self.grid = {}
    
    # This method builds out the grid for the game to be played on
    def build_grid(self):
        for y in range(1, 4):
            for x in range(1, 4):
                self.grid[(y,x)] = GNode((y,x))
    
    # This method places a marker down on the player's chosen space
    def place_marker(self, player, coordinate):
        if self.grid[coordinate].value == None:
            self.grid[coordinate].value = player.marker
            return True
        else:
            return False
    
    # This method places a marker down on the spot chosen by the player
    def place_marker(self, player, coordinate):
        if self.grid[coordinate].value == None:
            self.grid[coordinate].value = player.marker
            return True
        else:
            return False
    

class Application():
    def __init__(self):
        root = tk.tk()