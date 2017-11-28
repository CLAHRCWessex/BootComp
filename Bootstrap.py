# -*- coding: utf-8 -*-
"""
Multiple comparison bootstrap routines for simulation output analysis.
 
Implemented as a set of simple list comprehensions.

@author: T.Monks
    
"""


import numpy as np
import matplotlib as mlab
import matplotlib.pyplot as plt

import BasicStatistics as bs




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



class reporter(object):
    """
    
    Decorator for reporting the progress of a 
    bootstrap process
    
    """
    def __init__(self, func):
        self.func = func
		
    def __call__(self, *args):
        self.report(args[2])
        return self.func(*args)
	
    def report(self, args):
        args.lw_complete += 1.0
        #args.worker.ReportProgress((args.lw_complete / args.ncomparisons) * 100.0)

		
DECIMAL_PLACES = 2


#

def compare_scenarios_pairwise(scenarios, args):
    """
    Compare all scenarios against each other
    @scenarios: the list containing scenario data
    @args: bootstrap arguemnts (utility class)
    
    @args.nboots: number of bootstraps
    @args.confidence: alpha confidence level
    @args.bootfunction:  the bootstrap function selected (dependent or independent)
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
    @args.bootfunction:  the bootstrap function selected (dependent or independent)
    @args.nscenarios: number of scenarios
    @args.ncomparisons: number of comparisons (depending on pariwise or listwise)
    @args.comp_function: the method of comparison e.g. percentile or probability x > y
    """
    return [compare_two_scenarios(control, scenarios[i], args) for i in range(len(scenarios))]
    
   





@reporter
def compare_two_scenarios(first_scenario, second_scenario, args):
    """
    Compare two scenarios 

    @first_scenario - first scenario replication data;
    @second_scenario - second scenario replication data;
    """
    
    diffs = [args.boot_function(first_scenario, second_scenario) for i in range(args.nboots)] 
    return args.comp_function(diffs, args)


def compare_two_scenarios2(first_scenario, second_scenario, args):
    """
    Compare two scenarios using the list of comparison functions
    
    @first_scenario - first scenario replication data;
    @second_scenario - second scenario replication data;
    @args.comp_functions - a list of comparison functions to use. 
    """
    
    diffs = [args.boot_function(first_scenario, second_scenario) for i in range(args.nboots)] 
    return [func(diffs, args) for func in args.comp_functions]
    





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


def plot_boostrap_samples_cdf(data, args):
    # the histogram of the data
    n, bins, patches = plt.hist(data, 50, cumulative = True, normed=1, linewidth=1.5, histtype='step', facecolor='green', alpha=0.75)
    
    plt.xlabel('Mean difference')
    plt.ylabel('Cumulative Probability')
    
    plt.axis([min(data) - 1, max(data) + 1, 0, 1])
    plt.grid(True)
    
    plt.show()
    
def plot_boostrap_samples_pdf(data, args):
    # the histogram of the data
    n, bins, patches = plt.hist(data, 50, normed=1, facecolor='green', alpha=0.75)
    
    plt.xlabel('Mean difference')
    plt.ylabel('Cumulative Probability')
    
    plt.axis([min(data) - 1, max(data) + 1, 0, 1])
    plt.grid(True)
    
    plt.show()

def boot_mean_diff(data1, data2):
    """
    Computes the mean difference of bootstap samples
    Assumes independence of samples
    """
    return bootstrap_mean(data1) - bootstrap_mean(data2)



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
    
    @n : number of random intergers to generate
    
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
	

	
def boot_dep_x2_greater_than_x1(data1, data2):
    """
    Bootstraps dependent means and returns true/false
    if x2 is > x1
    """
    indexes = resample(len(data1))
    return bootstrap_mean2(data2, indexes) > bootstrap_mean2(data1, indexes)
	


def bootstrap_mean2(data, indexes):
    """
    Computes the mean of a bootstrap sample
    
    20170727 TM Notes: Not completely sure why I wrote two bootstrap_mean functions?
    This is the one that is used when assuming dependence.  bootstrap_mean used when assuming independence
    
    Refactor to single function?
    
    Uses numpy.mean over statistics.mean as appears to be more efficient.
    """
    
    return bs.mean(boot(data, indexes))
    

