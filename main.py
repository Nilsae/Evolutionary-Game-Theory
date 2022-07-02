from simulation import Simulation
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from eq import equilibrated_func
from numpy import zeros
import random
import pandas as pd
import itertools
from pandas import concat


def main():
    # population = 9  # number of agents
    time_steps = 30
    threshold = 1 / 2
    Z_func = "A"  # the next strategy if number of A-playing neighbors equlas B-playing ones
    global new_result
    result = pd.DataFrame(
        {'reached_desired?': [], 'Equilibrated?': [], 'types': [], 'initial': [], 'final': [],
         'desired': []})
    # algorithm works on:
    # desired_eq = ['A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A']  # desired equilibrium strategy of the agents
    # type_list = ['+', '+', '-', '-', '-', '+', '-', '-',
    #              '-']  # coordinator or anticoordinator listed identified by + and - signs
    # initial_strategy = ['B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']  # initial strategy of the agents

    # it also works on: (original example ;))
    #     desired_eq = ['A', 'B', 'A', 'A', 'B', 'A', 'A', 'A']  # desired equilibrium strategy of the agents
    #     type_list = ['+', '-', '-', '+', '-', '-', '+', '+']  # coordinator or anticoordinator listed identified by + and - signs
    #     initial_strategy = ['B', 'B', 'B', 'B', 'B', 'B', 'B','B']  # initial strategy of the agents# selection = [i for i in range(population)]
    # brute force:

    for population in range(5, 6):
        selection_co = [i for i in range(population)]
        for population_co in range(population + 1):  # to population
            data_co = itertools.combinations(selection_co, population_co)
            sublists_co = list(data_co)
            for i in range(len(sublists_co)):
                co_list = sublists_co[i]
                type_list = []
                co_num = 0
                for j in range(population):
                    if j in co_list:
                        type_list.append("+")
                        co_num = co_num + 1
                    else:
                        type_list.append("-")
                desired_record = []
                print("***typelist= " + str(type_list) + " ***")
                selection_desired_eq = [i for i in range(population - co_num)]
                for population_desired_eq in range(population - co_num + 1):  # to population
                    data_desired_eq = itertools.combinations(selection_desired_eq, population_desired_eq)
                    sublists_desired_eq = list(data_desired_eq)
                    for k in range(len(sublists_desired_eq)):
                        desired_eq_list = sublists_desired_eq[k]
                        desired_eq = [] * population
                        for h in range(population):
                            if h in co_list:
                                desired_eq.append('A')
                            elif (h > 0 and desired_eq[h - 1] == 'B') or (h == population - 1 and desired_eq[0] == 'B'):
                                desired_eq.append('A')
                            elif h not in desired_eq_list:
                                desired_eq.append('B')
                            else:
                                desired_eq.append('A')
                        # # desired_eq = list(dict.fromkeys(desired_eq))
                        # if desired_eq not in desired_record:
                        #     desired_record.append(desired_eq)
                        # else:
                        #     continue
                        if not equilibrated_func(desired_eq, type_list, population):
                            continue
                        selection_init = [i for i in range(population)]
                        for population_init in range(population + 1):  # to population
                            data_init = itertools.combinations(selection_init, population_init)
                            sublists_init = list(data_init)
                            for z in range(len(sublists_init)):
                                init_list = sublists_init[z]
                                initial_strategy = []
                                for v in range(population):
                                    if v in init_list:
                                        initial_strategy.append("A")
                                    else:
                                        initial_strategy.append("B")
                                isABA = 0
                                for dele in range(population):
                                    if dele+1 == population :
                                        initial_n1 = initial_strategy[0]
                                        initial_n2 = initial_strategy[1]
                                        type_n1 = type_list[0]
                                        type_n2 = type_list[1]
                                    elif dele+2 == population :
                                        initial_n1 = initial_strategy[dele+1]
                                        initial_n2 = initial_strategy[0]
                                        type_n1 = type_list[dele + 1]
                                        type_n2 = type_list[0]
                                    else:
                                        initial_n1 = initial_strategy[dele + 1]
                                        initial_n2 = initial_strategy[dele+2]
                                        type_n1 = type_list[dele + 1]
                                        type_n2 = type_list[dele + 2]

                                    if (initial_strategy[dele] == 'A' and initial_n1 == 'B' and initial_n2 == 'A' \
                                        and type_list[dele] == '-' and type_n1 == '-' and type_n2 == '-'):
                                        isABA=1
                                        break
                                if isABA == 1:
                                    continue
                                # do the work:
                                init_string = str(initial_strategy)
                                print("init: " + init_string + "\ndesired: " + str(desired_eq) + "\ntypes: " + str(
                                    type_list))
                                activated_list = zeros(population)
                                simulation = Simulation(population, Z_func, initial_strategy, type_list, activated_list,
                                                        desired_eq, init_string)
                                new_result, equilibrated, eq_time, reached_desired = simulation.one_episode(time_steps,
                                                                                                            threshold)
                                # result = pd.DataFrame.from_records
                                if reached_desired == 0:
                                    result = result.append(new_result)
                                    print("desired: " + str(desired_eq))
                                    print("init:    " + init_string)
        result.to_csv(f"newfile{population}.csv")


if __name__ == '__main__':
    main()
# focus on the number of times one agent must be allowed to be activated
