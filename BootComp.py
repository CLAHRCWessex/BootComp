# -*- coding: utf-8 -*-
"""
Simple bootstrap routine to compare multiple scenarios

Notes: 
    
This seems a lot slower in CPython compared to IronPython and .net.
Use numpy ndarray's for performance increase?
Need to profile code.

"""

import csv

import Bootstrap as bs
import MCC as mcc
import ConvFuncs as cf

CONFIDENCE = 95
N_BOOTS = 10
N_SCENARIOS = 12

def load_scenarios(file_name):
    """
    Reads scenario data from a .csv file (assumes comma delimited).  
    Assumes that each column represents a scenario.
    Returns a list of tuples.  Each tuple are the replications from each
    scenario

    """
    
    with open(file_name, 'r') as csvfile:

        c_reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        columns = list(zip(*c_reader))
        return columns


#note BootStrap routines require lists of lists
scenario_data = cf.list_of_lists(load_scenarios("data/scenarios.csv"))


args =  bs.BootstrapArguments()
args.nboots = N_BOOTS
args.nscenarios = N_SCENARIOS
args.ncomparisons = mcc.pairwise_comparisons_count(N_SCENARIOS)
args.confidence = mcc.bonferroni_adjusted_confidence(CONFIDENCE, N_SCENARIOS)

#Basically we just write a new bootstrap function for what ever type of comparison
#we want to do.  Then assign it to args.boot_function
#compare correlated scenarios using mean differences
args.boot_function = bs.boot_dep_mean_diff   

results = bs.compare_scenarios_pairwise(scenario_data, args)

#the output at this point at percentile CIs (bonferroni adjusted)
print(results)
