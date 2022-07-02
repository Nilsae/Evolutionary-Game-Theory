import numpy as np
import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time
from csv import writer
import itertools


def equilibrated_func(current_strtegy_list, type_list, population):
    willing_list = [""] * population
    for agent_id in range(population):
        if type_list[agent_id] == '+':
            willing_list = coordinating(agent_id, current_strtegy_list, willing_list, population)
        else:
            willing_list = anti_coordinating(agent_id, current_strtegy_list, willing_list, population)

    equilibrated = 1
    for agent_id in range(population):
        if current_strtegy_list[agent_id] != willing_list[agent_id]:
            equilibrated = 0
            break

    return equilibrated


def coordinating(agent_id, current_strategy_list, willing_list, population):
    A_neighbors_count = 0
    B_neighbors_count = 0
    total_neighbors_count = 2
    neighbors = [] * total_neighbors_count
    if agent_id == 0:
        neighbors = [population - 1, 1]
    elif agent_id == population - 1:
        neighbors = [population - 2, 0]
    else:
        neighbors = [agent_id - 1, agent_id + 1]

    for neighbor_id in neighbors:
        if current_strategy_list[neighbor_id] == "A":
            A_neighbors_count = A_neighbors_count + 1
        else:
            B_neighbors_count = B_neighbors_count + 1
    print(agent_id)
    if A_neighbors_count >= B_neighbors_count:
        willing_list[agent_id] = "A"
    else:
        willing_list[agent_id] = "B"

    return willing_list


def anti_coordinating(agent_id, current_strategy_list, willing_list, population):
    A_neighbors_count = 0
    B_neighbors_count = 0
    total_neighbors_count = 2
    neighbors = [] * total_neighbors_count
    if agent_id == 0:
        neighbors = [population - 1, 1]
    elif agent_id == population - 1:
        neighbors = [population - 2, 0]
    else:
        neighbors = [agent_id - 1, agent_id + 1]

    for neighbor_id in neighbors:
        if current_strategy_list[neighbor_id] == "A":
            A_neighbors_count = A_neighbors_count + 1
        else:
            B_neighbors_count = B_neighbors_count + 1
    #     print(agent_id)
    #     print(willing_list)
    if A_neighbors_count <= B_neighbors_count:
        willing_list[agent_id] = "A"
    else:
        willing_list[agent_id] = "B"
    return willing_list



