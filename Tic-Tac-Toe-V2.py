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
    
    # Iterates through a select group of nodes, performing a depth first search utilizing each node as a starting point
    def node_search(self, player1, player2, grid=None):
        x = None
        nodes_to_check = [x for key in grid.keys if key[0] == 1 or key[1] == 1]
        for node in nodes_to_check:
            r, c = node[0], node[1]
            winning_player = None
            exit_loop = False
            iter = 1
            while winning_player == None and exit_loop == False:
                if iter == 1:
                    winning_player = self.dfs(r, c, r, c+1, player1, player2, grid, [grid[node].value])
                elif iter == 2:
                    winning_player = self.dfs(r, c, r+1, c+1, player1, player2, grid, [grid[node].value])
                elif iter == 3:
                    winning_player = self.dfs(r, c, r+1, c, player1, player2, grid, [grid[node].value])
                elif iter == 4:
                    winning_player = self.dfs(r, c, r+1, c-1, player1, player2, grid, [grid[node].value])
                else:
                    exit_loop = True

    # Min max algorithm used by CPU player to simulate possible moves that can be played and return a dictionary full of possibles paths to take, sorted by key
    def min_max(self, grid, player, cpu, path=[], depth=0):
        new_grid = grid
        moves = {}
        for idx, node in enumerate(path):
            if idx != 1:
                grid[node].value = cpu.marker
            else:
                grid[node].value = player.marker
        if self.count_placed_nodes(grid) > 4 and depth > 0:
            win = self.node_search(grid, player, cpu)
            if win == player:
                moves["player"] = LinkedList()
                moves["player"].add_tail_node(path)
                return moves
            elif win == cpu:
                moves[depth] = LinkedList()
                moves[depth].add_tail_nodes(path)
                return moves
            elif win == None and depth == 3:
                moves[4] = LinkedList()
                moves[4].add_tail_node(path)
        elif self.count_placed_nodes(grid) < 5 and depth == 3:
            moves[4] = LinkedList()
            moves[4].add_tail_node(path)
            return moves
        for node in grid.keys:
            if grid[node].value == None:
                path.append(node)
                moves_found = self.min_max(grid, player, cpu, path, depth+1)
                for key in moves_found.keys:
                    if key in list(moves.keys):
                        moves[key].merge_lists(moves_found[key])
                    else:
                        moves[key] = moves_found[key]
        return moves
    
    # This method takes the created moves dictionary and uses it to find the optimal next move for the CPU
    def find_best_move(self, player, cpu):
        moves = self.min_max(self.grid, player, cpu)




class Application():
    def __init__(self):
        root = tk.tk()


new_grid = Grid()
new_grid.build_grid()
player1 = Player(name="TestName", avatar=None, marker="X", image=None)
player2 = Player(name="TestCPU", avatar=None, marker="O", image=None)
