# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:48:01 2017

@author: tm3y13
"""

import pandas as pd

def list_of_lists(list_of_tuples):
    return [list(x) for x in list_of_tuples]


def resamples_to_df(list_of_lists, nboots):
    """
    Converts a list_of_lists into a dataframe.  
    The list_of_lists represents a set of bootstrap resamples across
    k systems
    """
    df = pd.DataFrame(list_of_lists, columns = [str(i) for i in range(1, nboots+1)])
    df.index += 1
    return df.transpose()


def matrix_to_dataframe(matrix, headers):
    """
    Convert a matrix of multiple comparison results to a data frame
    
    @matrix - list of multiple comparisons in matrix form
    @header - the header/row header sring
    
    example of matrix
    
    [['-', 0.19, 1.00]
    [0.12, '-', 1.00]
    [0.88, 0.45, '-']]
    
    """
    
    df = pd.DataFrame(matrix, columns = headers)
    df['systems'] = pd.Series(headers, index=df.index)  
    df.set_index('systems', inplace=True)
    del df.index.name
    return df
   

def subset_of_list(data, indexes):
    """
    Returns a subset of the list @data that corresponds to 
    items stored in @indexes
    
    @data - a list e.g. a list of lists or list of ints
    @indexes - a list of indexes e.g. [0, 1, 2]
    
    Example:
        
        data = [5, 4, 3, 2, 1]
        indexes = [0, 1, 4]
        return = [5, 4, 1]
    """
    return [data[i] for i in indexes]