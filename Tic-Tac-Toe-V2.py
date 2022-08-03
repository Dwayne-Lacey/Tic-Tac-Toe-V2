import tkinter as tk
import random

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