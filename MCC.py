# -*- coding: utf-8 -*-
"""
Multiple comparison control functions for simulation output analysis

@author: T.Monks
"""


def bonferroni_adjusted_confidence(confidence, nscenarios):
    """
    standard bonferroni output 
    @confidence: integer 0-100
    @totalscenarios: number of scenarios simulated
    """
    alpha = (100.0 - confidence)/100.0
    corrected_alpha = alpha/pairwise_comparisons_count(nscenarios)
    return 100.0 * (1 - corrected_alpha)



def pairwise_comparisons_count(nscenarios):
    """
    Calculate the total number of pairwise comparisons of n scenarios
    
    @nscenarios: the number of scenarios
    """
    return ((nscenarios*(nscenarios-1))/2)