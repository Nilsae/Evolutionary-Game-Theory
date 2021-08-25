import random as rnd
import numpy as np
import random
class Agent():


    def __init__(self,network,id,Z_func):
        # self.point = 0.0
        self.strategy = None # A or B
        self.next_strategy = None
        self.previous_strategy = None
        self.neighbors_id = []
        # self.A_neighbors_count = 0
        # self.B_neighbors_count = 0
        self.Z_func = Z_func
        self.id =id
        self.network = network
        self.rule = "CO"#=type = upfate rule(coordinating , anti_coordinating
    def __coordinating(self, agents,Z_func,threshold):
        A_neighbors_count = 0
        B_neighbors_count = 0




        total_neighbors_count = len(self.neighbors_id)
        neighbors = []
        # print(self.neighbors_id)
        for neighbor_id in self.neighbors_id:
        # for index,focal in enumerate(agents):
        # for neighbor_id, felan in self.network[self.id]:
            # neighbors.append(agents[neighbor_id])
            if agents[neighbor_id].strategy =="A":
                A_neighbors_count= A_neighbors_count+1
            else :
                B_neighbors_count = B_neighbors_count+1
        # best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        # best_neighbor = agents[best_neighbor_id]

        # if A_neighbors_count>threshold*total_neighbors_count:
        #     self.next_strategy = "A"
        # elif A_neighbors_count<threshold*total_neighbors_count:
        #     self.next_strategy = "B"
        # else:
        #     if Z_func == "A":
        #         self.next_strategy = "A"
        #     elif Z_func == "previous":
        #         self.next_strategy = self.strategy
        #     elif Z_func == "random"  :# random
        #         random_int = random.randint(0, 1)
        #         if random_int == 0:
        #             self.next_strategy = "A"
        #         else:
        #             self.next_strategy = "B"
        #     else:
        #         print("Invalid Z!")
        #     self.A_neighbors_count = 0
        if A_neighbors_count>=B_neighbors_count:
            self.next_strategy = "A"
        else:
            self.next_strategy = "B"
        # print(f"{self.strategy}  a neighbors:{A_neighbors_count}")
        # self.B_neighbors_count =0

    def __anti_coordinating(self, agents,Z_func,threshold):
        A_neighbors_count = 0
        B_neighbors_count = 0
        total_neighbors_count = len(self.neighbors_id)
        # print(self.network)
        # print(type(self.network[self.id]))
        # print(self.neighbors_id)
        for neighbor_id in self.neighbors_id:
        # for neighbor_id,felan in self.network[self.id]:
            if agents[neighbor_id].strategy =="A":
                A_neighbors_count= A_neighbors_count+1
            else :
                B_neighbors_count = B_neighbors_count+1
        # best_neighbor_id = self.neighbors_id[np.argmax(neighbors_point)]
        # best_neighbor = agents[best_neighbor_id]

        # if A_neighbors_count<threshold*total_neighbors_count:
        #     self.next_strategy = "A"
        # elif A_neighbors_count>threshold*total_neighbors_count:
        #     self.next_strategy = "B"
        # else:
        #     if Z_func=="A":
        #         self.next_strategy = "A"
        #     elif Z_func == "previous":
        #         self.next_strategy = self.strategy
        #     elif Z_func == "random": # random
        #         random_int =random.randint(0,1)
        #         if random_int == 0:
        #             self.next_strategy = "A"
        #         else:
        #             self.next_strategy = "B"
        #     else:
        #         print("Invalid Z!")
        #     self.A_neighbors_count = 0
        # print("anei = ",A_neighbors_count,"bnei = ",B_neighbors_count)
        if A_neighbors_count<=B_neighbors_count:
            self.next_strategy = "A"
        else:
            self.next_strategy = "B"
        # print(f"{self.strategy}  a neighbors:{A_neighbors_count}")
        # self.B_neighbors_count = 0


    def decide_next_strategy(self, agent,Z_func,threshold):
        # print("rule = ",self.rule,"\n")
        if self.rule == "CO":
            self.__coordinating(agent,Z_func,threshold)

        elif self.rule == "ANTI":
            self.__anti_coordinating(agent,Z_func,threshold)

    def update_strategy(self):
        self.strategy = self.next_strategy