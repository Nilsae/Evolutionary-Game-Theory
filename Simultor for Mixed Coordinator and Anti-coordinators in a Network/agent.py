import random as rnd
import numpy as np

class Agent:


    def __init__(self):
        # self.point = 0.0
        self.strategy = None
        self.next_strategy = None
        self.neighbors_id = []
        self.A_neighbors_count = 0
        self.B_neighbors_count = 0
        self.rule = "CO"#=type = upfate rule(coordinating , anti_coordinating
    def __coordinating(self, agents):

        total_neighbors_count = len(self.neighbors_id)
        for neighbor_id in self.neighbors_id:
            if agents[neighbor_id].strategy ==1:
                self.A_neighbors_count= self.A_neighbors_count+1
            else :
                self.B_neighbors_count = self.B_neighbors_count+1
        # best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        # best_neighbor = agents[best_neighbor_id]

        if self.A_neighbors_count>1/2*total_neighbors_count:
            self.next_strategy = 1
        elif self.A_neighbors_count<1/2*total_neighbors_count:
            self.next_strategy = 0
        else:
            self.next_strategy = self.strategy

    def __anti_coordinating(self, agents):

        total_neighbors_count = len(self.neighbors_id)
        for neighbor_id in self.neighbors_id:
            if agents[neighbor_id].strategy ==1:
                self.A_neighbors_count= self.A_neighbors_count+1
            else :
                B_neighbors_count = self.B_neighbors_count+1
        # best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        # best_neighbor = agents[best_neighbor_id]

        if self.A_neighbors_count<1/2*total_neighbors_count:
            self.next_strategy = 1
        elif self.A_neighbors_count>1/2*total_neighbors_count:
            self.next_strategy = 0
        else:
            self.next_strategy = self.strategy

    def decide_next_strategy(self, agents):

        if self.rule == "CO":
            self.__coordinating(agents)

        elif self.rule == "ANTI":
            self.__anti_coordinating(agents)

    def update_strategy(self):
        self.strategy = self.next_strategy