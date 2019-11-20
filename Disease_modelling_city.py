# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:40:24 2019

@author: Sameer
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.pylab as plt


N = 1000
S = N - 1
I = 1
R = 0
D = 0
betaOne = 9 # infection rate
beta = 0.3
gamma = 0.15 # recovery rate
alphaOne = 0.4
alphaTwo = 0.25
deltaOne = 0.3
deltaTwo = 0.75
gammaOne = 0.25

class ward(object):
    def __init__(self,susceptible=1000,infected=0):
        self.susceptible = susceptible
        self.infected = infected
        self.died = 0
        self.recovered = 0
    
    def set_ward_values(self,result):
        self.susceptible = result[0]
        self.infected = result[1]
        self.died = result[2]
        self.recovered = result[3]
    def get_ward_values(self):
        return list((self.susceptible,self.infected,self.died,self.recovered))


def migrate_ward(ward1 ,ward2):
    for i in range(50):
        j = random.randint(1,1000)
        if j < ward1.infected:
            ward1.infected = ward1.infected - 1
            ward2.infected = ward2.infected + 1
        elif j > ward1.infected and (j < ward1.infected + ward1.susceptible):
            ward1.susceptible = ward1.susceptible - 1
            ward2.susceptible = ward2.susceptible + 1
        elif j > ward1.infected + ward1.susceptible and (j < ward1.infected + ward1.susceptible + ward1.recovered):
            ward1.recovered = ward1.recovered - 1
            ward2.recovered = ward2.recovered + 1
                
       
def contact_rate(w):
    count = 0
    #infected = int(beta * infected)
    for j in range(int(w.infected)):
        for i in range(betaOne):
            p = random.randint(1,1000)
            if p <= w.susceptible:
                count = count + 1
    return beta *count

 
    
def transition_probability(contact,w):
    #tranistion from Susceptible
    prob_s_i = contact / w.susceptible
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
    prob_r_s = 0.25 * (0.295 *w.infected /(0.15 *w.susceptible + 0.295 *w.infected))
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
    
wards = []
for i in range(10):
    wards.append(ward(1000,0))
    wards[0].infected = 1

for step in range(10):
    for i in range(10):
        contact = contact_rate(wards[i])
        P = transition_probability(contact,wards[i])
        result = wards[i].get_ward_values() * P
        wards[i].set_ward_values(result.tolist()[0])
        for j in range(10):
            if i != j:
                migrate_ward(wards[i],wards[j])

for i in range(10):
    print(wards[i].get_ward_values())
        
    

            
    
        
    





        
           
    