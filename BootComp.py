# -*- coding: utf-8 -*-
"""
Simple bootstrap routine to compare multiple scenarios

Notes: 
    
Discrepency in performance between IronPython.Net and CPython was down
to calculation of the mean of n bootstraps.  

Explanation: 
data = [1, 2, 3, 4, 5, 6, 7, 9]
statistics.mean(data) = 86ms 
np.mean(mean) = 44.8 ms
np.array(data).mean = 5.74 ms
math.fsum(data)/len(data) = 1.86 ms
sum(data)/len(data) = 1.24 ms

fsum(data) potentially has great precision in floating point arithm than sum(data)

Possibly more performance on offer if data is already in a numpy array.

"""


import Bootstrap as bs
import BootIO as io
import MCC as mcc
import ConvFuncs as cf

CONFIDENCE = 95
N_BOOTS = 1000
INPUT_DATA = "data/mini_scenarios.csv"

#note BootStrap routines require lists of lists
scenario_data = cf.list_of_lists(io.load_scenarios(INPUT_DATA))
N_SCENARIOS = len(scenario_data)
print("Loaded data. {0} scenarios".format(N_SCENARIOS))

args =  bs.BootstrapArguments()
args.nboots = N_BOOTS
args.nscenarios = N_SCENARIOS
args.ncomparisons = mcc.pairwise_comparisons_count(N_SCENARIOS)
args.confidence = mcc.bonferroni_adjusted_confidence(CONFIDENCE, N_SCENARIOS)

#args.boot_function = bs.boot_dep_mean_diff   
args.boot_function = bs.boot_mean_diff   

#Basically we just write a new function for what ever type of comparison
#we want to do.  Then assign it to args.comp_function
#This could be modified to complete multiple actions i.e. percentile intervals and probabilities
#Functions are:
#Bootstrap.percentile_confidence_interval(data, args) 
#Bootstrap.proportion_x2_greaterthan_x1(data, args) 
#Bootstrap.plot_boostrap_samples_pdf(data, args)
#Bootstrap.plot_boostrap_samples_cdf(data, args)
    
#args.comp_function = bs.percentile_confidence_interval
args.comp_function = bs.proportion_x2_greaterthan_x1
#args.comp_function = bs.plot_boostrap_samples_cdf # use this to product charts instead

args.comp_functions = [bs.proportion_x2_greaterthan_x1, bs.percentile_confidence_interval]

#args.comp_function = bs.proportion_x2_greaterthan_x1
#args.comp_function = bs.plot_boostrap_samples_cdf # use this to product charts instead

args.boot_function = bs.boot_mean_diff3
r = bs.resample_all_scenarios(scenario_data, args)


print("Running comparisons...")
#results = bs.compare_scenarios_pairwise(scenario_data, args)
results = bs.compare_scenarios_pairwise(r, args) # revised script

    
#io.print_long_format_comparison_results(results)
#io.write_long_format_comparison_results(results)

#print(results)

matrix = io.results_to_matrix(results) 
#print(matrix)
io.print_results_matrix(matrix, N_SCENARIOS) #To DO. only works if proportion comparison performed!

io.insert_inverse_results(matrix, N_SCENARIOS)
#io.print_results_matrix(matrix, N_SCENARIOS) #To DO. only works if proportion comparison performed!

#io.write_results_matrix(matrix, N_SCENARIOS) 
print("Results written to file.")





print("Bootstrap analysis complete.")

