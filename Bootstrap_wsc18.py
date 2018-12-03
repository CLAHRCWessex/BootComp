# -*- coding: utf-8 -*-
"""
Extra procedures for bootstrap multiple comparison routine
taking account of dependency across scenarios.
Used within SW18 and WCS18 conference papers.

"""

import numpy as np
import pandas as pd
from numba import jit, prange

import ConvFuncs as cf
import Bootstrap as bs

def load_systems(file_name, exclude_reps = 0, delim=','):
    """
    Reads scenario data from a .csv file (assumes comma delimited).  
    Assumes that each column represents a scenario.
    Returns a numpy array.  Each row is a scenario, each col a replication.
    Assumes all scenarios have the same number of replications. 
    
    @file_name = name of file containing csv data
    @delim = delimiter of file.  Default = ',' for CSV.  

    """
    
    return np.genfromtxt(file_name, delimiter=delim, skip_footer = exclude_reps)
    

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




def bootstrap_np(data, boots=1000):
    """
    Alternative bootstrap routine that works exclusively with a numpy 
    array.  Seems to offer limited performance improvement!?
    What am I doing in the standard Python code that makes it so efficient?
    Expense operations here are: round, random.uniform - but only to a limited
    extent!
    
    REturns a numpy array containing the bootstrap resamples
    @data = numpy array of systems to boostrap
    @boots = number of bootstrap (default = 1000)
    """
    to_return = np.empty([boots, data.shape[0]])
    
    sys_index =0
    total=0
        
    for system in data:
        
        for b in range(boots):
        
            for i in range(system.shape[0]):
                
                total += system[np.random.randint(0, system.shape[0])]

            to_return[b, sys_index] = total / system.shape[0]
            total= 0
        sys_index += 1
            
    return to_return
            
            
    
    
        

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
    
    

def constraints_bootstrap_plain_vanilla(data, threshold, boot_args, gamma=0.95, kind='lower'):
    """
    Bootstrap a chance constraint for k systems and filter out systems 
    where p% of resamples are greater a threshold t.  
    
    Example 1. A lower limit.  If the chance constaint was related to utilization it could be stated as 
    filter out any systems where 95% of the distribution is greater than 80%.
    
    Example 2. An upper limit.  If the chance constraint related to unwanted ward transfers it could be stated 
    as filter out any systems where 95% of the distribution is less than 50 transfers per annum.
    
    Returns a pandas.Series containing of the feasible systems i.e. that do not violate the chance constraint.
    
    @data - a numpy array of the data to bootstrap
    @threshold - the threshold of the chance constraint
    @boot_args - the bootstrap setup class
    @p - the probability cut of for the chance constraint  (default p = 0.95)
    @kind - 'lower' = a lower limit threshold; 'upper' = an upper limit threshold (default = 'lower')
    
    """
    
    valid_operations = ['upper', 'lower']
    
    if kind.lower() not in valid_operations:
        raise ValueError('Parameter @kind must be either set to lower or upper')
    
    resample_list = bs.resample_all_scenarios(data.tolist(), boot_args)
    df_boots = cf.resamples_to_df(resample_list, boot_args.nboots)
    
    if('lower' == kind.lower()):
        
        df_counts = pd.DataFrame(df_boots[df_boots >= threshold].count(), columns = {'count'})
    else:
        df_counts = pd.DataFrame(df_boots[df_boots <= threshold].count(), columns = {'count'})
        
    df_counts['prop'] = df_counts['count'] / boot_args.nboots
    df_counts['pass'] = np.where(df_counts['prop'] >= gamma, 1, 0)
    df_counts.index -= 1
    
    return df_counts.loc[df_counts['pass'] == 1].index
 
   
   
   
def constraints_bootstrap(data, threshold, nboots=1000, gamma=0.95, kind='lower'):
    """
    Bootstrap a chance constraint for k systems and filter out systems 
    where p% of resamples are greater a threshold t.  
    
    Example 1. A lower limit.  If the chance constaint was related to utilization it could be stated as 
    filter out any systems where 95% of the distribution is greater than 80%.
    
    Example 2. An upper limit.  If the chance constraint related to unwanted ward transfers it could be stated 
    as filter out any systems where 95% of the distribution is less than 50 transfers per annum.
    
    Returns a pandas.Series containing of the feasible systems i.e. that do not violate the chance constraint.
    
    Keyword arguments
    data -- a numpy array of the data to bootstrap
    threshold -- the threshold of the chance constraint
    boot_args -- the bootstrap setup class
    gamma -- the probability cut of for the chance constraint  (default p = 0.95)
    kind -- 'lower' = a lower limit threshold; 'upper' = an upper limit threshold (default = 'lower')
    
    """
    
    valid_operations = ['upper', 'lower']
    
    if kind.lower() not in valid_operations:
        raise ValueError('Parameter @kind must be either set to lower or upper')
    
    df_boots = pd.DataFrame(multi_bootstrap_par(data, nboots).T)
    
    if('lower' == kind.lower()):
       
        df_counts = pd.DataFrame(df_boots[df_boots >= threshold].count(), columns = {'count'})
    else:
        df_counts = pd.DataFrame(df_boots[df_boots <= threshold].count(), columns = {'count'})
      
    df_counts['prop'] = df_counts['count'] / nboots
    df_counts['pass'] = np.where(df_counts['prop'] >= gamma, 1, 0)
    
    return df_counts.loc[df_counts['pass'] == 1].index


