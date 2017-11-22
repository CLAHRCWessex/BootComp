# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:51:07 2017

@author: tm3y13
"""

import csv




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


def write_results_matrix(matrix, n_scenarios):
    """
    Converts scenario comparison results to matrix format.
    Includes "-" for comparisons that are N/A
    """
     
    headers = scenario_headers(n_scenarios)
    row_headers = scenario_row_headers(n_scenarios)
     
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

    matrix = [['-' for i in range(len(results))] for j in results]
   
        
    #loop through results and add to matrix
    for i in range(len(results)):
        k = 0
        for j in range(len(results[i])):
            matrix[i][i+j] = results[i][k]
            k+= 1
    
    return matrix


def print_results_matrix(matrix, n_scenarios, decimal_places = 2):
    """
    Screen print of comparison results in matrix form.  Not nice
    for large comparisons. 
    """
    
    headers = scenario_headers(n_scenarios)
    row_headers = scenario_row_headers(n_scenarios)
    
    #r_matrix = [round(x, decimal_places) for row in matrix]
    
    for row in matrix:
        for i in row:
            if i != "-":
                i = round(i, decimal_places)
                
    
    row_format ="{:>10}" * (len(headers)+1)
    print(row_format.format("", *headers))
    for scenario, row in zip(row_headers, matrix):
        print(row_format.format(scenario, *row ))
        
      
        
                
            
def scenario_headers(n_scenarios):
    """
    Returns a list representing headers in a results matrix
    """
    return ["S{0}".format(i) for i in range(2, n_scenarios+1)]
    


def scenario_row_headers(n_scenarios):
    """
    Returns a list representing headers in a results matrix
    """
    return ["S{0}".format(i) for i in range(1, n_scenarios)]



    

    