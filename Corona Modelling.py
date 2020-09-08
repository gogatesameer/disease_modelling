# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 17:49:13 2019

@author: Sameer
"""



import numpy as np
from matplotlib import pyplot
import matplotlib.pylab as plt
import random
import queue
import math


N =   5290644 #1350000000
S = N - 3
I = 3
R = 0
D = 0
betaOne = 3 # infection rate
beta = 0.855 #Quarantied %
gamma = 0.000 # recovery rate 0 since no Vaccination
gammaOne = 0.00# Recovery to Susceptible - Loss of Immunity - 0 assuming no re-infection
#latentFactor = 2
vaccinated = 0

sir = [S, I, D,R]



## Get Random contact rate based on Sampling
def contact_rate(susceptible,infected,step):
    count = 0
    q = random.randint(0,1)
    for j in range(infected):
        for i in range(betaOne-q):
            p = random.randint(1,N)
            if p <= susceptible:
                count = count + 1
    #print((365/(365+ 13*step)) * (1-beta) * count)
    if step < 120:
        return (365/(365+ 13*step)) * (1-beta) * count
    return (365/(365+ 13*120)) * (1-beta) * count

##Get probability matrix based on contact rate and previous state
def transition_probability(contact,sir):
    global vaccinated
    #tranistion from Susceptible
    prob_s_i = contact / (sir[0])
    prob_s_r = gamma 
    if prob_s_i > 1:
        prob_s_i = 1 - gamma
        
    prob_s_s = 1 - (prob_s_i + prob_s_r)
    prob_s_d = 0
    #transition from Infected
    prob_i_d = 0.0014571 #7 day period considered - so number is 0.02/7
    prob_i_r = 0.06857
    prob_i_s = 0
    prob_i_i = 1 - (prob_i_d + prob_i_r)
    
    #transition from State D - all zeros
    #transition from Recovered only to Suspectible
    prob_r_s = gammaOne * (sir[3] - vaccinated)/(sir[3] + 1)
    prob_r_r = 1 - prob_r_s
    prob_r_i = 0
    prob_r_d = 0
    
    #All probabbility from D state are 0 except D2D
    prob_d_d = 1
    prob_d_i = prob_d_r = prob_d_s = 0
    
    P = np.matrix([[prob_s_s,prob_s_i,prob_s_d,prob_s_r],
                   [prob_i_s,prob_i_i,prob_i_d,prob_i_r],
                   [0.,0.,1.,0.],
                   [prob_r_s,0.,0.,prob_r_r]])
    vaccinated = vaccinated + prob_s_r * sir[0]
    #print (vaccinated)
    return P
    
    
#P = transition_matrix(contact_rate,sir)


# Get the data
plot_data = []
plot_data.append(np.array(sir).flatten())
for step in range(365):
    #print(infected)          
    contact = contact_rate(int(sir[0]),int(sir[1]),step )
    P = transition_probability(contact,sir)
    #print (P)
    result = sir * P
    sir = result.tolist()[0]
    print(step,sir)
    plot_data.append(np.array(result).flatten())
    #print(sir[1] - infected_earlier)
 # Convert the data format
plot_data = np.array(plot_data)

# Create the plot
#plt.plot(plot_data[:, 0], label='S(t)')
plt.plot(plot_data[:, 1], label='I(t)')
plt.plot(plot_data[:, 2], label='D(t)')
plt.plot(plot_data[:, 3], label='R(t)')

plt.legend()

plt.xlabel('T')
plt.ylabel('N')

# use scientific notation
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.show()