@jit(nopython=False)
def multi_bootstrap_par(data, boots):
    """
    Keyword arguments:
    data -- numpy multi-dimentional array 
    boot -- number of bootstraps  
    
    """
    designs = data.shape[0]
    
    to_return = np.empty((designs, boots))
    
    for design in range(designs):
        
        to_return[design:design+1] = bootstrap(data[design], boots)
        
    return to_return


@jit(nopython=True, parallel=True)
def bootstrap_par(data, boots):
    """
    Create bootstrap datasets that represent the distribution of the mean.
    Returns a numpy array containing the bootstrap datasets 
    
    Keyword arguments:
    data -- numpy array of systems to boostrap
    boots -- number of bootstrap (default = 1000)
    """
    
    bs_data = np.empty(boots)
    
    for b in prange(boots):
        
        total=0
        
        for s in range(data.shape[0]):
        
            total += data[np.random.randint(0, data.shape[0])]

        bs_data[b] = total / data.shape[0]

    return bs_data


@jit(nopython=True)
def bootstrap(data, boots):
    """
    Create bootstrap datasets that represent the distribution of the mean.
    Returns a numpy array containing the bootstrap datasets 
    
    Keyword arguments:
    data -- numpy array of systems to boostrap
    boots -- number of bootstrap (default = 1000)
    """
    
    bs_data = np.empty(boots)
    
    for b in range(boots):
        
        total=0
        
        for s in range(data.shape[0]):
        
            total += data[np.random.randint(0, data.shape[0])]

        bs_data[b] = total / data.shape[0]

    return bs_data



def indifferent(x, indifference):
    """
    convert numbers to 0 or 1
     1 = difference less than 0.244
    0 = difference greater than 0.244
    """
    if x <= indifference:
        return 1
    else:
        return 0

def quality_bootstrap(feasible_systems, headers, best_system_index, x=0.1, y = 0.95, nboots = 1000):
    """
    1. Create differences of systems from best system
    2. Create nboots bootstrap datasets of the differences
    3. Return a DataFrame with all systems that are x% of feasible_systems[best_system_index] in y% of the boostrap samples
    
    Keyword arguments:
    feasible_systems -- systems that meet chance constraints (if there are any)
    headers -- list of system indexes that are feasible
    best_system_index -- index of the best system within @feasible_systems
    args - Instance of a BootstrapArguments class
    x -- % tolerance of difference from best mean allowed (default = 0.1)
    y -- % of boostrap samples that must be within tolerance x of best mean (default = 0.95)
    nboots = number of bootstrap datasets to create (default = 1000)
    
    """
    
    #setup differences
    diffs =  pd.DataFrame(feasible_systems.values.T - np.array(feasible_systems[best_system_index])).T
    diffs.columns = headers
    
    #create bootstrap datasets
    #resample_diffs = bs.resample_all_scenarios(diffs.values.T.tolist(), args)
    #df = cf.resamples_to_df(resample_diffs, nboots)
    df = pd.DataFrame(multi_bootstrap_par(diffs.values.T, nboots).T)
    df.columns = headers    
    
    #find systems that have y% of bootstrap samples within x% of the best mean
    return within_x(df, x, y, feasible_systems, best_system_index, nboots)
    
    

def within_x(diffs, x, y, systems, best_system_index, nboots):
    """
    Return x% of feasible_systems[best_system_index] in y% of the boostrap samples
    """
    indifference = systems[best_system_index].mean() * x
    df_indifference = diffs.applymap(lambda x: indifferent(x, indifference))   
    threshold = nboots * y
    df_within_limit = df_indifference.sum(0)
    df_within_limit= pd.DataFrame(df_within_limit, columns=['sum'])
    return df_within_limit.loc[df_within_limit['sum'] >= threshold].index
    


        


    
    