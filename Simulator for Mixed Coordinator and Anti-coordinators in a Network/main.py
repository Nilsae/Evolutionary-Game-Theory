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
    6. random_tree
    7. full_r_ary
    
Z_func options:
    1. previous
    2. A
    3. random
"""

def main():
    population = 9 # Agent number
    average_degree = 8          # Average degree of social network
    num_episode = 1    # Number of total episode in a single simulation for taking ensemble average
    network_type = "ring"    # topology of social network
    updating_activation_sequence = "asynchronous"
    time_steps = 701
    # coordinating_fraction = 1/2
    # A_B_fraction = 1/2
    threshold = 1/2
    Z_func = "A"
    dim = (2,3,1)
    episode =1

    equilibrable= 0
    always_equilibrates = 1
    global new_result

    always_eq = pd.DataFrame({'Eq': [],'co_list': [],'a_list': [],'het_list': [],  'population': [], 'equilibration time': []})
    nonables =  pd.DataFrame({'Eq': [],'co_list': [],'a_list': [],'het_list': [],   'population': [], 'equilibration time': []})
    result =    pd.DataFrame({'Eq': [],'co_list': [],'a_list': [],'het_list': [],   'population': [], 'equilibration time': []})
    non_eq =    pd.DataFrame({'Eq': [],'co_list': [],'a_list': [],'het_list': [],   'population': [], 'equilibration time': []})
#     colist_for_31 = ['+','-','-', '+', '+', '+', '-']
    for population in range(3,5):
        selection = [i for i in range(population)]
        print(f'population = {population}\n')
        for population_co in range(population+1): # to population
            data_co = itertools.combinations(selection, population_co)
            sublists_co = list(data_co)

            for i in range(len(sublists_co)):
                co_list = sublists_co[i]
                co_list_to_show = []
                a_list_to_show = []
                het_list_to_show=[]
                for i in range(population):
                    if i in co_list:
                        co_list_to_show.append("+")
                    else:
                        co_list_to_show.append("-")
                # for i in range(population):
                #     if i in het_list:
                #         het_list_to_show.append("Q")
                #     else:
                #         het_list_to_show.append("o")
                # print(co_list_to_show)
                # adj_anti = 0
                # for index,strategy in enumerate(co_list):
                #     if co_list[index] =='-' and co_list[index+1] =='-' and co_list[index+2] =='-' and co_list[index+3] =='+':
                #

                for population_a in range(population +1):
                    data_a = itertools.combinations(selection, population_a)
                    sublists_a = list(data_a)

                    # if population>8:
                    #     a_list = sublists_a[0]
                    #     simulation = Simulation(population, average_degree, network_type, updating_activation_sequence,
                    #                             dim, Z_func)
                    #     # random.seed()
                    #     new_result, equilibrated, eq_time = simulation.one_episode(episode, time_steps, result, non_eq,
                    #                                                                threshold,
                    #                                                                co_list, a_list,het_list)
                    #     # print(type(new_result))
                    #
                    #     result = result.append(new_result)
                    #     if equilibrated == 1 and eq_time < 2 * time_steps / 3:
                    #         equilibrable = 1
                    #         non_eq = non_eq.append(new_result)
                    #     else:
                    #         always_equilibrates = 0
                    # else:
                    for i in range(len(sublists_a)):
                        a_list = sublists_a[i]
                        # a_list = [1,3,5,7,9]
                        for population_het in range(population + 1):
                            data_het = itertools.combinations(selection, population_het)
                            sublists_het = list(data_het)
                            for j in range(len(sublists_het)):
                                het_list = sublists_het[j]

                                simulation = Simulation(population, average_degree, network_type, updating_activation_sequence, dim, Z_func)
                                # random.seed()
                                new_result,equilibrated,eq_time = simulation.one_episode(episode, time_steps,result,non_eq, threshold,
                                                       co_list,a_list,het_list)
                                # print(type(new_result))

                                result = result.append(new_result)
                                if equilibrated==1 and eq_time<2*time_steps/3:
                                    equilibrable =1
                                    non_eq = non_eq.append(new_result)
                                else:
                                    always_equilibrates =0

                if equilibrable == 0:
                    nonables = nonables.append(new_result)
                    # print(new_res_res)
                    print(f"nonable  ",new_result)

                equilibrable =0
                if always_equilibrates==1:
                    always_eq = always_eq.append((new_result))
                    print(f"always",new_result)
                    # print(always_eq)
                always_equilibrates =1
# # .

    ##################################################################################################################
#     sign_co_list =['+', '+', '-', '-', '-', '+', '-', '-', '-']
#     alphabet_strategy  =[]
#     co_list = []
#     a_list = []
#     for index,value in enumerate(sign_co_list):
#         if sign_co_list[index]=='+':
#             co_list.append(index)
#     # for index,value in enumerate(alphabet_strategy):
#     #     if alphabet_strategy[index]=='A':
#     #         a_list.append(index)
#     # equilibrable= 0
#     # co_list = [0]
#     # a_list = [1, 3, 5, 7, 9]
#     selection = [i for i in range(population)]
#     for population_a in range(population +1):
#         data_a = itertools.combinations(selection, population_a)
#         sublists_a = list(data_a)
#         for i in range(len(sublists_a)):
#             a_list = sublists_a[i]
#             simulation = Simulation(population, average_degree, network_type, updating_activation_sequence, dim, Z_func)
#         # random.seed()
#             new_result,equilibrated,eq_time = simulation.one_episode(episode, time_steps,result,non_eq, threshold,
#                                    co_list,a_list)
#             # print(new_result)
#             result = result.append(new_result)
#             if equilibrated== 0 or eq_time>2*time_steps/3:
#                 non_eq = non_eq.append(new_result)
#                 print(new_result)
#             else:
#                 equilibrable = 1
#                 print(new_result)
#

    result.to_csv(f"data/csv/total_hetero.csv")
    non_eq.to_csv(f"data/csv/non_eq_hetero.csv")
    nonables.to_csv(f"data/csv/non_equilibrable_hetero.csv")
    always_eq.to_csv(f"data/csv/always_equilibrates_hetero.csv")
#     if equilibrable ==0:
#         print("*********************non-equilibrable************************8")
    # ##################################################################################################################
# #
#
#     col_list = ["co_list"]
#     df = pd.read_csv("data/csv/non_equilibrable_ring_1_13.csv", usecols=col_list)
#     for i in range(1,203):
#         co_str = df["co_list"][i]
#         # print(co_str)
#         str = co_str[1:-1]
#         str = str[1:-1]
#         sign_co_list = list(str.split("', '"))
#         co_list = []
#         # print(sign_co_list)
#         for index,value in enumerate(sign_co_list):
#             print(index)
#             if sign_co_list[index]=='+':
#                 # print(index)
#                 co_list.append(index)
#
#         # print(co_list)
#         population = len(sign_co_list)
#         if population>6 :
#             break
#         print(population)
#         selection = [i for i in range(population)]
#         for population_a in range(population +1):
#             data_a = itertools.combinations(selection, population_a)
#             sublists_a = list(data_a)
#             for i in range(len(sublists_a)):
#                 a_list = sublists_a[i]
#                 simulation = Simulation(population, average_degree, network_type, updating_activation_sequence, dim, Z_func)
#                 new_result,equilibrated,eq_time = simulation.one_episode(episode, time_steps,result,non_eq, threshold,
#                                        co_list,a_list)
#                 if equilibrated == 0 or eq_time > time_steps - 30:
#                     result = result.append(new_result)
#                     print(new_result)
#
#     result.to_csv(f"data/csv/heterogeneous-co-barax.csv")
if __name__ == '__main__':
    main()
