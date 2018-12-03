import pandas as pd     

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
    Returns a pandas DataFrame containing the subset of key performance measures
    merged with a design of experiments file

    Keyword arguments:
    df_kpi -- Pandas DataFrame containing the (multilple) key performance metrics 
    indexes -- List of indexes to return from @df_kpi
    doe_file_name -- the path and filename to the design of experiment file (assume .csv)
    
    """
    df_doe = pd.read_csv(doe_file_name, index_col='System')
    df_doe.index -= 1
    df_kpi =  df_kpi[df_kpi.index.isin(indexes)]
    temp = df_doe[df_doe.index.isin(indexes)]
    df_subset_table = pd.concat([temp, df_kpi], axis=1)
    return df_subset_table.sort_values(by=['wait', 'util', 'tran'])






