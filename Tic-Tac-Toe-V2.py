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
    
    # This method is to run a check to see if an inserted path has a win
    def check_win(self, nodes_found, player1, player2):
        if nodes_found.count(player1.marker) == 3:
            return player1
        elif nodes_found.count(player2.marker) == 3:
            return player2
        else: 
            return None
    
    # This method performs a depth first search to gather nodes and place them in a list to check for a winning path
    def dfs(self, r, c, r2, c2, player1, player2, grid, nodes_found):
        if (r2, c2) not in grid.keys and len(nodes_found) < 3:
            return None
        elif len(nodes_found) == 3:
            return self.check_win(nodes_found, player1, player2)
        else:
            nodes_found.append(grid[(r2, c2)].value)
            r , r2 = r2, r2 + (r2 - r)
            c, c2 = c2, c2 + (c2 - c)
        return self.dfs(r, c, r2, c2, player1, player2, grid, nodes_found)
    
    # Simple method to count how many nodes have had a player marker placed on them
    def count_placed_nodes(self, grid):
        count = 0
        for node in grid.values:
            if node.value != None:
                count += 1
        return count

class Application():
    def __init__(self):
        root = tk.tk()