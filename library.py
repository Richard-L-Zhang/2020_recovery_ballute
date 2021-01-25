import numpy as np
import scipy as sp
import scipy.interpolate
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import json

atm_d, atm_p, bal_cd = [], [], [] # Data for atmosphere, cd
for entry in open("data/atm_d.txt").read().split(): # Make a copy of the data folder and correct the path if this doesn't work for you
  alt, density = entry.strip(")").strip("(").split(',')
  atm_d.append((np.float32(alt), np.float32(density)))
for entry in open("data/atm_p.txt").read().split():
  alt, pressure = entry.strip(")").strip("(").split(',')
  atm_p.append((np.float32(alt), np.float32(pressure)))
for entry in open("data/cd.txt").read().split():
  mach, cd_val = entry.strip(")").strip("(").split(',')
  bal_cd.append((np.float32(mach), np.float32(cd_val)))


mu = 398600441800000 # Constants for gravity, atmosphere
earth_r = 6370000
gamma = 1.4
a_drop, v_drop = 150000, 0 # Second stage parameters
m_stage = 11

rho = sp.interpolate.interp1d(*zip(*atm_d), copy = False, bounds_error = False, fill_value = (atm_d[0][1], 0))
p = sp.interpolate.interp1d(*zip(*atm_p), copy = False, bounds_error = False, fill_value = (atm_p[0][1], 0))
cd = sp.interpolate.interp1d(*zip(*bal_cd), copy = False, bounds_error = False, fill_value = (bal_cd[0][1], bal_cd[-1][1]))

def c(altitude): 
    '''Local speed of sound at any altitude'''
    if (rho(altitude) == 0 or p(altitude) == 0):
        return 0
    else:
        return np.sqrt(gamma*p(altitude) / rho(altitude))

def grav(altitude): 
    ''' Calculate local gravity'''
    return mu / ((earth_r + altitude)**2)

def bal_drag(altitude, velocity, mach, radius, deployed): 
    ''' Calculate ballute drag'''
    if (deployed == False or mach == 0):
        return 0
    else:
        return (0.5 * np.pi * (radius**2) * cd(mach) * rho(altitude) * (velocity**2))

def simulate(N, max_t, Q_deploy, radius, mass, drop_altitude, drop_velocity, detailed = True): 
    '''Numerical integration, fourth order Runge-Kutta (twice) '''
    alt, vel = [drop_altitude], [drop_velocity]
    mach, acc, drag, Q, deployed = [vel[0]/c(alt[0])], [-grav(alt[0])], [0.5 * rho(alt[0]) * (vel[0]**2)], [0], False
    t_list, dt = np.linspace(0, max_t-1, N), max_t/N

    for t in range(1, len(t_list)):
        if ((Q[-1] >= Q_deploy) and (deployed == False)): 
            deployed = True
            index_deploy = t
        kv1 = -grav(alt[-1]) + bal_drag(alt[-1], vel[-1], vel[-1]/c(alt[-1]), radius, deployed)/mass
        kv2 = -grav(alt[-1] + (0.5*vel[-1]*dt)) + bal_drag(alt[-1] + (0.5*vel[-1]*dt), vel[-1] + (0.5*kv1*dt), (vel[-1] + (0.5*kv1*dt))/c(alt[-1] + (0.5*vel[-1]*dt)), radius, deployed)/mass
        kv3 = -grav(alt[-1] + (0.5*vel[-1]*dt)) + bal_drag(alt[-1] + (0.5*vel[-1]*dt), vel[-1] + (0.5*kv2*dt), (vel[-1] + (0.5*kv2*dt))/c(alt[-1] + (0.5*vel[-1]*dt)), radius, deployed)/mass
        kv4 = -grav(alt[-1] + (vel[-1]*dt)) + bal_drag(alt[-1] + (vel[-1]*dt), vel[-1] + (kv3*dt), (vel[-1] + (kv3*dt))/c(alt[-1] + (vel[-1]*dt)), radius, deployed)/mass
        # Calculates coefficients for Runge-Kutta. Runge-Kutta is a set of high-order numerical integration methods
        # Error with this method reduces with (number of steps)^4, unlike Euler where error reduction is proportional to number of steps

        vel.append(vel[-1] + (dt*((kv1 + (2*kv2) +(2*kv3) + kv4)/6))) # Compute the new velocity with above coefficients
        acc.append((vel[-1]-vel[-2])/dt) # Determine the acceleration from change in velocity for graphing

        #kx1 = vel[-2]
        #kx2 = vel[-2] + (kv1*dt)/2
        #kx3 = vel[-2] + (kv2*dt)/2
        #kx4 = vel[-2] + (kv3*dt)
        #alt.append(alt[-1] + (dt*((kx1 + (2*kx2) +(2*kx3) + kx4)/6)))
        # Can substitute the above "kx" coefficients for the kv coefficients,as below, improving performance
        alt.append(alt[-1] + (dt*vel[-2]) + ((dt**2)*(kv1 + kv2 + kv3)/6)) # Compute the new altitude with above coefficients

        Q.append(0.5 * rho(alt[-1]) * (vel[-1]**2))
        mach.append(vel[-1]/c(alt[-1]))
        drag.append(bal_drag(alt[-1], vel[-1], mach[-1], radius, deployed))

        if (alt[-1] < 0):
            t_list = np.linspace(0, t_list[t], len(alt))
            break
    if (detailed == True):
        return alt, np.negative(vel), np.negative(mach), np.negative(acc), drag, Q, t_list, list(t_list).index(sp.interpolate.interp1d(alt, t_list, kind="nearest", copy = False, bounds_error = False, fill_value = max_t)(1000)), index_deploy
    else:
        return [max(np.negative(vel), max(list(map(abs, np.negative(acc))))), max(drag), max(Q), t_list[-1], vel[list(t_list).index(sp.interpolate.interp1d(alt, t_list, kind="nearest", copy = False, bounds_error = False, fill_value = max_t)(1000))]]
