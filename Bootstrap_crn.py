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
        
        


    
    