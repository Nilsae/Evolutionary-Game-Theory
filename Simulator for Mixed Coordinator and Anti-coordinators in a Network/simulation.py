import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from agent import Agent
import time

class Simulation:
    
    def __init__(self, population, average_degree, network_type,updating_activation_sequence,time_steps,coordinating_fraction):
        """
        network_type has several options, give following network type as string;
            1. lattice
            2. ring
            3. ER-random
            4. Complete (Not recommended!!! Too heavy!!!)
            4. Watts Strogatz(Small World)
            5. BA-SF
        """

        self.network_type = network_type
        self.network = None
        self.agents = self.__generate_agents(population, average_degree)
        # self.cooperators = self.choose
        self.time_steps = time_steps
        self.updating_activation_sequence = updating_activation_sequence
        self.coordinating_fraction = coordinating_fraction
        self.population = population
        self.average_degree = average_degree
        if(self.updating_activation_sequence == "synchronous"):
           self.active_agents =  self.__choose_cooperators_if_synchronous()
        elif(self.updating_activation_sequence == "asynchronous"):
            self.active_agents = self.__choose_cooperators_if_asynchronous()
        else:
            self.active_agents = self.__choose_cooperators_if_partial()

    def __generate_agents(self, population, average_degree):
        if self.network_type == "lattice":
            self.network = self.__generate_lattice(population)
            
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

        agents = [Agent(self.network,id) for id in range(population)]
        # agents = []
        # for id in range(population):
        #     agents.append(Agent(self.network,id))

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

    def __initialize_label_A_or_B(self):

        population = len(self.agents)
        random_index_of_A_players = rnd.sample(range(population), k=int(population / 2))
        print(type(random_index_of_A_players))
        for index , focal in enumerate(self.agents):

            if index in random_index_of_A_players:
                focal.strategy = "A"
            else:
                focal.strategy= "B"
        """Initialize the strategy of agents"""
        #
        # for index, focal in enumerate(self.agents):
        #     if index in self.initial_cooperators:
        #         focal.strategy = "C"
        #     else:
        #         focal.strategy = "D"
        #     print(focal.strategy)
        #     print(focal.rule)
    def determine_coordinator_or_anticoordinator(self):
        population = len(self.agents)
        coordinators_num = int(population*self.coordinating_fraction)
        random_index_of_Coordinators = rnd.sample(range(population), k=coordinators_num)
        for index, focal in enumerate(self.agents):
            if index in random_index_of_Coordinators:
                # print(index)

                focal.rule = "CO"
            else:
                focal.rule = "ANTI"
    # def __count_payoff(self, Dg, Dr):
    #     """Count the payoff based on payoff matrix"""
    #
    #     R = 1       # Reward
    #     S = -Dr     # Sucker
    #     T = 1+Dg    # Temptation
    #     P = 0       # Punishment
    #
    #     for focal in self.agents:
    #         focal.point = 0.0
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

    # def __update_strategy(self, rule ="CO"):
    #     for focal in self.agents:
    #         focal.decide_next_strategy(self.agents, rule = rule)
    #
    #     for focal in self.agents:
    #         focal.update_strategy()
    #
    # def __count_fc(self):
    #     """Calculate the fraction of cooperative agents"""
    #
    #     fc = len([agent for agent in self.agents if agent.strategy == "C"])/len(self.agents)
    #
    #     return fc

    # def __play_game(self, episode):

    #     """Continue games until fc gets converged"""
    #     tmax = 3000
    #
    #     self.__initialize_strategy()
    #     initial_fc = self.__count_fc()
    #     fc_hist = [initial_fc]
    #     print(f"Episode:{episode}, Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time: 0, Fc:{initial_fc:.3f}")
    #     # result = pd.DataFrame({'Time': [0], 'Fc': [initial_fc]})
    #
    #     for t in range(1, tmax+1):
    #         # self.__count_payoff(Dg, Dr)
    #         self.__update_strategy(rule = "IM")
    #         fc = self.__count_fc()
    #         fc_hist.append(fc)
    #         print(f"Episode:{episode}, Dr:{Dr:.1f}, Dg:{Dg:.1f}, Time:{t}, Fc:{fc:.3f}")
    #         # new_result = pd.DataFrame([[t, fc]], columns = ['Time', 'Fc'])
    #         # result = result.append(new_result)
    #         converged_num=0
    #         # Convergence conditions
    #         if fc == 0 or fc == 1:
    #             fc_converged = fc
    #             converged_num = converged_num+1
    #             comment = "Fc(0 or 1"
    #             print(comment)
    #             break
    #
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



    def one_episode(self, episode):
        self.__initialize_label_A_or_B()
        self.determine_coordinator_or_anticoordinator()
        # if(self.updating_activation_sequence == "synchronous"):
        #    active_agents =  self.__choose_cooperators_if_synchronous()
        # elif(self.updating_activation_sequence == "asynchronous"):
        #     active_agents = self.__choose_cooperators_if_asynchronous()
        # else:
        #     active_agents = self.__choose_cooperators_if_partial()
        # print(self.agents[0])
        # print(type(self.agents[0]))
        global new_result
        equilibrated = -1
        results = pd.DataFrame({'Eq': [], 'population': [], 'A': [], 'B': [],
                               'coordinating_fraction': [], 'time': []})
        for t in range(self.time_steps):
            for index in range(self.population):
                self.agents[index].previous_strategy = self.agents[index].strategy
                # print(f"{self.agents[index].strategy}  a neighbors:{self.agents[index].A_neighbors_count}")
            for index in self.cooperators:
                (self.agents[index]).decide_next_strategy(self.agents)
            for index in self.cooperators:
                (self.agents[index]).update_strategy()
            equilibrated, A_count, B_count = self.has_equilibrated()
            self.__take_snapshot(t,equilibrated)
            print("------------")

            # A_count =0
            # B_count =0
            # equilibrated =0
            # for agent in self.agents:
            #     if agent.strategy == "A":
            #         A_count = A_count + 1
            #     elif agent.strategy == "B":
            #         B_count = B_count + 1
            #     if A_count != B_count :
            #         equilibrated = 0
            #     elif for
            new_result = pd.DataFrame(
                [[equilibrated, self.population, A_count, B_count, self.coordinating_fraction, t]],
                columns=['Eq', 'population', 'A', 'B', 'coordinating_fraction', 'time'])
            results = results.append(new_result)
            # nx.draw(self.network)
            # time.sleep(0.5)

        # equilibrated, A_count, B_count = self.has_equilibrated()
        # if equilibrated:
        print(f"Equilibrated = {equilibrated}       A = {A_count} B = {B_count} time = {self.time_steps}")
        new_result = pd.DataFrame([[equilibrated,self.population,A_count,B_count,self.coordinating_fraction,self.time_steps]],
                                      columns=['Eq','population','A','B','coordinating_fraction','time'])
        print(self.network[1])
        # nx.draw(self.network)
        # plt.savefig("1.png")
        # self.__take_snapshot(self.time_steps)

        # equilibrated, A_count, B_count = self.has_equilibrated()
        # if not equilibrated:
        #     print(f"Did'nt Equilibrate!{equilibrated}  in time {self.time_steps} A = {A_count} B = {B_count}")
        #     new_result = pd.DataFrame([[equilibrated, self.population, A_count, B_count, self.coordinating_fraction, self.time_steps]],
        #                               columns=['Eq', 'population', 'A', 'B', 'coordinating_fraction', 'time'])

        # for index in range (100):
        #     print(f"{index} {self.agents[index].strategy}")
        results = results.append(new_result)
        # results.to_csv(f"diagram{episode}.csv")
        results.to_csv(f"data/csv/diagram.csv")



    #     """Run one episode"""
    #
    #     # result = pd.DataFrame({'Dg': [], 'Dr': [], 'Fc': []})
    #     result = pd.DataFrame({'A_count': [], 'B_count': [], 'Fc': []})
    #     self.__choose_initial_cooperators()
    #
    #     for Dr in np.arange(0, 1.1, 0.1):
    #         for Dg in np.arange(0, 1.1, 0.1):
    #             fc_converged = self.__play_game(episode, Dg, Dr)
    #             # new_result = pd.DataFrame([[format(Dg, '.1f'), format(Dr, '.1f'), fc_converged]], columns = ['Dg', 'Dr', 'Fc'])
    #             new_result = pd.DataFrame([fc_converged],columns=['Fc'])
    #             result = result.append(new_result)

        # result.to_csv(f"phase_diagram{episode}.csv")
