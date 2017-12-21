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
    return df.transpose()
   