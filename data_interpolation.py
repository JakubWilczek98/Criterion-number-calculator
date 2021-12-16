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
    csv_water = pd.read_csv('water.csv', sep=',',header=None)
    #New temperature
    new_temperature = np.arange(0, 370+1, 1)
    new_v = []
    A = []
    
    for i in csv_water:
        new_v = 0
        new_v = new_values(new_temperature, interpolate(csv_water[0], csv_water[i]))
        #visu(csv_water[0],csv_water[i],new_temperature,new_v)
        A.append(new_v)
    
    
    A = np.array(A)
    A = np.round(A,6)
    print(A)
    np.savetxt("new_csv_water.csv", np.column_stack(A), delimiter=",", fmt='%s')
        
        
    
    
    
    
    
    
    
    '''
    
    
    new_values = new_values(new_temperature,interpolate(csv_water[0], csv_water[1]))
    
    plt.plot(new_temperature, new_values, '*')
    
    
    f = interp1d(csv_water[0], csv_water[1])
    f2 = interp1d(csv_water[0], csv_water[1], kind='cubic')
    
    
    
    #plt.plot(csv_water[0],csv_water[1], 'o', x_new, f(x_new), '*')
    
    '''
    





