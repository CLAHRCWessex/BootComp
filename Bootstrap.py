# -*- coding: utf-8 -*-
"""
Multiple comparison bootstrap routines for simulation output analysis.

Implemented as a set of simple list comprehensions.

@author: T.Monks
    
"""


import numpy as np
import pandas as pd

import BasicStatistics as bs
import ConvFuncs as cf



class BootstrapArguments:
    """
    
    Utility class - encapsulates any arguments needed for
    bootstrapping.
    
    Will nearly always contain the following properties/methods:
        nboots: number of bootstraps
        confidence: alpha confidence level
        bootfunction:  the bootstrap function selected (dependent or independent)
        comparisonfunction: the comparison function selelcted (e.g. percentile CIs)
        nscenarios: number of scenarios
        ncomparisons: number of comparisons (depending on pariwise or listwise)   
    """
    def __init__(self):
        pass



		
DECIMAL_PLACES = 2


def resample_all_scenarios(scenarios, args):
    """
    Create @args.nboots resamples of the test statistic from each 
    scenario e.g. the mean
    
    @scenarios - the list of scenarios
    @args - bootstrap arguments (utility class)
    """
    return [resample_scenario(sc, args) for sc in scenarios]


def resample_scenario(data, args):
    """
    Create @args.nboots resamples of a test statistic (e.g. mean) from the 
    replication data for a scenario
    
    @data - replications / batch means from a scenario
    @args - bootstrap arguments (utility class)
    @args.point_estimate_func - point estimate summary statistic to bootstrap e.g. mean or Var
    
    """
    return [args.point_estimate_func(data) for i in range(args.nboots)]
    
        

def compare_scenarios_pairwise(scenarios, args):
    """
    Compare all scenarios against each other
    @scenarios: the list containing scenario data
    @args: bootstrap arguments (utility class)
    
    @args.nboots: number of bootstraps
    @args.confidence: alpha confidence level
    @args.test_statistic_function: the test statistic to compare scenarios
    @args.nscenarios: number of scenarios
    @args.ncomparisons: number of comparisons (depending on pariwise or listwise)
    """
    args.lw_complete = 0
	
    
    return [compare_scenarios_listwise(scenarios[i], scenarios[i+1:], args)
               for i in range(len(scenarios) - 1)]
     

def compare_scenarios_listwise(control, scenarios, args):
    """
    Compare all scenarios to a base case/control
    
    @control: the main comparator (either 'base case' or 'the best')
    @scenarios: the list containing scenario data
    @args: bootstrap arguments (utility class)
    
    @args.nboots: number of bootstraps
    @args.confidence: alpha confidence level
    @args.difference_func: the function used for comparing the difference between scenarios.
    @args.nscenarios: number of scenarios
    @args.ncomparisons: number of comparisons (depending on pariwise or listwise)
    @args.summary_function: the method to summarise the comparison e.g. percentile or probability x > y
    """
    return [compare_two_scenarios(control, scenarios[i], args) for i in range(len(scenarios))]
    
   



#@reporter
#def compare_two_scenarios(first_scenario, second_scenario, args):
#    """
#    Compare two scenarios 

#    @first_scenario - first scenario replication data;
#    @second_scenario - second scenario replication data;
#    """
    
#    diffs = [args.boot_function(first_scenario, second_scenario) for i in range(args.nboots)] 
#    return args.comp_function(diffs, args)


#def compare_two_scenarios2(first_scenario, second_scenario, args):
#    """
#    Compare two scenarios using the list of comparison functions
    
#    @first_scenario - first scenario replication data;
#    @second_scenario - second scenario replication data;
#    @args.comp_functions - a list of comparison functions to use. 
#    """
    
#   diffs = [args.boot_function(first_scenario, second_scenario) for i in range(args.nboots)] 
#   return [func(diffs, args) for func in args.comp_functions]

def compare_two_scenarios(first_scenario, second_scenario, args):
    """
    Compare two scenarios 

    @first_scenario - first scenario replication data;
    @second_scenario - second scenario replication data;
    """
    
    diffs = args.difference_func(first_scenario, second_scenario) 
    return args.summary_func(diffs, args)



def percentile_confidence_interval(data, args):
    """
    100(1-alpha) confidence interval using percentile method
    
    @data: the bootstrapped mean differences
    @args: bootstrap arguments (utility class)
    @args.nboots: number of boots
    """
    alpha = 1 -(args.confidence/100.0)
    lower = int((alpha/2) * args.nboots)
    upper = int((1 - (alpha/2)) * args.nboots)

    data.sort()

    return [round(data[lower], DECIMAL_PLACES), round(data[upper], DECIMAL_PLACES)]
    

def proportion_x2_greaterthan_x1(data, args):
    """
    The number of bootstraps where the comparator was bigger than the control
    Really not sure what to call this procedure!  
    Rename to something more intuitive.
    
    @data: the bootstrapped mean differences
    @args: bootstrap arguments (utility class)
    
    """
    return round(sum(x < 0 for x in data)/args.nboots, DECIMAL_PLACES)


