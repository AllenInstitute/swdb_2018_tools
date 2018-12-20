import numpy as np
import pandas as pd

def print_info(some_var):
    var_type = type(some_var)
    print(var_type)
    my_nparr = np.zeros((5,5))
    my_dict = {'a':1, 'b':2}
    columns = ['A','B', 'C']
    my_pd = pd.DataFrame(index=[1,2,3], columns=columns)
    my_list = ['1', '2', '3']

    if var_type == type(my_nparr):
        print some_var.shape
    if var_type == type(my_dict):
        print some_var.keys()
    if var_type == type(my_pd):
        print some_var.columns
    if var_type == type(my_list):
        print len(some_var)  