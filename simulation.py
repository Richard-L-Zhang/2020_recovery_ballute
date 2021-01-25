#This module runs simulation and Store data and rechieve data from simulation_data.json

import numpy as np
import scipy as sp
import scipy.interpolate
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import json

import library


def dump_simulation_data(N,max_t,Q_deploy,radius, m_stage, a_drop, v_drop):
    '''This module runs simulation and stores the data in the json file'''
    #Single RK4 simulation
    print("Begin Simulation...")
    alt, vel, mach, acc, drag, Q, t_list, index_1000, index_deploy = library.simulate(N,max_t,Q_deploy,radius, m_stage, a_drop, v_drop) 
    print("Simulation Completed!")
   
    #change to list and append to data list
    vel=vel.tolist()
    mach=mach.tolist()
    acc=acc.tolist()
    t_list=t_list.tolist()
    key_points={"index_1000":index_1000,"index_deploy":index_deploy}
    index_deploy=[index_deploy]
    simulation_data=[]
    simulation_data.append(alt)
    simulation_data.append(vel)
    simulation_data.append(mach)
    simulation_data.append(acc)
    simulation_data.append(drag)
    simulation_data.append(Q)
    simulation_data.append(t_list)
    simulation_data.append(key_points)

    #check type
    #for data in simulation_data:
     #   print(type(data))
    with open("data/simulation_data.json",'w') as f:
        json.dump(simulation_data,f)
        print("Successfully dumped simulation data!")

def get_simulation_data():
    '''This module retrieves simulation data from simulation_data.json file '''
    with open("data/simulation_data.json",'r') as f:
        data=json.load(f)
        print("Successfully loaded simulation data!")
    return data