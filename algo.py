
from typing import List
import  pulp as p
import pandas as pd
import numpy as np
import networkx as nx
#https://www.geeksforgeeks.org/python-linear-programming-in-pulp/
#first of all we will cheack a division that Maximizes the sum of the values then we will use a linear programing
# so that the distribution is without envy(i took the terms from the presentation)

def find_max_division(allocation: List[List[float]],salery):
    G = nx.Graph()
    division = {}

    for pla in range(len(allocation)):
        for o in range(len(allocation[0])):
            if allocation[pla][o]>0:
                G.add_edge(("player" ,pla),("object",o),weight = allocation[pla][o])
    PerfectMachGraph = nx.max_weight_matching(G)



    for i in PerfectMachGraph:
        if i[0][0] == "player":
            x= i[0][1]
            y =i[1][1]
            division[x] = y
        else:
            x = i[1][1]
            y =i[0][1]
            division[x] = y

    #now we will do the linare programin with 3 Constraints
    model = p.LpProblem("Problem", p.LpMaximize)
    varaince  = []

    for i in range(len(division)):
        varaince.append(p.LpVariable(str(i)))

    for j in range(len(division)):
        for i in range(len(division)):
            model += (allocation[division[j]][j] - varaince[j]) >= (allocation[division[j]][i] - varaince[i])

    z = p.LpVariable("z")
    for j in range(len(division)):
        model += z <= (allocation[division[j]][j] - varaince[j])

    sum = 0
    for i in range(len(varaince)):
        sum += varaince[i]
    model += sum == salery
    status = model.solve()
    for i in range(len((division))):
        print("room number " + str(i)  +"  "+ str(varaince[i].value()))

if __name__ == '__main__':
    #we give a graph with valuation and the Rent and we will return the agalitary divsion
    print(find_max_division([[1, 2, 4], [5, 20, 3], [7, 1, 3]], 4544))
    print(find_max_division([[1,3 , 5], [5, 20, 3], [9, 6, 3]], 5000))
    print(find_max_division([[1, 6, 4], [5, 20, 3], [7, 1, 4]], 6000))