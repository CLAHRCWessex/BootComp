# -*- coding: utf-8 -*-
"""
Simple bootstrap routine to compare multiple scenarios

Notes: 
    
Discrepency in performance between IronPython.Net and CPython was down
to calculation of the mean of n bootstraps.  

Examplanation: 
data = [1, 2, 3, 4, 5, 6, 7, 9]
statistics.mean(data) = 86ms 
np.mean(mean) = 44.8 ms
np.array(data).mean = 5.74 ms
math.fsum(data)/len(data) = 1.86 ms
sum(data)/len(data) = 1.24 ms

fsum(data) potentially has great precision in floating point arithm than sum(data)

"""

import csv

import Bootstrap as bs
import MCC as mcc
import ConvFuncs as cf

CONFIDENCE = 95
N_BOOTS = 100
N_SCENARIOS = 12  #get number of scenarios from file?

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

args.boot_function = bs.boot_dep_mean_diff   

#Basically we just write a new function for what ever type of comparison
#we want to do.  Then assign it to args.comp_function
#At the moment there are two:
#Bootstrap.percentile_confidence_interval(data, args)
#Bootstrap.proportion_x2_greaterthan_x1(data, args) - is this what you wanted?
    
args.comp_function = bs.percentile_confidence_interval
#args.comp_function = bs.proportion_x2_greaterthan_x1

results = bs.compare_scenarios_pairwise(scenario_data, args)

#the output at this point at percentile CIs (bonferroni adjusted)
print(results)
#need to think about a way to display results cleanly.
