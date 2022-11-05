from shutil import move
import tkinter as tk
import random
from copy import deepcopy

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
        if (r2, c2) not in grid.keys() and len(nodes_found) < 3:
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
        for node in grid.values():
            if node.value != None:
                count += 1
        return count
    
    # Iterates through a select group of nodes, performing a depth first search utilizing each node as a starting point
    def node_search(self, player1, player2, grid=None):
        x = None
        nodes_to_check = [key for key in grid.keys() if key[0] == 1 or key[1] == 1]
        winning_player = None
        for node in nodes_to_check:
            r, c = node[0], node[1]
            exit_loop = False
            iter = 1
            while winning_player == None and exit_loop == False:
                if iter == 1:
                    winning_player = self.dfs(r, c, r, c+1, player1, player2, grid, [grid[node].value])
                    iter += 1
                elif iter == 2:
                    winning_player = self.dfs(r, c, r+1, c+1, player1, player2, grid, [grid[node].value])
                    iter += 1
                elif iter == 3:
                    winning_player = self.dfs(r, c, r+1, c, player1, player2, grid, [grid[node].value])
                    iter += 1
                elif iter == 4:
                    winning_player = self.dfs(r, c, r+1, c-1, player1, player2, grid, [grid[node].value])
                    iter += 1
                else:
                    exit_loop = True
            if winning_player != None:
                return winning_player
        return winning_player

    # Min max algorithm used by CPU player to simulate possible moves that can be played and return a dictionary full of possibles paths to take, sorted by key
    def min_max(self, grid, player, cpu, path=[], depth=0):
        new_grid = deepcopy(grid)
        moves = {}

        # Enters in only the simulated CPU markers into the simulated grid based on simulated coordinates from path
        # This is done on idx = 0 and idx = 2. When idx = 1 it is the player's simulated turn
        for idx, node in enumerate(path):
            if idx != 1:
                new_grid[node].value = cpu.marker
            else:
                new_grid[node].value = player.marker
        
        # Checks how many moves have been made on the simulated grid total to decide if a win check should be done. Requires a minimum of 5 moves made before a win could be possibly made
        nodes_placed = self.count_placed_nodes(new_grid)
        if nodes_placed > 4 and depth > 0:
            win = self.node_search(player, cpu, new_grid)
            if win == player:
                moves["player"] = LinkedList()
                moves["player"].add_tail_node(path)
                return moves
            elif win == cpu:
                moves[depth] = LinkedList()
                moves[depth].add_tail_node(path)
                return moves
            elif win == None and depth == 3:
                moves[4] = LinkedList()
                moves[4].add_tail_node(path)
        
        # If there's been a recursion depth of 3 but fewer than 5 nodes have been placed down, there's no possibility of winning path being found
        # Stores all potential paths that haven't had at least 5 nodes placed in dictionary key 4
        elif nodes_placed < 5 and depth == 3:
            moves[4] = LinkedList()
            moves[4].add_tail_node(path)
            return moves

        for node in new_grid.keys():
            current_path = path.copy()
            if new_grid[node].value == None:
                current_path.append(node)
                if depth < 3:
                    moves_found = self.min_max(new_grid, player, cpu, current_path, depth+1)
                    for key in moves_found.keys():
                        if key in list(moves.keys()):
                            moves[key].merge_lists(moves_found[key])
                        else:
                            moves[key] = moves_found[key]
        return moves
    
    # This method takes the created moves dictionary and uses it to find the optimal next move for the CPU
    # 1 - CPU wins next move, player - Player wins in their next move, 3 - CPU wins in their second move, 4 - Nobody wins in next three simulated moves
    def find_best_move(self, player, cpu):
        available_moves = self.min_max(self.grid, player, cpu)
        if 1 in available_moves.keys():
            move_to_return = available_moves[1].pop_node()
        elif "player" in available_moves.keys():
            move_to_return = available_moves["player"].pop_node()
            return move_to_return[1]
        else:
            minimum_key = min(list(available_moves.keys()))
            move_to_return = available_moves[minimum_key].pop_node()
        return move_to_return[0]


class Application():
    def __init__(self):
        root = tk.tk()


new_grid = Grid()
new_grid.build_grid()
player1 = Player(name="TestName", avatar=None, marker="X", image=None)
player2 = Player(name="TestCPU", avatar=None, marker="O", image=None)


new_grid.place_marker(player1, (2,2))
new_grid.place_marker(player2, (1,1))
new_grid.place_marker(player1, (2,1))
new_grid.place_marker(player2, (1,2))
new_grid.place_marker(player1, (1,3))
all_moves = new_grid.min_max(grid=new_grid.grid, player=player1, cpu=player2)
move_found = new_grid.find_best_move(player1, player2)
print(all_moves)
