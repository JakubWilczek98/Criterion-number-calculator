import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

def interpolate(x,y):
    return interp1d(x, y, 'cubic')
    
def new_values(new_x, f):
    return f(new_x)

def visu(temp,value,new_temperature, new_values):
    plt.plot(temp, value,'o',new_temperature, new_values, '*')
    plt.show()


if __name__ == "__main__":
    #Data set
    csv_file = pd.read_csv('dry_air.csv', sep=',',header=None)
    #New temperature
    new_temperature = np.arange(-50, 1200+1, 1)
    new_v = []
    A = []
    #main
    for i in csv_file:
        new_v = 0
        new_v = new_values(new_temperature, interpolate(csv_file[0], csv_file[i]))
        #visu(csv_file[0],csv_file[i],new_temperature,new_v)
        A.append(new_v)
    #Save dataset
    A = np.array(A)
    A = np.round(A,6)
    #print(A)
    np.savetxt("new_csv_dry_air.csv", np.column_stack(A), delimiter=",", fmt='%s')
        
    
    





