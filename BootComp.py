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

fsum(data) potentially has great precision in floating point arithmetic than sum(data)

Possibly more performance on offer if data is already in a numpy array.

"""


import Bootstrap as bs
import BootIO as io
import BootChartExtensions as ch
import MCC as mcc
import ConvFuncs as cf


N_BOOTS = 2000
INPUT_DATA = "data/real_scenarios.csv"

scenario_data = io.load_scenarios(INPUT_DATA)
N_SCENARIOS = len(scenario_data)
print("Loaded data. {0} scenarios".format(N_SCENARIOS))

args =  bs.BootstrapArguments()
args.nboots = N_BOOTS
args.nscenarios = N_SCENARIOS
args.ncomparisons = mcc.pairwise_comparisons_count(N_SCENARIOS)

args.summary_func = bs.proportion_x2_greaterthan_x1
#args.summary_func = bs.proportion_x2_lessthan_x1


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

msmallest = bs.rank_systems_msmallest(df_boots, args, 5)
print(msmallest)
   

subset_indexes = msmallest.index.values.tolist()[:10]
subset = cf.subset_of_list(boot_data, subset_indexes)

args.nscenarios = len(subset)
results = bs.compare_scenarios_pairwise(subset, args) 

#io.print_long_format_comparison_results(results)
#io.write_long_format_comparison_results(results)

matrix = io.results_to_matrix(results) 
io.insert_inverse_results(matrix, args.nscenarios)
df = io.matrix_to_dataframe(matrix, [str(i) for i in subset_indexes])
print(df)


io.write_results_matrix(matrix, [str(i) for i in subset_indexes])

#io.write_results_matrix(matrix, N_SCENARIOS)
print("\nResults written to file.")


print("Bootstrap analysis complete.")


