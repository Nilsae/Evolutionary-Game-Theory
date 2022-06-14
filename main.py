#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import zeros
import random
import  pandas as pd
from simulation import Simulation
import itertools
from pandas import concat


def main():
    population = 9 # number of agents
    num_episode = 1    # Number of total episode in a single simulation for taking ensemble average
    time_steps =30
    threshold = 1/2
    Z_func = "A" # the next strategy if number of A-playing neighbors equlas B-playing ones
    always_equilibrates = 1
    global new_result
    result = pd.DataFrame({'reached_desired?': [],'Equilibrated?': [],'types': [],'initial strategy set': [],'final strategy set': [],'equilibration time': []})
    desired_eq = ['A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A'] #desired equilibrium strategy of the agents
    type_list = ['+', '+', '-', '-', '-', '+', '-', '-', '-'] #coordinator or anticoordinator listed identified by + and - signs
    initial_strategy  =['B', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'A'] #initial strategy of the agents
    # selection = [i for i in range(population)]
    activated_list = zeros(population)
    simulation = Simulation(population, Z_func, initial_strategy, type_list,activated_list, desired_eq)
    new_result,equilibrated,eq_time,reached_desired = simulation.one_episode(time_steps, threshold)
    result = result.append(new_result)
    result.to_csv(f"newfile.csv")


if __name__ == '__main__':
    main()
