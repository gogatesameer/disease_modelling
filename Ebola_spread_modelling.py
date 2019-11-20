# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 17:24:30 2019

@author: Sameer
"""

import matplotlib.pylab as plt
from scipy.integrate import odeint
import numpy as np

N = 10000
S = N - 1
I = 1
R = 0
D = 0
betaOne = 23 # infection rate
beta = 0.3
gamma = 0.15 # recovery rate
alphaOne = 0.4
alphaTwo = 0.25
deltaOne = 0.3
deltaTwo = 0.75
gammaOne = 0.25

#Numerical Solution
# differential equatinons
def diff(sir, t):
    # sir[0] - S, sir[1] - I, sir[2] - R
    dsdt = gammaOne * sir[2] - betaOne * ( 1 - beta) *sir[0] *sir[1] / N - gamma * sir[0]
    
    didt = betaOne * ( 1 - beta) *sir[0] *sir[1] / N - alphaOne * beta * sir[1] - \
    alphaTwo * (1 - beta) * sir[1] -( deltaOne * beta * sir[1] ) - deltaTwo * ( 1- beta)  * sir[1]
    
    drdt = alphaOne * beta * sir[1] + alphaTwo * (1 - beta) * sir[1] + gamma * sir[0] - gammaOne * sir[2]
    
    dDdt = deltaOne * beta * sir[1] + deltaTwo * ( 1- beta) * sir[1]
    
    print (dsdt , didt , drdt , dDdt)
    
    dsirDdt = [dsdt, didt, drdt, dDdt]
    
    return dsirDdt


# initial conditions
sir0 = (S, I, R, D)

# time points
t = np.linspace(0, 40)

# solve ODE
# the parameters are, the equations, initial conditions, 
# and time steps (between 0 and 100)
sir = odeint(diff, sir0, t)

plt.plot(t, sir[:, 0], label='S(t)')
plt.plot(t, sir[:, 1], label='I(t)')
plt.plot(t, sir[:, 2], label='R(t)')
plt.plot(t, sir[:, 3], label='D(t)')



plt.legend()

plt.xlabel('T')
plt.ylabel('N')

# use scientific notation
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.show()