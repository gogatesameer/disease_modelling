# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 17:49:13 2019

@author: Sameer
"""



import numpy as np
from matplotlib import pyplot
import matplotlib.pylab as plt


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
gammaOne = 0.25 # Recovery to Susceptible

sir = [S, I, R, D]


## Get Random contact rate based on Random Sampling
def contact_rate(step,susceptible,infected):
    count = 0
    #infected = int(beta * infected)
    for j in range(infected):
        for i in range(betaOne):
            p = random.randint(1,10000)
            if p <= susceptible:
                count = count + 1
    return beta *count

##Get probability matrix based on contact rate and previous state
def transition_matrix(contact,sir, step):
    #tranistion from Susceptible
    prob_s_i = contact / sir[0]
    prob_s_r = gamma 
    if prob_s_i > 1:
        prob_s_i = 1 - gamma
        
    prob_s_s = 1 - (prob_s_i + prob_s_r)
    prob_s_d = 0
    #transition from Infected
    prob_i_d = 0.615
    prob_i_r = 0.295
    prob_i_s = 0
    prob_i_i = 1 - (prob_i_d + prob_i_r)
    
    #transition from State D - all zeros
    #transition from Recovered only to Suspectible
    prob_r_s = 0.25 * (0.295 *sir[1] /(0.15 *sir[0] + 0.295 *sir[1]))
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
    return P
    
    
#P = transition_matrix(contact_rate,sir)


# Get the data
plot_data = []
for step in range(100):
    contact = contact_rate(step,int(sir[0]),int(sir[1]))
    print(sir,contact)
    P = transition_matrix(contact,sir,step)
    #print (P)
    result = sir * P
    sir = result.tolist()[0]
    plot_data.append(np.array(result).flatten())

# Convert the data format
plot_data = np.array(plot_data)

# Create the plot
plt.plot(plot_data[:, 0], label='S(t)')
plt.plot(plot_data[:, 1], label='I(t)')
plt.plot(plot_data[:, 2], label='D(t)')
plt.plot(plot_data[:, 3], label='R(t)')

plt.legend()

plt.xlabel('T')
plt.ylabel('N')

# use scientific notation
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.show()
