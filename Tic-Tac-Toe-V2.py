from ast import Lambda
import tkinter as tk
import os, sys
from copy import deepcopy

# Backend logic and objects necessary for game to run
class Player():
    def __init__(self, name, avatar, marker):
        self.name = name
        self.avatar = avatar
        self.marker = marker
        self.win = False
        self.CPU = False

# Nodes used specifically by linkedlists
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

# Nodes to be used by graphs
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
    
    def clear_grid(self):
        for node in self.grid.values():
            node.value = None
            node.image = None
    
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


# Begins classes built as the separate windows used for the application
# Builds frame for avatar/setup window
class AvatarWindow(tk.Frame):
    def __init__(self, master, player1, player2, main):

        # Will inherit root window when instantiated 
        tk.Frame.__init__(self, master)

        # Stores reference to root application 
        self.main = main

        # Instantiates radiobutton variable and defines default state as single player mode
        self.v = tk.IntVar(value=1)

        # Stores references to each player object
        self.player1 = player1
        self.player2 = player2

        # Obtains working directory for program 
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

        # Adds in all images for player avatars
        # All images must be saved in same folder as application to work
        # Turtle avatar can be found at <a target="_blank" href="https://icons8.com/icon/49018/turtle">Turtle</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        turtle_photo = tk.PhotoImage(file=dirname + '\gturtle.png')

        # Monkey avatar can be found at <a target="_blank" href="https://icons8.com/icon/62481/chimpanzee">Chimpanzee</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        monkey_photo = tk.PhotoImage(file=dirname + '\monkey.png')

        # Frog avatar can be found at <a target="_blank" href="https://icons8.com/icon/Npta5BprV_io/frog-face">Frog Face</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        frog_photo = tk.PhotoImage(file=dirname + '\gfrog.png')

        # Koala avatar can be found at <a target="_blank" href="https://icons8.com/icon/bxiThUWYVUpC/koala">Koala</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        koala_photo = tk.PhotoImage(file=dirname + '\koala.png')

        # Walrus avatar can be found at <a target="_blank" href="https://icons8.com/icon/2oOXGVA1B6St/walrus">Walrus</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        walrus_photo = tk.PhotoImage(file=dirname + '\walrus.png')

        # Panda avatar can be found at <a target="_blank" href="https://icons8.com/icon/01OJtDgOj8sL/panda">Panda</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        panda_photo = tk.PhotoImage(file=dirname + '\panda.png')

        # Question mark avatar can be found at <a target="_blank" href="https://icons8.com/icon/103873/question-mark">Question Mark</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
        CPU_avatar = tk.PhotoImage(file=dirname + '\question.png')

        # Stores each avatar in object for later reference by methods
        self.turtle = turtle_photo
        self.monkey = monkey_photo
        self.frog = frog_photo
        self.koala = koala_photo
        self.walrus = walrus_photo
        self.panda = panda_photo
        self.cpu_avatar = CPU_avatar

        # Creates and assigns objects to frame grid
        # Creates spacers needed for GUI
        row_1_spacer = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        left_row_2_spacer = tk.Canvas(self, background="#8F8F8F", width=100, height=5, highlightthickness=0)
        right_row_2_spacer = tk.Canvas(self, background="#8F8F8F", width=100, height=5, highlightthickness=0)

        row_3_spacer = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        row_4_spacer1 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)
        row_4_spacer2 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)
        row_4_spacer3 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        row_5_spacer = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        row_6_spacer1 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)
        row_6_spacer2 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)
        row_6_spacer3 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)
        row_6_spacer4 = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        row_7_spacer = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        row_8_spacer1 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)
        row_8_spacer2 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_8_spacer3 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_8_spacer4 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)
        row_8_spacer5 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)
        row_8_spacer6 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_8_spacer7 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_8_spacer8 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)

        row_9_spacer = tk.Canvas(self, background="#8F8F8F", width=1, height=5, highlightthickness=0)

        row_10_spacer1 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)
        row_10_spacer2 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_10_spacer3 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_10_spacer4 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)
        row_10_spacer5 = tk.Canvas(self, background="#8F8F8F", width=30, height=20, highlightthickness=0)
        row_10_spacer6 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)
        row_10_spacer7 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_10_spacer8 = tk.Canvas(self, background="#8F8F8F", width=5, height=20, highlightthickness=0)
        row_10_spacer9 = tk.Canvas(self, background="#8F8F8F", width=20, height=20, highlightthickness=0)

        row_11_spacer = tk.Canvas(self, background="#8F8F8F", width=1, height=20, highlightthickness=0)

        left_row_12_spacer = tk.Canvas(self, background="#8F8F8F", width=100, height=5, highlightthickness=0)
        right_row_12_spacer = tk.Canvas(self, background="#8F8F8F", width=100, height=5, highlightthickness=0)

        # Creates labels used within GUI
        setup_label = tk.Label(self, background="#FFFFFF", width=10, height=2, highlightthickness=0, text="SETUP", font=('Segoe 16 bold'))
        self.player1_avatar_label = tk.Label(self, background="#FFFFFF", width=10, highlightthickness=0, image=CPU_avatar)
        self.player2_avatar_label = tk.Label(self, background="#FFFFFF", width=10, highlightthickness=0, image=CPU_avatar)
        player_count_label = tk.Label(self, background="#FFFFFF", width=10, height=2, highlightthickness=0, text="PLAYERS", bg="#8F8F8F", font=('Segoe 14 bold'))
        self.error_label = tk.Label(self, background="#8F8F8F", width=10, height=2, highlightthickness=0, text="", font=('Segoe 16 bold'), fg='red')

        # Creates entry boxes for player names
        self.player1_entry = tk.Entry(self, background="#FFFFFF", width=10, highlightthickness=0, font=('Segoe 20 bold'), justify=tk.CENTER)
        self.player2_entry = tk.Entry(self, background="#FFFFFF", width=10, highlightthickness=0, font=('Segoe 20 bold'), justify=tk.CENTER)

        # Create radio buttons to toggle single or multiplayer modes
        self.single_p_rbutton = tk.Radiobutton(self, text="1", variable=self.v, value=1, activebackground="#8F8F8F", bg="#8F8F8F", font=('Segoe 14 bold'))
        self.single_p_rbutton.bind('<ButtonRelease-1>', self.change_single_player)

        self.multi_p_rbutton = tk.Radiobutton(self, text="2", variable=self.v, value=2, activebackground="#8F8F8F", bg="#8F8F8F", font=('Segoe 14 bold'))
        self.multi_p_rbutton.bind('<ButtonRelease-1>', self.change_multi_player)

        # Creates buttons for selecting an avatar as well as the start game button
        # Buttons containing images 
        start_game_btn = tk.Button(self, background="#FFFFFF", width=15, height=2, highlightthickness=0, text="START GAME", font=('Segoe 14 bold'), command=lambda: self.complete_setup())
        
        self.player1_avi_btn1 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=turtle_photo, command=lambda: self.select_avatar(turtle_photo, self.player1, self.player1_avatar_label, self.player2_avatar_label))
        self.player1_avi_btn1.image = turtle_photo

        self.player1_avi_btn2 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=monkey_photo, command=lambda: self.select_avatar(monkey_photo, self.player1, self.player1_avatar_label, self.player2_avatar_label))
        self.player1_avi_btn2.image = monkey_photo

        self.player1_avi_btn3 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=frog_photo, command=lambda: self.select_avatar(frog_photo, self.player1, self.player1_avatar_label, self.player2_avatar_label))
        self.player1_avi_btn3.image = frog_photo

        self.player1_avi_btn4 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=koala_photo, command=lambda: self.select_avatar(koala_photo, self.player1, self.player1_avatar_label, self.player2_avatar_label))
        self.player1_avi_btn4.image = koala_photo

        self.player1_avi_btn5 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=walrus_photo, command=lambda: self.select_avatar(walrus_photo, self.player1, self.player1_avatar_label, self.player2_avatar_label))
        self.player1_avi_btn5.image = walrus_photo

        self.player1_avi_btn6 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=panda_photo, command=lambda: self.select_avatar(panda_photo, self.player1, self.player1_avatar_label, self.player2_avatar_label))
        self.player1_avi_btn6.image = panda_photo

        self.player2_avi_btn1 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=turtle_photo, command=lambda: self.select_avatar(turtle_photo, self.player2, self.player2_avatar_label, self.player1_avatar_label))
        self.player2_avi_btn1.image = turtle_photo

        self.player2_avi_btn2 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=monkey_photo, command=lambda: self.select_avatar(monkey_photo, self.player2, self.player2_avatar_label, self.player1_avatar_label))
        self.player2_avi_btn2.image = monkey_photo

        self.player2_avi_btn3 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=frog_photo, command=lambda: self.select_avatar(frog_photo, self.player2, self.player2_avatar_label, self.player1_avatar_label))
        self.player2_avi_btn3.image = frog_photo

        self.player2_avi_btn4 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=koala_photo, command=lambda: self.select_avatar(koala_photo, self.player2, self.player2_avatar_label, self.player1_avatar_label))
        self.player2_avi_btn4.image = koala_photo

        self.player2_avi_btn5 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=walrus_photo, command=lambda: self.select_avatar(walrus_photo, self.player2, self.player2_avatar_label, self.player1_avatar_label))
        self.player2_avi_btn5.image = walrus_photo

        self.player2_avi_btn6 = tk.Button(self, background="#FFFFFF", highlightthickness=0, image=panda_photo, command=lambda: self.select_avatar(panda_photo, self.player2, self.player2_avatar_label, self.player1_avatar_label))
        self.player2_avi_btn6.image = panda_photo
        

        # Builds out window
        row_1_spacer.grid(row=1, column=1, sticky="nsew", columnspan=19)
        
        left_row_2_spacer.grid(row=2, column=1, columnspan=5, sticky="nsew")
        setup_label.grid(row=2, column=6, columnspan=9, sticky="nsew")
        right_row_2_spacer.grid(row=2, column=15, columnspan=5, sticky="nsew")

        row_3_spacer.grid(row=3, column=1, sticky="nsew", columnspan=19)

        row_4_spacer1.grid(row=4, column=1, sticky="nsew")
        self.player1_entry.grid(row=4, column=2, columnspan=5, sticky="nsew")
        row_4_spacer2.grid(row=4, column=7, columnspan=7, sticky="nsew")
        self.player2_entry.grid(row=4, column=14, columnspan=5, sticky="nsew")
        row_4_spacer3.grid(row=4, column=19, sticky="nsew")
    
        row_5_spacer.grid(row=5, column=1, sticky="nsew", columnspan=19)

        row_6_spacer1.grid(row=6, column=1, columnspan=3, sticky="nsew")
        self.player1_avatar_label.grid(row=6, column=4, sticky="nsew")
        row_6_spacer2.grid(row=6, column=5, columnspan=3, sticky="nsew")
        start_game_btn.grid(row=6, column=8, columnspan=5, sticky="nsew")
        row_6_spacer3.grid(row=6, column=13, columnspan=3, sticky="nsew")
        self.player2_avatar_label.grid(row=6, column=16, sticky="nsew")
        row_6_spacer4.grid(row=6, column=17, columnspan=3, sticky="nsew")

        row_7_spacer.grid(row=7, column=1, columnspan=19, sticky="nsew")

        row_8_spacer1.grid(row=8, column=1, sticky="nsew")
        self.player1_avi_btn1.grid(row=8, column=2, sticky="nsew")
        row_8_spacer2.grid(row=8, column=3, sticky="nsew")
        self.player1_avi_btn2.grid(row=8, column=4, sticky="nsew")
        row_8_spacer3.grid(row=8, column=5, sticky="nsew")
        self.player1_avi_btn3.grid(row=8, column=6, sticky="nsew")
        row_8_spacer4.grid(row=8, column=7, sticky="nsew")
        player_count_label.grid(row=8, column=8, columnspan=5, sticky="nsew")
        row_8_spacer5.grid(row=8, column=13, sticky="nsew")
        self.player2_avi_btn1.grid(row=8, column=14, sticky="nsew")
        row_8_spacer6.grid(row=8, column=15, sticky="nsew")
        self.player2_avi_btn2.grid(row=8, column=16, sticky="nsew")
        row_8_spacer7.grid(row=8, column=17, sticky="nsew")
        self.player2_avi_btn3.grid(row=8, column=18, sticky="nsew")
        row_8_spacer8.grid(row=8, column=19, sticky="nsew")

        row_9_spacer.grid(row=9, column=1, columnspan=19, sticky="nsew")
        
        row_10_spacer1.grid(row=10, column=1, sticky="nsew")
        self.player1_avi_btn4.grid(row=10, column=2, sticky="nsew")
        row_10_spacer2.grid(row=10, column=3, sticky="nsew")
        self.player1_avi_btn5.grid(row=10, column=4, sticky="nsew")
        row_10_spacer3.grid(row=10, column=5, sticky="nsew")
        self.player1_avi_btn6.grid(row=10, column=6, sticky="nsew")
        row_10_spacer4.grid(row=10, column=7, sticky="nsew")

        # Buttons to select single or multiplayer mode as well as space between radiobuttons
        self.single_p_rbutton.grid(row=10, column=8, columnspan=2, sticky="nsew")
        row_10_spacer5.grid(row=10, column=10, sticky="nsew")
        self.multi_p_rbutton.grid(row=10, column=11, columnspan=2, sticky="nsew")

        
        row_10_spacer6.grid(row=10, column=13, sticky="nsew")
        self.player2_avi_btn4.grid(row=10, column=14, sticky="nsew")
        row_10_spacer7.grid(row=10, column=15, sticky="nsew")
        self.player2_avi_btn5.grid(row=10, column=16, sticky="nsew")
        row_10_spacer8.grid(row=10, column=17, sticky="nsew")
        self.player2_avi_btn6.grid(row=10, column=18, sticky="nsew")
        row_10_spacer9.grid(row=10, column=19, sticky="nsew")

        row_11_spacer.grid(row=11, column=1, columnspan=19, sticky="nsew")

        left_row_12_spacer.grid(row=12, column=1, columnspan=4, sticky="nsew")
        self.error_label.grid(row=12, column=5, columnspan=10, sticky="nsew")
        right_row_12_spacer.grid(row=12, column=15, columnspan=5, sticky="nsew")

        # Adds weights to frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Sets default settings when loading into screen
        self.change_single_player(None)

    # Helper functions for setup window
    # Sets parameters so that single player mode is enabled
    def change_single_player(self, n):
        self.player2_entry.delete(0, tk.END)
        self.player2_entry.insert(0, "CPU")
        self.player2_entry["state"] = tk.DISABLED
        self.player2.name = "CPU"
        self.player2.CPU = True
        self.player2.avatar = self.cpu_avatar
        self.player2_avatar_label["image"] = self.cpu_avatar
        self.player2_avi_btn1["state"] = tk.DISABLED
        self.player2_avi_btn2["state"] = tk.DISABLED
        self.player2_avi_btn3["state"] = tk.DISABLED
        self.player2_avi_btn4["state"] = tk.DISABLED
        self.player2_avi_btn5["state"] = tk.DISABLED
        self.player2_avi_btn6["state"] = tk.DISABLED
        for button in self.winfo_children():
            if 'tkinter.Button' in str(type(button)):
                if len(str(button)[22:24].strip()) > 0:
                    current_button = int(str(button)[22:24].strip())
                else:
                    current_button = 1
                if button["image"] == self.player1_avatar_label['image']:
                    button["state"] = tk.DISABLED
                elif current_button < 8:
                    button["state"] = tk.ACTIVE
    
    # Sets parameters so that multiplayer mode is enabled
    def change_multi_player(self, n):
        self.player2_entry["state"] = tk.NORMAL
        self.player2_entry.delete(0, tk.END)
        self.player2.name = ""
        self.player2.CPU = False
        self.player2.avatar = None
        self.player2_avatar_label["image"] = None
        for button in self.winfo_children():
            if 'tkinter.Button' in str(type(button)):
                if button["image"] == self.player1_avatar_label['image']:
                    button["state"] = tk.DISABLED
                else:
                    button["state"] = tk.ACTIVE
    
    # Allows users to select their own unique avatar to use during the game
    def select_avatar(self, image, player1, label1, label2):
        player1.avatar = image
        label1["image"] = image
        for button in self.winfo_children():
            if 'tkinter.Button' in str(type(button)):
                if len(str(button)[22:24].strip()) > 0:
                    current_button = int(str(button)[22:24].strip())
                else:
                    current_button = 1
                if button["image"] == label1['image'] or button['image'] == label2['image']:
                    button["state"] = tk.DISABLED
                elif self.player2.CPU == True and current_button < 8:
                    button["state"] = tk.ACTIVE
                elif self.player2.CPU == False:
                    button["state"] = tk.ACTIVE
    
    # Completes game setup, provides error handling for players attempting to start the game without a name and then progresses to the next screen
    def complete_setup(self):
        player1_name = self.player1_entry.get()
        if self.player2.CPU == False:
            player2_name = self.player2_entry.get()
        else:
            player2_name = "CPU"
        if len(player1_name) < 1 or len(player2_name) < 1:
            self.error_label['text'] = "Please enter your name"
        else:
            self.player1.name = player1_name
            self.player2.name = player2_name
            self.main.game_frame.tkraise()
            
        