def proportion_x2_lessthan_x1(data, args):
    """
    The number of bootstraps where the comparator was bigger than the control
    Really not sure what to call this procedure!  
    Rename to something more intuitive.
    
    @data: the bootstrapped mean differences
    @args: bootstrap arguments (utility class)
    
    """
    return round(sum(x > 0 for x in data)/args.nboots, DECIMAL_PLACES)



def boot_mean_diff(data1, data2):
    """
    Computes the mean difference of bootstap samples
    Assumes independence of samples
    """
    return [a - b for a, b in zip(data1, data2)]


#def boot_mean_diff(data1, data2):
#    """
#    Computes the mean difference of bootstap samples
#    Assumes independence of samples
#    """
#    return bootstrap_mean(data1) - bootstrap_mean(data2)



def bootstrap_mean(data):
    """
    Computes the mean of a bootstrap sample
    """
    return bs.mean(boot(data, resample(len(data))))

 

def boot(data, sample):
    """
    returns a list of resampled values
    
    @data: the original scenario data
    @sample: a list of random numbers used to resample from @data
    
    """
    return [data[i] for i in sample]



def resample(n):
    """
    returns a list of size n containing resampled values (integers) between
    0 and n - 1
    
    @n : number of random integers to generate
    
    """
    x = [round(np.random.uniform(0, n-1)) for i in range(n)]
        
    return x
		
	
		

def boot_dep_mean_diff(data1, data2):
    """
    Bootstraps dependent mean difference
    Note: assumes that the lists have the same length
        
    """
    indexes = resample(len(data1))
        
    return bootstrap_mean2(data1, indexes) - bootstrap_mean2(data2, indexes)
	

	

	


def bootstrap_mean2(data, indexes):
    """
    Computes the mean of a bootstrap sample
    
    20170727 TM Notes: Not completely sure why I wrote two 
    bootstrap_mean functions?
    This is the one that is used when assuming dependence.  
    bootstrap_mean used when assuming independence
    
    Refactor to single function?
    
    Uses numpy.mean over statistics.mean as appears to be more efficient.
    """
    
    return bs.mean(boot(data, indexes))
    


def rank_systems_min(df_boots, args):
    """
    Returns a dataframe containing ranked systems.  
    Dataframe contains the frequency and proportion of bootstrap
    resamples where a systems was 'best'.  In this case the minimum value.
    special case of rank_systems_msmallest
    
    @df_boots - Pandas.DataFrame of bootstrap resamples. cols = systems
                rows = resamples
    @args - BootstrapArguments object
    @args.nboots- the number of bootstrap resamples per system
    """
    min_systems = df_boots.idxmin(axis=1)
    ranks = min_systems.value_counts().to_frame()   
    ranks['p_x'] = pd.Series(ranks[0]/args.nboots, index=ranks.index)
    ranks.columns = ['f_x', 'p_x']
    ranks.index.rename('system', inplace=True)
    return ranks


def rank_systems_max(df_boots, args):
    """
    Returns a dataframe containing ranked systems.  
    Dataframe contains the frequency and proportion of bootstrap
    resamples where a systems was 'best'.  In this case the maximum value.
    Special case of rank_systems_mlargest
    
    @df_boots - Pandas.DataFrame of bootstrap resamples. cols = systems
                rows = resamples
    @args - BootstrapArguments object
    @args.nboots- the number of bootstrap resamples per system
    """
    min_systems = df_boots.idxmax(axis=1)
    ranks = min_systems.value_counts().to_frame()   
    ranks['p_x'] = pd.Series(ranks[0]/args.nboots, index=ranks.index)
    ranks.columns = ['f_x', 'p_x']
    ranks.index.rename('system', inplace=True)
    return ranks    


def rank_systems_mlargest(df_boots, args, m):
    """
    Returns a the systems that occur most frequently in 
    the 'm' systems with the largest values for each resample.  
    
    @df_boots - Pandas.DataFrame of bootstrap resamples. cols = systems
                rows = resamples
    @args - arguments used in the resamples
    @m- number of best systems to consider
    """
    systems = np.argsort(-df_boots.values, axis=1)[:, :m].flatten()
    return rank_systems_m(systems, args)         


def rank_systems_msmallest(df_boots, args, m):
    """
    Returns a the systems that occur most frequently in 
    the 'm' systems with the smallest values for each resample.  
    
    @df_boots - Pandas.DataFrame of bootstrap resamples. cols = systems
                rows = resamples
    @args - arguments used in the resamples
    @m- number of best systems to consider
    """
    systems = np.argsort(df_boots.values, axis=1)[:, :m].flatten()
    return rank_systems_m(systems, args)

def rank_systems_m(systems, args):
    #returning indexes that are 1 too low.
    unique, counts = np.unique(systems, return_counts=True)
    #unique+1 adds 1 to indexes to line up with dataframes.
    np_a = np.asarray((unique+1, counts)).T
    df = pd.DataFrame(np_a, columns = ['system', 'f_x']) 
    df['p_x'] = pd.Series(df['f_x']/args.nboots, index=df.index)  
    df.set_index('system', inplace=True)
    return df.sort_values(['f_x'], ascending=[False], kind='quicksort')  



    


    