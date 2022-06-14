import random as rnd
import numpy as np
import random


class Agent():
    def __init__(self, network, Z_func, id):
        self.strategy = None  # A or B
        self.next_strategy = None
        self.previous_strategy = None
        self.neighbors_id = []
        self.Z_func = Z_func
        self.network = network
        self.type = None  # =type = update rule(coordinating , anti_coordinating
        self.id = id

    def __coordinating(self, agents, Z_func, threshold):
        A_neighbors_count = 0
        B_neighbors_count = 0
        total_neighbors_count = len(self.neighbors_id)
        neighbors = []
        for neighbor_id in self.neighbors_id:
            if agents[neighbor_id].strategy == "A":
                A_neighbors_count = A_neighbors_count + 1
            else:
                B_neighbors_count = B_neighbors_count + 1
        # if self.binary_threshold =="normal":
        #         print("co: "+str(A_neighbors_count)+" As and "+str(B_neighbors_count)+" Bs")
        if A_neighbors_count >= B_neighbors_count:
            self.next_strategy = "A"
        else:
            self.next_strategy = "B"

    def __anti_coordinating(self, agents, Z_func, threshold):
        A_neighbors_count = 0
        B_neighbors_count = 0
        total_neighbors_count = len(self.neighbors_id)
        for neighbor_id in self.neighbors_id:
            if agents[neighbor_id].strategy == "A":
                A_neighbors_count = A_neighbors_count + 1
            else:
                B_neighbors_count = B_neighbors_count + 1
        # if self.binary_threshold == "normal":
        #         print("anti: "+str(A_neighbors_count)+" As and "+str(B_neighbors_count)+" Bs")
        if A_neighbors_count <= B_neighbors_count:
            self.next_strategy = "A"
        else:
            self.next_strategy = "B"

    def decide_next_strategy(self, agent, Z_func, threshold):
        if self.type == "+":
            self.__coordinating(agent, Z_func, threshold)

        elif self.type == "-":
            self.__anti_coordinating(agent, Z_func, threshold)

    def update_strategy(self):
        self.strategy = self.next_strategy

