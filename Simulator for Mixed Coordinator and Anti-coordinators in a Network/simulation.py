import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from agent import Agent
import time
from csv import writer
import itertools

#
# def append_list_as_row(file_name, list_of_elem):
#     # Open file in append mode
#     with open(file_name, 'a+', newline='') as write_obj:
#         # Create a writer object from csv module
#         csv_writer = writer(write_obj)
#         # Add contents of list as last row in the csv file
#         csv_writer.writerow(list_of_elem)

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





        if(self.updating_activation_sequence == "synchronous"):
           self.active_agents =  self.__choose_cooperators_if_synchronous()
        elif(self.updating_activation_sequence == "asynchronous"):
            self.active_agents = self.__choose_cooperators_if_asynchronous()
        else:
            self.active_agents = self.__choose_cooperators_if_partial()

    def __generate_agents(self, population, average_degree,Z_func):
        if self.network_type == "lattice":
            self.network = self.__generate_lattice(population)
            # self.network =nx.grid_2d_graph(5,5)
        elif self.network_type == "ring":
            self.network = nx.circulant_graph(population, [1])
            
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
        # agents = []
        # for id in range(population):
        #     agents.append(Agent(self.network,id))
        #
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

    def __choose_cooperators_if_partial(self):
        population = len(self.agents)
        self.cooperators = rnd.sample(range(population), k = int(population/2))

    def __choose_cooperators_if_asynchronous(self):
        population = len(self.agents)
        self.cooperators = rnd.sample(range(population), k = 1)

    def __choose_cooperators_if_synchronous(self):
        population = len(self.agents)
        self.cooperators = [i for i in range(population)]

    def __initialize_label_A_or_B(self,A_B_fraction):

        population = len(self.agents)
        random_index_of_A_players = rnd.sample(range(population), k=int(population *A_B_fraction))
        # print(type(random_index_of_A_players))
        for index , focal in enumerate(self.agents):

            if index in random_index_of_A_players:
                focal.strategy = "A"
            else:
                focal.strategy= "B"

    def determine_coordinator_or_anticoordinator(self,coordinating_fraction,co_list):
        # population = len(self.agents)
        # selection = [i for i in range(population)]
        # coordinators_num = int(population*coordinating_fraction)
        # random_index_of_Coordinators = rnd.sample(range(population), k=coordinators_num)
        # for population_co in range(population+1): # to population
            # total_co_set = # every state with current population_co
            # data = itertools.combinations(selection, population_co)
            # sublists = list(data)
            # i = 0
        for index, focal in enumerate(self.agents):
            if index in co_list:
                focal.rule = "CO"
            else:
                focal.rule = "ANTI"
            # i= i+1

    #         if t >= 100 and np.absolute(np.mean(fc_hist[t-100:t-1]) - fc)/fc < 0.001:
    #             fc_converged = np.mean(fc_hist[t-99:t])
    #             comment = "Fc(converged)"
    #             print(comment)
    #             break
    #
    #         if t == tmax:
    #             fc_converged = np.mean(fc_hist[t-99:t])
    #             comment = "Fc(final timestep)"
    #             print(comment)
    #             break
    #
    #     # print(f"Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, {comment}:{fc_converged:.3f}")
    #     # result.to_csv(f"time_evolution_Dg_{Dg:.1f}_Dr_{Dr:.1f}.csv")
    #
    #
    #     return fc_converged
    #
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
                labels[index] = "CO"
            else:
                labels[index] = "ANTI"

        nx.draw_networkx_labels(self.network, pos, labels, font_size=16)
        eq_str = ""
        if equilibrated:
            eq_str = "Equilibrated!"
        plt.title(f"t={timestep}  {eq_str}", fontsize=20)
        plt.axis = "off"
        time_past_eq = -1
        # if equilibrated == 1:
        #     time_past_eq = time_past_eq +1
        #     # eq_time = timestep
        #     fig,ax = plt.subplots()
        #     ax.set_xlabel(f"equilibrated at time {timestep-time_past_eq} !")
        plt.xticks([])
        plt.yticks([])
        plt.savefig(f"data/images/snap_t={timestep}.png")
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
        # print(self.agents)
        # if A_count != B_count :
        #     equilibrated = 0
        return equilibrated,A_count,B_count


    def one_episode(self, episode,A_B_fraction,time_steps,coordinating_fraction,result,non_eq,threshold,co_list):
        self.__initialize_label_A_or_B(A_B_fraction)
        self.determine_coordinator_or_anticoordinator(coordinating_fraction,co_list)

        # if(self.updating_activation_sequence == "synchronous"):
        #    active_agents =  self.__choose_cooperators_if_synchronous()
        # elif(self.updating_activation_sequence == "asynchronous"):
        #     active_agents = self.__choose_cooperators_if_asynchronous()
        # else:
        #     active_agents = self.__choose_cooperators_if_partial()
        # print(self.agents[0])
        # print(type(self.agents[0]))
        # global new_result,result,non_eq
        equilibrated = -1

        equilibrated_array=[]
        for t in range(time_steps):
            for index in range(self.population):
                self.agents[index].previous_strategy = self.agents[index].strategy
            for index in self.cooperators:
                (self.agents[index]).decide_next_strategy(self.agents,self.Z_func,threshold)
            for index in self.cooperators:
                (self.agents[index]).update_strategy()
            equilibrated, A_count, B_count = self.has_equilibrated()
            # self.__take_snapshot(t,equilibrated)
            equilibrated_array.append(equilibrated)


            # new_result = pd.DataFrame(
            #     [[equilibrated, self.population, A_B_fraction, coordinating_fraction, t]],
            #     columns=['Eq', 'population', 'A', 'B', 'coordinating_fraction', 'time'])
            # results = results.append(new_result)
        eq_time = -1

        if(equilibrated == 1):
            eq_time =0
            for tt in range(time_steps-1,0,-1):
                if equilibrated_array[tt]==0:
                    eq_time = tt
                    break
        list_to_show = []
        for i in range(self.population):
            if i in co_list:
                list_to_show.append("C")
            else:
                list_to_show.append("A")

        new_result = pd.DataFrame(
            {'list': [list_to_show], 'Eq': [equilibrated], 'population': [self.population], 'A/B': [A_B_fraction],
             'coordinating_fraction': [coordinating_fraction], 'equilibration time': [eq_time]})
        # if (equilibrated == 0):
            # non_eq =  non_eq.append(new_result)
            # non_eq.to_csv("data/csv/diagram_non_eqs.csv")
            # with open(f"data/csv/diagram_non_eqs.csv", 'a') as f_object:
            #     writer_object = writer(f_object)
            #     writer_object.writerow(new_result)
            #     f_object.close()
        print(f"Equilibrated = {equilibrated}     time = {eq_time}")
        # new_result = pd.DataFrame([[co_list,equilibrated,self.population,A_B_fraction,coordinating_fraction,eq_time]],
        #                               columns=['list','Eq','population','A/B','coordinating_fraction','equilibration time'])

        # print(new_result)
        # new_result = pd.DataFrame({'list':[co_list],'Eq':equilibrated,'population':self.population,'A/B':A_B_fraction,'coordinating_fraction':coordinating_fraction,'equilibration time':eq_time})
        # a = pd.DataFrame({'year': [2019], 'make': ["Mercedes"], 'model': ["C-Class"]})
        # print(new_result)
        # result.append(new_result)
        #print(self.network)
        # res_row = [equilibrated,self.population,A_B_fraction,coordinating_fraction,eq_time]

        # columns = ['list', 'Eq', 'population', 'A/B', 'coordinating_fraction', 'equilibration time']
        # csv_file = pd.read_csv(f"data/csv/diagram.csv",names = columns)
        # result.append(new_result)
        # result.to_csv(f"data/csv/diagram.csv")
        return new_result,equilibrated
        # with open(f"data/csv/diagram.csv", 'a') as f_object:
        #     writer_object = writer(f_object)
        #     writer_object.writerow(new_result)
        #     f_object.close()
        #
        # with open(f"data/csv/diagram_non_eqs.csv", 'a') as f_object:
        #     writer_object = writer(f_object)
        #     writer_object.writerow(new_result)
        #     f_object.close()

        # results.to_csv(f"diagram{episode}.csv")
        # results.to_csv(f"data/csv/diagram.csv")
        # append_list_as_row(f"data/csv/diagram.csv", res_row)

