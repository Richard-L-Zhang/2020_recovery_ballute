import numpy as np
import scipy as sp
import scipy.interpolate
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import json

import simulation
import plot_figure
import temperature

#parameters 
N,max_t,Q_deploy,radius=int(1E5),700,0,0.35
a_drop, v_drop = 150000, 0 # Second stage parameters
m_stage = 11

# ------------------------------           main          ----------------------------------

#whether to rerun simulation
#simulation.dump_simulation_data(N,max_t,Q_deploy,radius, m_stage, a_drop, v_drop)

alt, vel, mach, acc, drag, Q, t_list, key_points=simulation.get_simulation_data()
plot_figure.plot(alt, vel, mach, acc, drag, Q, t_list,key_points['index_1000'],key_points['index_deploy'])
power=temperature.get_power(vel,drag)
temperature.temperature_simulation(t_list,temperature.get_power(vel,drag),radius)
