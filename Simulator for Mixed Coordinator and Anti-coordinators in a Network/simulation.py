import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from agent import Agent
import time
from csv import writer
import itertools


class Simulation:
    
    def __init__(self, population, average_degree, network_type,updating_activation_sequence,dim,Z_func):

        self.dim = dim
        self.network_type = network_type
        self.network = None
        self.Z_func = Z_func
        self.agents = self.__generate_agents(population, average_degree,self.Z_func)
        # self.cooperators = self.choose
        self.updating_activation_sequence = updating_activation_sequence
        self.population = population
        self.average_degree = average_degree





        # if(self.updating_activation_sequence == "synchronous"):
        #    self.active_agents =  self.__choose_cooperators_if_synchronous()
        # elif(self.updating_activation_sequence == "asynchronous"):
        #     self.active_agents = self.__choose_cooperators_if_asynchronous()
        # else:
        #     self.active_agents = self.__choose_cooperators_if_partial()

    def __generate_agents(self, population, average_degree,Z_func):
        if self.network_type == "lattice":
            self.network = self.__generate_lattice(population)
            # self.network =nx.grid_2d_graph(5,5)
        elif self.network_type == "ring":
            self.network = nx.circulant_graph(population, [1])

        elif self.network_type == "random_tree":
            self.network = nx.random_tree(population)

        elif self.network_type == "full_r_ary":
            r=2
            self.network = nx.full_rary_tree(r, population, create_using=None)

        elif self.network_type == "ER":
            self.network = nx.random_regular_graph(average_degree, population)
        
        elif self.network_type == "Complete":
            self.network = nx.complete_graph(population)
            
        elif self.network_type == "WS":
            self.network = nx.watts_strogatz_graph(population, average_degree, 0.5)
        
        elif self.network_type == "BA-SF":
            rearange_edges = int(average_degree*0.5)
            self.network = nx.barabasi_albert_graph(population, rearange_edges)

        agents = [Agent(self.network,id,self.Z_func) for i in range(population)]

        if self.network_type == "lattice":
            n = int(np.sqrt(population))
            for index, focal in enumerate(agents):
                neighbors_id = list(self.network[int(index//n), int(index%n)])
                for (x,y) in neighbors_id:
                    nb_id = int(x*n+y)
                    focal.neighbors_id.append(nb_id)

        # When using another topology
        else:
            for index, focal in enumerate(agents):
                neighbors_id = list(self.network[index])
                for nb_id in neighbors_id:
                    focal.neighbors_id.append(nb_id)

        return agents

    def __generate_lattice(self, population):
        """
        Default Lattice has only 4 adges(vertical&horizontal), so adding 4 edges in diagonal direction and
        Set periodic boundary condition
        """

        n = int(np.sqrt(population))    # n×n lattice is generated
        G = nx.grid_graph(dim = [n,n])

        # Add diagonal edge except for outer edge agent
        for i in range(1,n-1):
            for j in range(1,n-1):
                G.add_edge((i,j), (i+1,j+1))
                G.add_edge((i,j), (i+1,j-1))
                G.add_edge((i,j), (i-1,j+1))
                G.add_edge((i,j), (i-1,j-1))

        # Add edge along i = 0, j=1~n-2
        for j in range(1,n-1):
            G.add_edge((0,j), (n-1,j))
            G.add_edge((0,j), (n-1,j+1))
            G.add_edge((0,j), (n-1,j-1))
            G.add_edge((0,j), (1,j-1))
            G.add_edge((0,j), (1,j+1))

        # Add edge along j=0, i=1~n-2
        for i in range(1,n-1):
            G.add_edge((i,0), (i,n-1))
            G.add_edge((i,0), (i-1,n-1))
            G.add_edge((i,0), (i+1,n-1))
            G.add_edge((i,0), (i+1,1))

        # Add edge along j=0
        G.add_edge((0,0), (n-1,0))
        G.add_edge((0,0), (n-1,0+1))
        G.add_edge((0,0), (n-1,n-1))
        G.add_edge((0,0), (0,n-1))
        G.add_edge((0,0), (1,n-1))

        # Add edge along j=n-1
        G.add_edge((0,n-1), (n-1,n-1))
        G.add_edge((0,n-1), (n-1,0))
        G.add_edge((0,n-1), (n-1,n-2))
        G.add_edge((0,n-1), (0,0))

        # Add edge along i=n-1
        G.add_edge((n-1,0), (0,0))
        G.add_edge((n-1,0), (0,1))
        G.add_edge((n-1,0), (0,n-1))
        G.add_edge((n-1,0), (n-1,n-1))
        G.add_edge((n-1,0), (n-2,n-1))

        # Upper right edge agent
        G.add_edge((n-1,n-2),(n-2,n-1))

        return G

    # def __choose_cooperators_if_partial(self):
    #     population = len(self.agents)
    #     self.cooperators = rnd.sample(range(population), k = int(population/2))
    #
    # def __choose_cooperators_if_asynchronous(self):
    #     population = len(self.agents)
    #     self.cooperators = rnd.sample(range(population), k = 1)
    #
    # def __choose_cooperators_if_synchronous(self):
    #     population = len(self.agents)
    #     self.cooperators = [i for i in range(population)]

    def __initialize_label_A_or_B(self,a_list):

        population = len(self.agents)
        # random_index_of_A_players = rnd.sample(range(population), k=int(population *A_B_fraction))
        # print(type(random_index_of_A_players))
        for index , focal in enumerate(self.agents):

            if index in a_list:
                focal.strategy = "A"
            else:
                focal.strategy= "B"

    def determine_coordinator_or_anticoordinator(self,co_list):

        for index, focal in enumerate(self.agents):
            if index in co_list:
                focal.rule = "CO"
            else:
                focal.rule = "ANTI"

    def __take_snapshot(self, timestep,equilibrated):
        if self.network_type == "lattice":
            n = int(np.sqrt(len(self.agents)))
            for index, focal in enumerate(self.agents):
                if focal.strategy == "A":
                    self.network.nodes[int(index//n), int(index%n)]["strategy"] = "A"
                else:
                    self.network.nodes[int(index//n), int(index%n)]["strategy"] = "B"

            def color_for_lattice(i,j):
                if self.network.nodes[i,j]["strategy"] == "A":
                    return 'cyan'
                else:
                    return 'pink'

            color = dict(((i, j), color_for_lattice(i,j)) for i,j in self.network.nodes())
            pos = dict((n, n) for n in self.network.nodes())

        else:
            for index, focal in enumerate(self.agents):
                if focal.strategy == "A":
                    self.network.nodes[index]["strategy"] = "A"
                else:
                    self.network.nodes[index]["strategy"] = "B"

            def color(i):
                if self.network.nodes[i]["strategy"] == "A":
                    return 'cyan'
                else:
                    return 'pink'

            color =  dict((i, color(i)) for i in self.network.nodes())
            if self.network_type == "ring":
                pos = nx.circular_layout(self.network)

            else:
                pos = nx.spring_layout(self.network)

        nx.draw_networkx_edges(self.network, pos)
        nx.draw_networkx_nodes(self.network, pos, node_color = list(color.values()), node_size = 500)
        labels = {}
        for index, focal in enumerate(self.agents):
            if focal.rule == "CO":
                labels[index] = f"{index},CO"
            else:
                labels[index] = f"{index},ANTI"

        nx.draw_networkx_labels(self.network, pos, labels, font_size=16)
        eq_str = ""
        if equilibrated:
            eq_str = "Equilibrated!"
        plt.title(f"t={timestep}  {eq_str}", fontsize=20)
        plt.axis = "off"
        time_past_eq = -1

        plt.xticks([])
        plt.yticks([])
        plt.savefig(f"data/images/snap_t={timestep}.png", dpi = 300)
        plt.close()

    def has_equilibrated(self):
        equilibrated = 1
        A_count = 0
        B_count = 0
        # for agent in self.agents:
        #     if agent.strategy!= agent.next_strategy:
        #         equilibrated =0
        for index, focal in enumerate(self.agents):
            if focal.strategy!=focal.previous_strategy:
                equilibrated = 0
            # elif focal.next_strategy!=focal.strategy:
            #     equilibrated = 0
                break
        for agent in self.agents:
            if agent.strategy=="A":
                A_count=A_count+1
            elif agent.strategy=="B":
                B_count = B_count +1

        return equilibrated,A_count,B_count


    def one_episode(self, episode,time_steps,result,non_eq,threshold,co_list,a_list):
        self.__initialize_label_A_or_B(a_list)
        self.determine_coordinator_or_anticoordinator(co_list)


        equilibrated = -1

        equilibrated_array=[]
        last_a_list= []
        for t in range(time_steps):
            for index in range(self.population):
                self.agents[index].previous_strategy = self.agents[index].strategy
                if(t == time_steps-1):
                  last_a_list.append(self.agents[index].strategy)
            index = rnd.sample(range(self.population), k = 1)
            # if index!=0 and index!= self.population-1:

            # for index in self.cooperators:
            (self.agents[index[0]]).decide_next_strategy(self.agents,self.Z_func,threshold)
            # for index in self.cooperators:
            (self.agents[index[0]]).update_strategy()
            equilibrated, A_count, B_count = self.has_equilibrated()
            # self.__take_snapshot(t,equilibrated)
            equilibrated_array.append(equilibrated)


        eq_time = -1

        if(equilibrated == 1):
            eq_time =0
            for tt in range(time_steps-1,0,-1):
                if equilibrated_array[tt]==0:
                    eq_time = tt
                    break
        co_list_to_show = []
        a_list_to_show= []
        for i in range(self.population):
            if i in co_list:
                co_list_to_show.append("+")
            else:
                co_list_to_show.append("-")
        # for i in range(self.population):
        #     if i in a_list:
        #         a_list_to_show.append("A")
        #     else:
        #         a_list_to_show.append("B")

        new_result = pd.DataFrame(
            {'Eq': [equilibrated], 'co_list': [co_list_to_show], 'a_list': [last_a_list],
             'population': [self.population], 'equilibration time': [eq_time]})

        if equilibrated == 0:
            # this new_result is obviously new_result_non_eq but for simplicity was not renamed
            new_result = pd.DataFrame(
                {'Eq': [equilibrated],'co_list': [co_list_to_show],'a_list': [a_list_to_show],  'population': [self.population],  'equilibration time': [eq_time]})
        #     print(new_result)
        # print(new_result)
        return  new_result,equilibrated, eq_time

