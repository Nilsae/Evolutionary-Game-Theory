#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simulation import Simulation
import random
import  pandas as pd

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
    population = 20 # Agent number
    average_degree = 8          # Average degree of social network
    num_episode = 10     # Number of total episode in a single simulation for taking ensemble average
    network_type = "ring"    # topology of social network
    updating_activation_sequence = "synchronous"
    time_steps = 70
    coordinating_fraction = 1/2
    A_B_fraction = 1/2
    Z_func = "previous"
    dim = (2,3,4)
    simulation = Simulation(population, average_degree, network_type,updating_activation_sequence  ,dim ,Z_func )
    results = pd.DataFrame({'Eq': [], 'population': [], 'A/B': [],
                            'coordinating_fraction': [], 'equilibration time': []})
    for episode in range(num_episode):
        # A_B_fraction = 1/(episode +1)
        random.seed()
        simulation.one_episode(episode,A_B_fraction,time_steps,coordinating_fraction,results)

if __name__ == '__main__':
    main()
