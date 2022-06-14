import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from agent import Agent
import time
from csv import writer
import itertools


def plus(idd, number, population):
    if idd + number >= population:
        return idd + number - population - 1
    else:
        return idd + number


def minus(idd, number, population):
    if idd + number <= 0:
        return population - idd
    else:
        return idd - 1


class Simulation:
    def __init__(self, population, z_func, strategy_list, type_list, activated_list, desired_eq):
        self.network = None
        self.Z_func = z_func
        self.population = population
        self.strategy_list = strategy_list
        self.type_list = type_list
        self.activated_list = activated_list
        self.desired_eq = desired_eq
        self.agents = self.__generate_agents()

    def __generate_agents(self):
        self.network = nx.circulant_graph(self.population, [1])  # ring only
        agents = [Agent(self.network, self.Z_func, i) for i in range(self.population)]
        for index, focal in enumerate(agents):
            neighbors_id = list(self.network[index])
            print(neighbors_id)
            for nb_id in neighbors_id:
                focal.neighbors_id.append(nb_id)
        return agents

    def __initialize_label_A_or_B(self):
        for index, focal in enumerate(self.agents):
            focal.strategy = self.strategy_list[index]

    def determine_coordinator_or_anticoordinator(self, co_list):
        for index, focal in enumerate(self.agents):
            if self.type_list[index] == '+':
                focal.type = "+"
            else:
                focal.type = "-"

    def __take_snapshot(self, timestep, equilibrated):

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

        color = dict((i, color(i)) for i in self.network.nodes())
        # if self.network_type == "ring":
        pos = nx.circular_layout(self.network)
        #
        # else:
        #     pos = nx.spring_layout(self.network)

        nx.draw_networkx_edges(self.network, pos)
        nx.draw_networkx_nodes(self.network, pos, node_color=list(color.values()), node_size=500)
        labels = {}
        for index, focal in enumerate(self.agents):
            if focal.type == "+":
                labels[index] = f"{index},+"
            else:
                labels[index] = f"{index},-"

        nx.draw_networkx_labels(self.network, pos, labels, font_size=16)
        eq_str = ""
        if equilibrated:
            eq_str = "Equilibrated!"
        plt.title(f"t={timestep}  {eq_str}", fontsize=20)
        plt.axis = "off"
        time_past_eq = -1

        plt.xticks([])
        plt.yticks([])
        plt.savefig(f"snap_t={timestep}.png", dpi=300)
        plt.close()

    def has_equilibrated(self):
        equilibrated = 1
        for index, focal in enumerate(self.agents):
            if focal.strategy != focal.previous_strategy:
                equilibrated = 0
                break

        return equilibrated

    def one_episode(self, time_steps, threshold):
        reached_desired = 0
        self.__initialize_label_A_or_B()
        self.determine_coordinator_or_anticoordinator(self.type_list)
        equilibrated = -1
        equilibrated_array = []
        current_strategy_list = self.strategy_list
        for t in range(time_steps):
            for f in self.agents:
                print("id: " + str(f.id) + " type: " + f.type + " strategy: " + f.strategy + " willing to be: " + str(
                    f.next_strategy))
            for i in range(self.population):
                self.agents[i].previous_strategy = self.agents[i].strategy
                # if(t == time_steps-1):

                (self.agents[i]).decide_next_strategy(self.agents, self.Z_func, threshold)
                print("next strategy in this timestep is decided for everyone!")
                current_strategy_list[i] = self.agents[i].strategy
                reached_desired = (self.strategy_list == current_strategy_list)
            # RANDOM AGENT TO BE ACTIVATED
            # index_list = rnd.sample(range(self.population), k = 1)#########GGG#####
            # index = index_list[0]
            # AGENT TO BE ACTIVATED UNDER OUR POLICY:
            index = self.activate_policy()
            print("in this timestep agent to be activated and updated has been selected: agent " + str(index))

            # if index!=0 and index!= self.population-1:
            if index != -1:
                # for index in self.cooperators: (everybody is cooperating)
                #                 (self.agents[index]).decide_next_strategy(self.agents, self.Z_func, threshold)
                print("selected agent next strategy: " + self.agents[index].next_strategy)
                # for index in self.cooperators:
                (self.agents[index]).update_strategy()
                # self.agents[index].next_strategy = (self.agents[index]).strategy
            else:
                print("no one found\n")
                break
            equilibrated = self.has_equilibrated()
            self.__take_snapshot(t, equilibrated)
            print("selected agent : " + str(index))
            equilibrated_array.append(equilibrated)
        eq_time = -1

        new_result = pd.DataFrame(
            {'reached_desired?': [reached_desired], 'Equilibrated?': [equilibrated], 'types': [self.type_list],
             'initial strategy set': [self.strategy_list], 'final strategy set': [current_strategy_list],
             'equilibration time': [eq_time]})
        return new_result, equilibrated, eq_time, reached_desired

    def activate_policy(self):
        c1 = []
        c2 = []
        c3 = []
        for agent in self.agents:
            w = (agent.strategy == self.desired_eq[agent.id])
            B = (agent.strategy != agent.next_strategy)
            print("w=" + str(w), "B = " + str(B))
            if B == 1:
                if agent.strategy == 'B' and agent.type == '+' \
                        and (self.strategy_list[plus(agent.id, 1, self.population)] == 'A' \
                             or self.strategy_list[
                                 minus(agent.id, 1, self.population)] == 'A'):  # if agent[i+1]= A or agent[i-1] = A:
                    c3.append(agent.id)  # add agent i to c3
                elif (agent.strategy == 'B') and \
                        ((self.strategy_list[plus(agent.id, 1, self.population)] == 'B' and \
                          self.type_list[plus(agent.id, 1, self.population)] == '-' and \
                          self.strategy_list[plus(agent.id, 2, self.population)] == 'A' and \
                          self.type_list[plus(agent.id, 2, self.population)] == '-') or \
                         (self.strategy_list[minus(agent.id, 1, self.population)] == 'B' and \
                          self.type_list[minus(agent.id, 1, self.population)] == '-' and \
                          self.strategy_list[minus(agent.id, 2, self.population)] == 'A' and \
                          self.type_list[minus(agent.id, 2,
                                               self.population)] == '-')):  # else if (agent[i+1] = B- and agent[i+2] = A-) or (agent[i-1] = B- and agent[i-2] = A-):
                    c3.append(agent.id)  # add agent i to c3
                elif (agent.strategy == 'A' and agent.type == '-') and \
                        ((self.strategy_list[plus(agent.id, 1, self.population)] == 'A' and \
                          self.type_list[plus(agent.id, 1, self.population)] == '-') or \
                         (self.strategy_list[minus(agent.id, 1, self.population)] == 'A' and \
                          self.type_list[minus(agent.id, 1, self.population)] == '-')):
                    c3.append(agent.id)  # else if agent i = A- and(agent i+1 = A- or agent i-1 = A-)
                    # add agent i to c3
                else:
                    if w == 0:
                        c1.append(agent.id)
                    else:
                        c2.append(agent.id)
        print("c1: " + str(c1) + " c2: " + str(c2) + " c3: " + str(c3))
        for i in range(self.population):
            if i in c1:
                self.activated_list[i] = 1
                return i
        for i in range(self.population):
            if i in c2 and self.activated_list[i] == 0:
                self.activated_list[i] = 1
                return i
        for i in range(self.population):
            if i in c3:
                self.activated_list[i] = 1
                return i

        return -1
