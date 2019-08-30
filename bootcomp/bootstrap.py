# -*- coding: utf-8 -*-
"""
Functions that form the two stage bootstrap
comparison procedure.

"""

import numpy as np
import pandas as pd
from numba import jit, prange

def bootstrap_np(data, boots=1000):
    """
    Alternative bootstrap routine that works exclusively with a numpy
    array.  Seems to offer limited performance improvement!?

    #This is slow because it isn't really proper NumPy - use of loops
    need to be cut out.

    Returns a numpy array containing the bootstrap resamples
    @data = numpy array of systems to boostrap
    @boots = number of bootstrap (default = 1000)
    """
    to_return = np.empty([boots, data.shape[0]])

    sys_index = 0
    total = 0

    for system in data:

        for boot in range(boots):

            for sample in range(system.shape[0]):

                total += system[np.random.randint(0, system.shape[0])]

            to_return[boot, sys_index] = total / system.shape[0]
            total = 0
        sys_index += 1

    return to_return



def constraints_bootstrap(data, threshold, nboots=1000,
                          gamma=0.95, kind='lower', cores='single'):
    """
    Bootstrap a chance constraint for k systems and filter out systems
    where p% of resamples are greater a threshold t.

    Example 1. A lower limit.  If the chance constaint was related to
    utilization it could be stated as filter out any systems where 95% of
    the distribution is greater than 80%.

    Example 2. An upper limit.  If the chance constraint related to unwanted
    ward transfers it could be stated as filter out any systems
    where 95% of the distribution is less than 50 transfers per annum.

    Returns a pandas.Series containing of the feasible systems
    i.e. that do not violate the chance constraint.

    Keyword arguments:
    data -- a numpy array of the data to bootstrap
    threshold -- the threshold of the chance constraint
    n_boots -- the number of bootstrap datasets to generate (default = 1000)
    gamma -- the probability cut off for the chance constraint (default p = 0.95)
    kind -- 'lower' = a lower limit threshold; 'upper' = an upper
             limit threshold (default = 'lower')
    cores - single ('single' or 's') core or parallel ('p' or 'parallel')
            execution. (default = 's')
    """
    #pylint: disable-msg=R0913

    valid_operations = ['upper', 'lower']
    valid_cores = ['single', 'parallel', 's', 'p']

    if kind.lower() not in valid_operations:
        raise ValueError('Parameter @kind must be either set to lower or upper')

    if cores.lower() not in valid_cores:
        msg = 'Parameter @cores must be either set to '
        msg += 'single (default) or parrallel (or p)'
        raise ValueError(msg)

    if cores in ('single', 's'):
        df_boots = pd.DataFrame(multi_bootstrap(data, nboots).T)
    else:
        df_boots = pd.DataFrame(multi_bootstrap_par(data, nboots).T)

    if kind.lower() == 'lower':
        df_counts = pd.DataFrame(df_boots[df_boots >= threshold].count(),
                                 columns={'count'})
    else:
        df_counts = pd.DataFrame(df_boots[df_boots <= threshold].count(),
                                 columns={'count'})

    df_counts['prop'] = df_counts['count'] / nboots
    df_counts['pass'] = np.where(df_counts['prop'] >= gamma, 1, 0)

    return df_counts.loc[df_counts['pass'] == 1].index


@jit(nopython=False)
def multi_bootstrap(data, boots):
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

        to_return[design:design+1] = bootstrap_par(data[design], boots)

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

    #pylint: disable-msg=E1133
    bs_data = np.empty(boots)

    for boot in prange(boots):

        total = 0

        for sample in range(data.shape[0]):

            total += data[np.random.randint(0, data.shape[0])]

        bs_data[boot] = total / data.shape[0]

    return bs_data


