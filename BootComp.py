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
import BootChartExtensions as ch
import MCC as mcc
import ConvFuncs as cf




CONFIDENCE = 95
N_BOOTS = 1000
INPUT_DATA = "data/real_scenarios.csv"

#note BootStrap routines require lists of lists
scenario_data = cf.list_of_lists(io.load_scenarios(INPUT_DATA))
N_SCENARIOS = len(scenario_data)
print("Loaded data. {0} scenarios".format(N_SCENARIOS))

args =  bs.BootstrapArguments()
args.nboots = N_BOOTS
args.nscenarios = N_SCENARIOS
args.ncomparisons = mcc.pairwise_comparisons_count(N_SCENARIOS)
args.confidence = mcc.bonferroni_adjusted_confidence(CONFIDENCE, N_SCENARIOS)



#Basically we just write a new function for what ever type of comparison
#we want to do.  Then assign it to args.comp_function
#This could be modified to complete multiple actions i.e. percentile intervals and probabilities
#Functions are:
#Bootstrap.percentile_confidence_interval(data, args)   = percentile confidence intervals
#Bootstrap.proportion_x2_greaterthan_x1(data, args)     = P(Sj > Si)
#Bootstrap.plot_boostrap_samples_pdf(data, args)        = Graphical comparison of difference PDF
#Bootstrap.plot_boostrap_samples_cdf(data, args)        = Graphical comparison of difference CDF
    
#args.comp_function = bs.percentile_confidence_interval
args.comp_function = bs.proportion_x2_greaterthan_x1
args.comp_function = bs.proportion_x2_lessthan_x1
#args.comp_function = ch.plot_boostrap_samples_cdf # use this to product charts instead
#args.comp_function = ch.plot_boostrap_samples_pdf


#args.comp_functions = [bs.proportion_x2_greaterthan_x1, bs.percentile_confidence_interval]  # to run multiple comparisons funcs in one go.

#what test statisic to calculate - here we used the mean.
args.point_estimate_func = bs.bootstrap_mean

#need to think about these names
args.test_statistic_function = bs.boot_mean_diff


print("Resampling..please wait")
boot_data = bs.resample_all_scenarios(scenario_data, args)
print("Resampling complete.")


print("Running comparisons...\n")
results = bs.compare_scenarios_pairwise(boot_data, args) 

df_boots = cf.resamples_to_df(boot_data, args.nboots)

ranks_1 = bs.rank_systems_min(df_boots, args)
print(ranks_1)

#mlargest = bs.rank_systems_mlargest(df_boots, args, 5)
#print(mlargest)

nsmallest = bs.rank_systems_msmallest(df_boots, args, 1)
print(nsmallest)
   
#io.print_long_format_comparison_results(results)
#io.write_long_format_comparison_results(results)

matrix = io.results_to_matrix(results) 

#io.print_results_matrix(matrix, N_SCENARIOS) #To DO. only works if proportion comparison performed!
io.insert_inverse_results(matrix, N_SCENARIOS)

#io.print_results_matrix(matrix, N_SCENARIOS) #To DO. only works if proportion comparison performed!

io.write_results_matrix(matrix, N_SCENARIOS)
print("\nResults written to file.")


print("Bootstrap analysis complete.")


