import numpy as np
import scipy as sp
import scipy.interpolate
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import json
import simulation


tcc=0.25 #thermal conductivity 
density = 115000 #g/m3
thickness = 70/115000
hc=1.67#heat capacity, J/K*g
def get_power(vel, drag):
    '''get power that heats the ballute, i.e. the power that decelerates the ballute'''
    power=[]
    if len(vel) != len(drag):
        print("different length of velocity and drag lists!")
    for index in range(min(len(vel), len(drag))):
        power.append(abs(vel[index]*drag[index]))
    return power

def temperature_simulation(t_list,power,radius,layer=50,T0=float(300)):
    temperature=[[T0]*10]

    