@jit(nopython=True)
def bootstrap(data, boots):
    """
    Create bootstrap datasets that represent the distribution of the mean.
    Returns a numpy array containing the bootstrap datasets

    Keyword arguments:
    data -- numpy array of systems to boostrap
    boots -- number of bootstrap (default = 1000)

    Developer notes:

    Could this be faster if was writtien in proper NumPy?
    i.e no loops - then maybe wouldn't need numba dependency?

    """

    bs_data = np.empty(boots)

    for boot in range(boots):

        total = 0

        for sample in range(data.shape[0]):

            total += data[np.random.randint(0, data.shape[0])]

        bs_data[boot] = total / data.shape[0]

    return bs_data



def indifferent(x, indifference):
    """
    convert numbers to 0 or 1
    1 = difference less than 0.244
    0 = difference greater than 0.244
    """
    if x <= indifference:
        return 1

    return 0


def quality_bootstrap(feasible_systems, headers, best_system_index,
                      x=0.1, beta=0.95, nboots=1000, cores='s'):
    """
    1. Create differences of systems from best system
    2. Create nboots bootstrap datasets of the differences
    3. Return a DataFrame with all systems that are x% of
       feasible_systems[best_system_index] in y% of the boostrap samples

    Keyword arguments:
    feasible_systems -- systems that meet chance constraints
                        (if there are any)

    headers -- list of system indexes that are feasible

    best_system_index -- index of the best system within @feasible_systems

    x -- % tolerance of difference from best mean allowed (default = 0.1)

    beta -- % of boostrap samples that must be within tolerance x of
        best mean (default = 0.95)

    nboots = number of bootstrap datasets to create (default = 1000)

    cores - single ('single' or 's') core or parallel ('p' or 'parallel')
            execution. (default = 's')
    """
    #pylint: disable-msg=R0913

    valid_cores = ['single', 'parallel', 's', 'p']
    msg = 'Parameter @cores must be either set to single or parrallel'

    if cores.lower() not in valid_cores:
        raise ValueError(msg)

    #setup differences
    diffs = pd.DataFrame(feasible_systems.values.T -
                         np.array(feasible_systems[best_system_index])).T
    diffs.columns = headers

    #create bootstrap datasets

    if cores in ('single', 's'):
        df = pd.DataFrame(multi_bootstrap(diffs.values.T, nboots).T)
    else:
        df = pd.DataFrame(multi_bootstrap_par(diffs.values.T, nboots).T)

    df.columns = headers

    #find systems that have beta% of bootstrap samples within x% of the best mean
    return within_x(df, x, beta, feasible_systems, best_system_index, nboots)


def within_x(diffs, x, y, systems, best_system_index, nboots):
    """
    Return x% of feasible_systems[best_system_index] in y% of the 
    boostrap samples
    
    Returns indexes of systems that meet quality criteria
    """
    #pylint: disable-msg=R0913

    df_indifference = indifference_dataframe(x, systems, 
                                             best_system_index, 
                                             diffs)
    
    df_within_limit = dataframe_to_sum_of_columns(df_indifference)
    
    indexes = indexes_meeting_quality_criteria(y, nboots, df_within_limit)
    
    return indexes


def indifference_dataframe(x, systems, best_system_index, diffs):
    '''Returns a pandas dataframe containing 1/0.  
    1 = value is within x% of the best system mean
    0 = value is not within x% of the best system mean
    
    Keyword arguments:
    diffs -- DataFrame of bootstrap datasets of mean differences
    '''
    indifference = systems[best_system_index].mean() * x
    df_indifference = diffs.applymap(lambda x: indifferent(x, indifference))
    return df_indifference


def dataframe_to_sum_of_columns(to_sum):
    '''
    Returns a dataframe that is the sum of the columns
    of the argument to_sum
    
    keyword arguments:
    to_sum -- pandas dataframe   
    '''
    arr = to_sum.sum(axis=0)
    df = pd.DataFrame(arr, columns=['sum'])
    return df
    

def indexes_meeting_quality_criteria(y, nboots, df_counts):
    '''
    Returns the indexes of the columns that meet the quality
    criteria
    '''
    threshold = nboots * y
    return df_counts.loc[df_counts['sum'] >= threshold].index
    




