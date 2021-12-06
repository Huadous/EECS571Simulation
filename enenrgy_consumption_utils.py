import numpy as np
from numpy.lib import delete
pg0 = 100       # the average CPU runtime power
gamma = 50      # constant coefficients that depend on the hardware and the application characteristics, indicating 
cg = 150        # the sensitivity to memory frequency scaling and the core voltage/frequency scaling respectively 
# D = 25          # s the component that is sensitive to GPU frequency scaling
delta = 0.8     # a constant factor that indicates the sensitivity of this application to GPU core frequency scaling
t0 = 5          # represents the other component in task execution time



def g1(vgc):
    return np.sqrt((vgc - 0.5)/2) + 0.5

def g1_reverse(fgc):
    return 2 * (fgc - 0.5) ** 2 + 0.5

def average_power_consumption(vgc, fgc, fgm):
    return pg0 + gamma * fgm + cg * (vgc) ** 2 * fgc

def run_time(fgc, fgm, D):
    return D * (delta / fgc + (1 - delta) / fgm) + t0

def run_time_reverse(time):
    return time - t0

def run_time_reverse_new(fgc, fgm, time):
    return (time - t0) / (delta / fgc + (1 - delta) / fgm)

def power_consumption(vgc, fgc, fgm, D):
    apc = average_power_consumption(vgc, fgc, fgm)
    rt = run_time(fgc, fgm, D)
    # print('apc: ' + str(apc), 'rt: ' + str(rt))
    return apc * rt 

def vgc_to_fgm_based_on_t(V, time_interval, D):
    fgc = g1(V)
    fgm = D*(1-delta) / (time_interval - t0 - D * delta / fgc)
    return fgm