class GameWindow(tk.Frame):
    def __init__(self, master, main):
        tk.Frame.__init__(self, master)



class Application():
    def __init__(self):
        # Instantiates application
        self.root = tk.Tk()

        # Creates players 1 and 2 objects 
        self.player1 = Player(name="", avatar=None, marker="X")
        self.player2 = Player(name="CPU", avatar=None, marker="O")

        # Adds title to window
        self.root.title("Tic-Tac-Toe")

        # Builds game main window and enters in player specific information
        self.game_frame = GameWindow(self.root, self)
        self.game_frame.grid(row=1, column=1, sticky="nsew")

        # Builds setup window and passes in player objects to be edited within setup 
        self.avatar_frame = AvatarWindow(self.root, self.player1, self.player2, self)
        self.avatar_frame.grid(row=1, column=1, sticky="nsew")

        # Maintains application loop until retrieving input to close application
        self.root.mainloop()


new_game = Application()


# new_grid = Grid()
# new_grid.build_grid()
# player1 = Player(name="TestName", avatar=None, marker="X", image=None)
# player2 = Player(name="TestCPU", avatar=None, marker="O", image=None)


# new_grid.place_marker(player1, (2,2))
# new_grid.place_marker(player2, (1,1))
# new_grid.place_marker(player1, (2,1))
# new_grid.place_marker(player2, (1,2))
# new_grid.place_marker(player1, (1,3))
# all_moves = new_grid.min_max(grid=new_grid.grid, player=player1, cpu=player2)
# move_found = new_grid.find_best_move(player1, player2)
# print(all_moves)
