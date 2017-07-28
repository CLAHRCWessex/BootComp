#
#  Copyright T.Monks 2010
"""
Module contains routines for calculations of basic statistics such as mean, std dev etc.
"""

import math 


def mean(data):
    """
    Computes the mean of a list of numbers
    @data - list of integers/floats etc.
    
    """
    #return math.fsum(i for i in data)/len(data)
    return sum(data)/len(data)
   


def std_dev(data, arith_mean):
    """
    Computes the standard deviation

    @data - list of integers/floats etc.
    @arith_mean - the arthimetic mean of the data
    """
    var = mean([square(x - arith_mean) for x in data])
    return math.sqrt(var)



def square(x):
    """
    Computes the square of x
    
    @x - value to square	
    """
    return x * x