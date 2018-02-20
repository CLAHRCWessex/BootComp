# -*- coding: utf-8 -*-
"""
An alternative implementation of the bootstrap multiple comparison routine
taking account of dependency across scenarios.

"""

import numpy as np


def load_scenarios(file_name, delim=','):
    """
    Reads scenario data from a .csv file (assumes comma delimited).  
    Assumes that each column represents a scenario.
    Returns a numpy array.  Each row is a scenario, each col a replication.
    Assumes all scenarios have the same number of replications. 
    
    @file_name = name of file containing csv data
    @delim = delimiter of file.  Default = ',' for CSV.  

    """
    
    return np.genfromtxt(file_name, delimiter=delim)
    

def resample_all_scenarios(data, boots=1000):
    """
    Create @args.nboots resamples of the test statistic from each 
    scenario e.g. the mean
    
    @data - a numpy array of scenarios/systems (each col = different scenario)
    @boots - bootstrap resamples with replacement to complete. Default = 1000.
    """
    
    resampled = np.empty([boots, data.shape[1]])
        
    for i in range(boots):
        resampled[i] = block_bootstrap(data).mean(axis=0)
        
    return resampled        

        

def block_bootstrap(data):
    """
    Block bootstrap to account for dependency across replications
    If Common Random Numbers have been used and have successfully
    produced a positive dependency then this approach should be used.
    """
    resampled = np.empty([data.shape[0], data.shape[1]])
    
    for i in range(data.shape[0]):
        resampled[i] = data[np.random.choice(data.shape[0])]
            
    return resampled
        

def variance_reduction_results(data):
    """
    Check if common random numbers have
    been successful in reducing the variance
    
    if successful the variance of the differences between
    two scenarios will be less than the sum.
    
    returns: numpy array of length len(data) - 1.  Each value 
    is either 0 (variance not reduced) or 1 (variance reduced)
    
    @data - the scenario data.
    
    """
    sums = sum_of_variances(data)
    diffs = variance_of_differences(data)
    
    less_than = lambda t: 1 if t <=0 else 1
    vfunc = np.vectorize(less_than)
    return vfunc(np.subtract(diffs, sums))
    
    
    

def sum_of_variances(data):
    var = data.var(axis=0)

    sums = np.empty([var.shape[0] -1, ])
    
    for i in range(len(var) - 1):
        sums[i] = var[i] + var[i+1]
        
    return sums


    
        

def variance_of_differences(data):
    """
    return the variance of the differences
    """
    return np.diff(data).var(axis=0)
    
    








        


    
    