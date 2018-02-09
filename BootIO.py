# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:51:07 2017

@author: tm3y13
"""

import csv
import pandas as pd

from ConvFuncs import list_of_lists



def load_scenarios(file_name):
    """
    Reads scenario data from a .csv file (assumes comma delimited).  
    Assumes that each column represents a scenario.
    Returns a list of lists.  Each list is the replications from each
    scenario

    """
    
    with open(file_name, 'r') as csvfile:

        c_reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        columns = list(zip(*c_reader))
        return list_of_lists(columns)


def print_long_format_comparison_results(results):
    """
    Displays the comparison in a readable format
    @results.  List of lists containing comparison results
    """
    scenario = 1
    comp = 2
    
    for lists in results:
        print("Scenario {0}".format(scenario))
        comp = scenario + 1  
        scenario += 1
        
        for interval in lists:
            print("Vs. {0}: {1}".format(comp, interval))
            comp += 1
            
            
def write_long_format_comparison_results(results):
    """
    Outputs the comparison in a readable format to file
    @results.  List of lists containing comparison results
    """
    scenario = 1
    comp = 2
    
    with open("output.txt", "w") as outfile:
        
        for lists in results:
            outfile.write("Scenario {0}\n".format(scenario))
            comp = scenario + 1  
            scenario += 1
            
            for interval in lists:
                outfile.write("Vs. {0}: {1}\n".format(comp, interval))
                comp += 1            


#def write_results_matrix(matrix, n_scenarios):
    """
    Converts scenario comparison results to matrix format.
    Includes "-" for comparisons that are N/A
    """
     
#    headers = scenario_headers(n_scenarios)
#    row_headers = scenario_row_headers(n_scenarios)

#    output_list = []
    
#    headers.insert(0, '')
#    output_list.append(headers) 
#    for scenario, row in zip(row_headers, matrix):
#        output_list.append([scenario, *row])

           
#    with open('results_matrix.csv', 'w', newline='') as f:
#        writer = csv.writer(f)
#        writer.writerows(output_list)
        
        
        
def write_results_matrix(matrix, headers):
    """
    Converts scenario comparison results to matrix format.
    Includes "-" for comparisons that are N/A
    """
    
    row_headers = headers[:]
    
    output_list = []
    
    headers.insert(0, '')
    output_list.append(headers) 
    for scenario, row in zip(row_headers, matrix):
        output_list.append([scenario, *row])

           
    with open('results_matrix.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_list)
        
    
def results_to_matrix(results):
    """
    Converts scenario comparison results to matrix format.
    Includes "-" for comparisons that are N/A
    """

    matrix = [['-' for i in range(len(results)+1)] for j in results]
    matrix.append(['-' for i in range(len(results)+1)])
        
    #loop through results and add to matrix
    for i in range(len(results)):
        k = 0
        for j in range(len(results[i])):
            matrix[i][i+j+1] = results[i][k]
            k+= 1
            
    #add the inverse results to the matrix
    
    
    return matrix


def insert_inverse_results(matrix, n_scenarios):
    """
    By default a matrix of comparison results is only half
    filled along the diagonal.  This function fills in the 
    remaining diagnonal with the inverted results. 
    """
      
    for col in range(len(matrix[0])):
        for row in range(col+1, len(matrix[0])):
            if(matrix[col][row] != '-'):
                matrix[row][col] = round(1 - matrix[col][row], 2)
                
    

        
       
## only works for full results.  doesn't work subsets
            
def scenario_headers(n_scenarios):
    """
    Returns a list representing headers in a results matrix
    """
    return ["S{0}".format(i) for i in range(1, n_scenarios+1)]
    


def scenario_row_headers(n_scenarios):
    """
    Returns a list representing headers in a results matrix
    """
    return ["S{0}".format(i) for i in range(1, n_scenarios+1)]


    
def print_results_matrix(matrix, headers):
    """
    Screen print of comparison results in matrix form.  Not nice
    for large comparisons. 
    """
    
    row_headers = headers
                       
    row_format ="{:>8}" * (len(headers)+1)
    print(row_format.format("", *headers))
    for scenario, row in zip(row_headers, matrix):
        print(row_format.format(scenario, *row ))
        
        

                       

def colour_cells_by_proportion(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    
    lower=0.05
    upper=0.95
    colour = 'white'
    if type(val) is float:
        
        
        if val <= lower :
            colour = 'red' 
        elif val <= 1 and val >= upper:
            colour = 'green'
        elif val < upper and val > lower:
            colour = 'yellow'
    
    return 'background-color: %s' % colour

        

    