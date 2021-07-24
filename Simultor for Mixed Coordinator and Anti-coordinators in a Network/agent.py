import random as rnd
import numpy as np
import random

class Agent():


    def __init__(self):
        # self.point = 0.0
        self.strategy = None # A or B
        self.next_strategy = None
        self.previous_strategy = None
        self.neighbors_id = []
        self.A_neighbors_count = 0
        self.B_neighbors_count = 0
        self.rule = "CO"#=type = upfate rule(coordinating , anti_coordinating
    def __coordinating(self, agents):

        #         for nb_id in focal.neighbors_id:
        #             neighbor = self.agents[nb_id]
        #             if focal.strategy == "C" and neighbor.strategy == "C":
        #                 focal.point += R
        #             elif focal.strategy == "C" and neighbor.strategy == "D":
        #                 focal.point += S
        #             elif focal.strategy == "D" and neighbor.strategy == "C":
        #                 focal.point += T
        #             elif focal.strategy == "D" and neighbor.strategy == "D":
        #                 focal.point += P




        total_neighbors_count = len(self.neighbors_id)
        neighbors = []
        for neighbor_id in self.neighbors_id:
            # neighbors.append(agents[neighbor_id])
            if agents[neighbor_id].strategy =="A":
                self.A_neighbors_count= self.A_neighbors_count+1
            else :
                self.B_neighbors_count = self.B_neighbors_count+1
        # best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        # best_neighbor = agents[best_neighbor_id]

        if self.A_neighbors_count>1/2*total_neighbors_count:
            self.next_strategy = "A"
        elif self.A_neighbors_count<1/2*total_neighbors_count:
            self.next_strategy = "B"
        else:
            self.next_strategy = self.strategy

    def __anti_coordinating(self, agents):

        total_neighbors_count = len(self.neighbors_id)
        for neighbor_id in self.neighbors_id:
            if agents[neighbor_id].strategy =="A":
                self.A_neighbors_count= self.A_neighbors_count+1
            else :
                B_neighbors_count = self.B_neighbors_count+1
        # best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        # best_neighbor = agents[best_neighbor_id]

        if self.A_neighbors_count<1/2*total_neighbors_count:
            self.next_strategy = "A"
        elif self.A_neighbors_count>1/2*total_neighbors_count:
            self.next_strategy = "B"
        else:
            random_int =random.randint(0,1)
            if random_int == 0:
                self.next_strategy = "A"
            else:
                self.next_strategy = "B"

    def decide_next_strategy(self, agent):

        if self.rule == "CO":
            self.__coordinating(agent)

        elif self.rule == "ANTI":
            self.__anti_coordinating(agent)

    def update_strategy(self):
        self.strategy = self.next_strategy