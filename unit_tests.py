#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for the BootComp package.  
All testing is done by pytest

Testing of bootstap function is controlled by 
setting a random seed for numpy.

This is complicated by the use of numba.  To ensure
the random number streams used are the same the functions
with the numba jit decorator are 'unwrapped' by a call to 
func.__wrapped__
 
"""
import numpy as np
import pandas as pd
import bootcomp.bootstrap as bs
import pytest


def test_single_bootstrap_result():
    '''
    Tests if the bootstrap routine
    returns the correct mean for a single bootstrap
    '''
    np.random.seed(seed=999)
    data = np.arange(1, 10)
    
    #original function is decorated by numba
    #unwrap the function so that random seed can be set
    orig_bs = bs.bootstrap.__wrapped__
    
    indexes = np.random.randint(0, data.shape[0], data.shape[0])
    expected = np.array(data[indexes].mean())
    print(data[indexes])
    
    #reset seed
    np.random.seed(seed=999)
    actual = orig_bs(data, boots=1)
    print(actual, expected)
    assert expected == actual
    
def test_2_bootstrap_results():
    '''
    Tests if the bootstrap routine
    returns the correct mean for a single bootstrap
    '''
    np.random.seed(seed=999)
    data = np.arange(1, 10)
    expected = np.zeros(2)
    
    #original function is decorated by numba
    #unwrap the function so that random seed can be set
    orig_bs = bs.bootstrap.__wrapped__
    
    #first pass
    indexes = np.random.randint(0, data.shape[0], data.shape[0])
    expected[0] = np.array(data[indexes].mean())
    
    #second pass
    indexes = np.random.randint(0, data.shape[0], data.shape[0])
    expected[1] = np.array(data[indexes].mean())
    
    #reset seed
    np.random.seed(seed=999)
    actual = orig_bs(data, boots=2)
    print(actual, expected)
    assert np.array_equal(expected, actual)
    

def test_single_bootstrap_size():
    data = np.arange(1, 10)
    
    expected = (1, )
    actual = bs.bootstrap(data, boots=1)
    
    assert expected == actual.shape
    
def test_single_bootstrap_size_10():
    data = np.arange(1, 10)
    boots = 10
    expected = (boots, )
    actual = bs.bootstrap(data, boots=boots)
    
    assert expected == actual.shape
    
def test_single_bootstrap_type():
    data = np.arange(1, 10)
    actual = bs.bootstrap(data, boots=1)
    assert type(actual) == np.ndarray
    
def test_single_bootstrap_type_10():
    data = np.arange(1, 10)
    boots = 10
    actual = bs.bootstrap(data, boots=boots)
    assert type(actual) == np.ndarray
    
    
def test_multi_bootstrap_result():
    '''
    Tests if the bootstrap routine
    returns the correct mean for a single bootstrap
    there are 2 competing designs
    '''
    np.random.seed(seed=999)
    data = np.arange(1, 21)
    data = np.reshape(data, (2, 10))
    boots = 1
    designs = 2
    expected = np.zeros((designs, boots))
    
    #original function is decorated by numba
    #unwrap the function so that random seed can be set
    numb_bs = bs.bootstrap
    # monkey patch module to get rid of numba
    bs.bootstrap = bs.bootstrap.__wrapped__  
    
    orig_multi = bs.multi_bootstrap.__wrapped__
    
    indexes = np.random.randint(0, data.shape[1], data.shape[1])
    expected[0, 0] = np.array(data[0, indexes].mean())
    
    indexes = np.random.randint(0, data.shape[1], data.shape[1])
    expected[1, 0] = np.array(data[1, indexes].mean())
    
    #reset seed
    np.random.seed(seed=999)
    actual = orig_multi(data, boots=boots)    
    #re-apply numba function 
    bs.bootstrap = numb_bs
    assert np.array_equal(expected, actual)
    

def test_multi_bootstrap_size_5_10():
    data = np.arange(1, 51)
    data = np.reshape(data, (5, 10))
    boots = 10
    designs = 5
    expected = np.zeros((designs, boots))
    actual = bs.multi_bootstrap(data, boots=boots)
    
    assert expected.shape == actual.shape
    
    
def test_indifferece_1():
    x_test = 10
    indiff_test = 10.1
    expected = 1
    actual = bs.indifferent(x_test, indiff_test)
    assert expected == actual    
    

def test_indifferece_0():
    x_test = 10
    indiff_test = 9.9
    expected = 0
    actual = bs.indifferent(x_test, indiff_test)
    assert expected == actual   

    
def test_within_x():
    '''This was complicated to test!
    Probably means I should refactor the function
    
    Test
    5 designs
    5 replications
    
    10 bootstraps
    
    original data
    5 x 5 matrix.
    Columns {0:1, 1:2, 2:3, 3:4, 4:5}
    
    Therefore differences are:
    diffs = [0, 1, 2, 3, 4] 
    
    bootstrap datasets are just repeats of these values
    
    x = 2 i.e. happy with values up to twice the the best
    y = 0.99 (this will work as all values are the same in boots)
        
    '''
    
    designs = 5
    boots = 20
    reps = 5
    
    expected = [0, 1, 2]
    
    #synthetic replication data
    data = np.zeros((designs, reps))
    for i in range(0, data.shape[0]):
        data[i, :] = i+1
    
    #smallest values in index 0
    best_index = 0
    
    #boot differences (always the same value)
    df_boots = np.zeros((designs, boots))
    
    for i in range(df_boots.shape[0]):
        df_boots[i, :] = i
        
    df_boots = pd.DataFrame(df_boots).T
    print(df_boots)
                       
    x = 2 # effectively 
    y = 0.95
    
    data = pd.DataFrame(data).T
    print(data)
    
    actual = bs.within_x(df_boots, x, y, data, best_index, boots)
    print('type {}'.format(type(actual)))
    print(expected, actual.tolist())
    assert expected == actual.tolist()
    
    
def test_within_x_1():
    '''This was complicated to test!
    Probably means I should refactor the function
    
    Test
    5 designs
    5 replications
    
    10 bootstraps
    
    original data
    5 x 5 matrix.
    Columns {0:1, 1:2, 2:3, 3:4, 4:5}
    
    Therefore differences are:
    diffs = [0, 1, 2, 3, 4] 
    
    bootstrap datasets are just repeats of these values
    
    x = 2 i.e. happy with values up to twice the the best
    y = 0.99 (this will work as all values are the same in boots)
        
    '''
    
    designs = 5
    boots = 10
    reps = 5
    
    expected = [0, 1]
    
    #synthetic replication data
    data = np.zeros((designs, reps))
    for i in range(0, data.shape[0]):
        data[i, :] = i+1
    
    #smallest values in index 0
    best_index = 0
    
    #boot differences (always the same value)
    df_boots = np.zeros((designs, boots))
    
    for i in range(df_boots.shape[0]):
        df_boots[i, :] = i
        
    df_boots = pd.DataFrame(df_boots).T
    print(df_boots)
                       
    x = 1 # effectively 
    y = 0.95
    
    data = pd.DataFrame(data).T
    print(data)
    
    actual = bs.within_x(df_boots, x, y, data, best_index, boots)
    print('type {}'.format(type(actual)))
    print(expected, actual.tolist())
    assert expected == actual.tolist()
    
    

def test_indifference_array():
    '''This was complicated to test!
        
    Test
    5 designs
    5 replications
    
    15 bootstraps
    
    original data
    5 x 5 matrix.
    Columns {0:1, 1:2, 2:3, 3:4, 4:5}
    
    Therefore differences are:
    diffs = [0, 1, 2, 3, 4] 
    
    bootstrap datasets are just repeats of these values
    
    x = 1 i.e. happy with values up to 1 more the the best
        
    '''
    
    designs = 5
    boots = 15
    reps = 5
        
    #synthetic replication data
    data = np.zeros((designs, reps))
    for i in range(0, data.shape[0]):
        data[i, :] = i+1
    
    #smallest values in index 0
    best_index = 0
    
    #boot differences (always the same value)
    df_boots = np.zeros((designs, boots))
    
    for i in range(df_boots.shape[0]):
        df_boots[i, :] = i
        
    df_boots = pd.DataFrame(df_boots).T
    print(df_boots)
                       
    x = 1 # effectively 

    data = pd.DataFrame(data).T
    
    expected = np.zeros((designs, boots), np.int64)
    
    for i in range(0, 2):
        expected[i, :] = 1
    
    actual = bs.indifference_array(x, data, best_index, df_boots)
    #actual is an pandas dataframe
    assert actual.equals(pd.DataFrame(expected.T))    

       
