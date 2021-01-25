# plot!

import numpy as np
import scipy as sp
import scipy.interpolate
import math
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import json
import simulation

def plot(alt, vel, mach, acc, drag, Q, t_list,index_1000,index_deploy):
    '''Plot the initial 6 figures'''
    fig1, axes1 = plt.subplots(2, 3, figsize=(13, 8), dpi = 120) # Detailed graphs for a single simulation
    axes1[0][0].plot(t_list, alt)
    axes1[0][0].set_ylabel("Altitude ASL / $m$")
    axes1[0][0].set_title("Altitude")
    axes1[0][1].plot(t_list, vel)
    axes1[0][1].set_ylabel("Vertical speed (down positive) / $ms^{{-1}}$")
    axes1[0][1].set_title("Vertical speed")
    axes1[0][1].plot(t_list[index_1000], vel[index_1000], marker = "x", markersize = 8, color = "r", label = "1km speed")
    axes1[0][1].annotate("1 km: {0:.4} $ms^{{-1}}$, after {1:.4} $s$".format(vel[index_1000],t_list[index_1000]),
                xy=(t_list[index_1000], vel[index_1000]), xycoords="data",
                xytext=(-170, 50), textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))
    axes1[1][0].plot(t_list, mach)
    axes1[1][0].set_ylabel("Local Mach / $M$")
    axes1[1][0].set_title("Mach number")
    axes1[1][1].plot(t_list, acc)
    axes1[1][1].set_ylabel("Vertical acceleration (down positive) / $ms^{-2}$")
    axes1[1][1].set_title("Acceleration")
    peak_accel = max(list(map(abs, acc)))
    peak_accel_index = np.argmax((list(map(abs, acc))))
    pa_sign = np.sign(acc[peak_accel_index])
    axes1[1][1].annotate("Peak accel. {:.2f} $ms^{{-2}}$".format(pa_sign * peak_accel),
                xy=(t_list[peak_accel_index], pa_sign*peak_accel), xycoords="data",
                xytext=(30, 30), textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))
    axes1[0][2].plot(t_list, Q)
    axes1[0][2].set_ylabel("Dynamic pressure / $Pa$")
    axes1[0][2].set_title("Dynamic pressure")
    axes1[0][2].plot(t_list[index_deploy], Q[index_deploy], marker = "x", markersize = 8, color = "r", label = "Ballute deployment")
    axes1[0][2].legend()
    axes1[0][2].annotate("Max Q: {:.2f} $Pa$".format(max(Q), 1),
                xy=(t_list[np.argmax(Q)],max(Q)), xycoords="data",
                xytext=(50, -30), textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))
    axes1[1][2].set_title("Ballute Drag")
    axes1[1][2].set_ylabel("Drag / $N$")
    axes1[1][2].plot(t_list, drag)
    axes1[1][2].annotate("Max Force: {:.2f} $N$".format(max(drag)),
                xy=(t_list[np.argmax(drag)],max(drag)), xycoords="data",
                xytext=(70, -5), textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))
    plt.tight_layout()
    plt.show()