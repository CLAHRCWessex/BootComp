import pandas as pd
from Bootstrap_wsc18 import load_systems
import os

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
   df_wait_s2 = pd.DataFrame(load_systems(model_file[0]))[take_forward]
   df_util_s2 = pd.DataFrame(load_systems(model_file[1]))[take_forward]
   df_tran_s2 = pd.DataFrame(load_systems(model_file[2]))[take_forward]
      
   print("Loaded waiting time data. {0} systems; {1} replications".format(df_wait_s2.shape[1], df_wait_s2.shape[0]))
   print("Loaded utilzation data. {0} systems; {1} replications".format(df_util_s2.shape[1], df_util_s2.shape[0]))
   print("Loaded transfers data. {0} systems; {1} replications".format(df_tran_s2.shape[1], df_tran_s2.shape[0]))
   
   return df_wait_s2,df_util_s2, df_tran_s2


def simulate_stage_1(n_1, model):
   system_data_wait = load_systems(model[0], exclude_reps = 50-n_1)
   system_data_util = load_systems(model[1], exclude_reps = 50-n_1)
   system_data_tran = load_systems(model[2], exclude_reps = 50-n_1)
   
   print("Loaded waiting time data. {0} systems; {1} replications".format(system_data_wait.shape[1], system_data_wait.shape[0]))
   print("Loaded utilzation data. {0} systems; {1} replications".format(system_data_util.shape[1], system_data_util.shape[0]))
   print("Loaded transfers data. {0} systems; {1} replications".format(system_data_tran.shape[1], system_data_tran.shape[0]))
   
   df_tran = pd.DataFrame(system_data_tran)
   df_util = pd.DataFrame(system_data_util)
   df_wait = pd.DataFrame(system_data_wait)
   
   return df_wait, df_util, df_tran


