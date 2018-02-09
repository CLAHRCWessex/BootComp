# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 08:15:16 2017

@author: tm3y13
"""

import matplotlib.pyplot as plt
import seaborn as sns

DECIMAL_PLACES = 2


def plot_boostrap_samples_cdf(data, args):
    # the histogram of the data
    
    fig, axs = plt.subplots(1, 1, sharey=False, tight_layout=True)
    
    n, bins, patches = axs.hist(data, 50, cumulative = True, normed=1, 
                                linewidth=1.5, histtype='step', 
                                facecolor='green', alpha=0.75)
    
    plt.xlabel('Mean difference')
    plt.ylabel('Cumulative Probability')
    
    plt.axis([min(data) - 1, max(data), 0, 1])
    plt.grid(True)
    
    plt.show()
    
    return fig
    
    
    
def plot_boostrap_samples_pdf(data, args):
    
    fig, axs = plt.subplots(1, 1, sharey=False, tight_layout=True)
    
    # the histogram of the data
    n, bins, patches = axs.hist(data, 50, normed=1, 
                                facecolor='green', alpha=0.75)
    
    plt.xlabel('Mean difference')
    plt.ylabel('Probability')
    
    plt.axis([min(data) - 1, max(data) + 1, 0, 0.3])
    plt.grid(True)
    
    plt.show()
    
    return fig
    
    
