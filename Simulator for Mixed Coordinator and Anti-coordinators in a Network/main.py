#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simulation import Simulation
import random
import  pandas as pd
import itertools
"""
network_type options:
    1. lattice
    2. ring
    3. ER-random
    4. Complete
    4. Watts Strogatz(Small World)
    5. BA-SF
    
Z_func options:
    1. previous
    2. A
    3. random
"""

def main():
    population = 7 # Agent number
    average_degree = 8          # Average degree of social network
    num_episode = 1    # Number of total episode in a single simulation for taking ensemble average
    network_type = "ring"    # topology of social network
    updating_activation_sequence = "asynchronous"
    time_steps = 70
    coordinating_fraction = 1/2
    A_B_fraction = 1/2
    threshold = 1/2
    Z_func = "A"
    dim = (2,3,1)
    episode =1

    result = pd.DataFrame({'Eq': [],'co_list': [],'a_list': [],  'population': [], 'equilibration time': []})
    non_eq = pd.DataFrame({'Eq': [],'co_list': [],'a_list': [],  'population': [], 'equilibration time': []})
    for population in range(1,30):
        selection = [i for i in range(population)]
        print(f'population = {population}\n')
        for population_co in range(population+1): # to population
            data_co = itertools.combinations(selection, population_co)


            sublists_co = list(data_co)

            for i in range(len(sublists_co)):

                co_list = sublists_co[i]


                for population_a in range(population +1):
                    data_a = itertools.combinations(selection, population_a)
                    sublists_a = list(data_a)
                    for i in range(len(sublists_a)):
                        a_list = sublists_a[i]
                        simulation = Simulation(population, average_degree, network_type, updating_activation_sequence, dim, Z_func)
                        random.seed()
                        equilibrated = simulation.one_episode(episode, A_B_fraction, time_steps, coordinating_fraction, result,non_eq, threshold,
                                               co_list,a_list)
                        # result = result.append(new_result)
                        # if equilibrated== 0 :
                        #     non_eq = non_eq.append(new_result)
        # result.to_csv(f"data/csv/total{population}.csv")
        # non_eq.to_csv(f"data/csv/non_eq{population}.csv")

if __name__ == '__main__':
    main()
