#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from simulation import Simulation
import random

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
    population = 300 # Agent number
    average_degree = 8          # Average degree of social network
    num_episode = 1            # Number of total episode in a single simulation for taking ensemble average
    network_type = "ring"    # topology of social network
    updating_activation_sequence = "synchronous"
    time_steps = 200
    coordinating_fraction = 1/2
    A_B_fraction = 1/300
    Z_func = "previous"

    # updating_activation_sequence = "asynchronous"
    # updating_activation_sequence = "partially_synchronous"
    dim = (2,3,4)
    simulation = Simulation(population, average_degree, network_type,updating_activation_sequence  ,dim ,Z_func )

    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode,A_B_fraction,time_steps,coordinating_fraction)

if __name__ == '__main__':
    main()
