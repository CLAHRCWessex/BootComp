import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_systems(file_name, exclude_reps=0, delim=','):
    """
    Reads scenario data from a .csv file (assumes comma delimited).
    Assumes that each column represents a scenario.
    Returns a numpy array.  Each row is a scenario, each col a replication.
    Assumes all scenarios have the same number of replications.

    @file_name = name of file containing csv data
    @delim = delimiter of file.  Default = ',' for CSV.

    Notes: should this be in this module?

    """

    return np.genfromtxt(file_name, delimiter=delim,
                         skip_footer=exclude_reps)

def load_model_file(filepath):
    return [filepath + "/" + f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]

def get_best_subset(dfs, labels, subset):
    """
    Returns the best subset and best systems
    from a collection of performance measures across multiple

    Keyword arguments:
    dfs -- list of numpy.ndarrys
    labels -- labels/names of numpy.ndarrys in @dfs
    subset -- list of indexes to return 
    
    """
    df_list = []
    
    for i in range(len(dfs)):      
        df_sub = dfs[i][subset].mean()
        df_sub.rename(labels[i], inplace=True)
        df_list.append(df_sub)
        
    subset_kpi = pd.concat(df_list, axis=1)  
    
    best_system_index = subset_kpi.sort_values(by=labels).index[0]
    
    return best_system_index, subset_kpi


def best_subset_table(df_kpi, indexes, doe_file_name):
    """
    """
    df_doe = pd.read_csv(doe_file_name, index_col='System')
    df_doe.index -= 1
    df_kpi =  df_kpi[df_kpi.index.isin(indexes)]
    temp = df_doe[df_doe.index.isin(indexes)]
    df_subset_table = pd.concat([temp, df_kpi], axis=1)
    return df_subset_table.sort_values(by=['wait', 'util', 'tran'])



def simulate_stage_2(take_forward, model_file):
   files = sorted(model_file, reverse=True) 
   df_wait_s2 = pd.DataFrame(load_systems(files[0]))[take_forward]
   df_util_s2 = pd.DataFrame(load_systems(files[1]))[take_forward]
   df_tran_s2 = pd.DataFrame(load_systems(files[2]))[take_forward]
      
   print("Loaded waiting time data. {0} systems; {1} replications".format(df_wait_s2.shape[1], df_wait_s2.shape[0]))
   print("Loaded utilzation data. {0} systems; {1} replications".format(df_util_s2.shape[1], df_util_s2.shape[0]))
   print("Loaded transfers data. {0} systems; {1} replications".format(df_tran_s2.shape[1], df_tran_s2.shape[0]))
   
   return df_wait_s2,df_util_s2, df_tran_s2


def simulate_stage_1(n_1, model):
    
   files = sorted(model, reverse=True)
   system_data_wait = load_systems(files[0], exclude_reps = 50-n_1)
   system_data_util = load_systems(files[1], exclude_reps = 50-n_1)
   system_data_tran = load_systems(files[2], exclude_reps = 50-n_1)
   
   print("Loaded waiting time data. {0} systems; {1} replications".format(system_data_wait.shape[1], system_data_wait.shape[0]))
   print("Loaded utilzation data. {0} systems; {1} replications".format(system_data_util.shape[1], system_data_util.shape[0]))
   print("Loaded transfers data. {0} systems; {1} replications".format(system_data_tran.shape[1], system_data_tran.shape[0]))
   
   df_tran = pd.DataFrame(system_data_tran)
   df_util = pd.DataFrame(system_data_util)
   df_wait = pd.DataFrame(system_data_wait)
   
   return df_wait, df_util, df_tran

def ward_model_charts(doe_file_path, df_wait, df_util, df_tran):
    df_doe = pd.read_csv(doe_file_path, index_col='System')
    df_doe.index -= 1
    
    temp = df_doe.loc[df_doe['Number of Bays']==0]
    #temp.index += 1
    subset_waits = df_wait[temp.index].mean()
    subset_waits.rename('wait', inplace=True)
    subset_utils = df_util[temp.index].mean()
    subset_utils.rename('util', inplace=True)
    subset_trans = df_tran[temp.index].mean()
    subset_trans.rename('tran', inplace=True)
    
    
    subset_utils_sem = df_util[temp.index].sem()
    subset_utils_sem.rename('util_sem', inplace=True)
    
    subset_utils_count = df_util[temp.index].count()
    subset_utils_count.rename('n_util', inplace=True)

    subset_kpi = pd.concat([temp, subset_waits, subset_utils, subset_trans, subset_utils_sem, subset_utils_count], axis = 1)
    subset_kpi['Waiting Time (hrs)'] = round(subset_kpi['wait']*24, 2)
    
    confidence = 0.95
    
    subset_kpi['hw_95'] = subset_kpi['util_sem'] * sp.stats.t.ppf((1+confidence)/2., subset_kpi['n_util']-1)
    
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    fig, axes = plt.subplots(nrows=1, ncols=2, sharey=False)
    
    subset_kpi.sort_values('util').plot(y = 'util', x= 'Number of Singles', figsize=(20, 8), fontsize = 18, 
                                        linewidth=3, legend =False, kind='scatter', ax=axes[1], xticks=[x for x in range(43, 56, 1)], xlim=(42, 56), yerr='hw_95')#, xlim=(70, 92), ylim=(0, 35))
    axes[0].set_ylabel('Mean Waiting Time (hrs)', fontsize = 18)
    axes[1].set_xlabel('Number of Singles (beds)', fontsize = 18)
    
    
    
    
    subset_kpi.plot('Number of Singles', 'Waiting Time (hrs)', figsize=(20, 8), fontsize = 18, 
                                        linewidth=3, legend =False, kind='line', ms=10, style='o-', ax=axes[0], xlim=(42, 56),
                                        xticks=[x for x in range(43, 56, 1)])
    axes[0].set_xlabel('Number of Singles (beds)', fontsize = 18)
    axes[1].set_ylabel('Mean Utilization (% beds)', fontsize = 18)
    axes[0].grid(True)
    axes[1].grid(True)
    axes[1].legend(['mean (n=5)','95% Confidence Interval'],fontsize=18)
    #plt.tight_layout()
    
    return fig

