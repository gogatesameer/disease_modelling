
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:40:24 2019

@author: Sameer
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.pylab as plt
import random
import time


N = 5290644
S = N - 3
I = 3
R = 0
D = 0
betaOne = 3 # infection rate
beta = 0.18  # Probability of Infection , Considering Quarantine
gamma = 0.0 # recovery rate
gammaOne = 0.00 ## Recovered to Susceptible
vaccinated = 0
numWards = 11

r0_lockdown = 1.05
r0_post_lockdown = 1.1
mcmc = 1

labels = [ 'KhadakWasla','Parvati' ,'Kothrud','Kasba Peth','Camp','Wadgaon Sheri','Hadpsar',
           'Bhosari','Pimpri','Chinchwad','Shivaji Nagar']

population =[584522,425206,485829,348868,349744,548397,605110,529521,424425,622176,366840]


class ward(object):
    def __init__(self,total=500000,infected=0):
        self.total = total
        self.susceptible = total
        self.infected = infected
        self.died = 0
        self.recovered = 0
    
    def set_ward_values(self,result):
        self.susceptible = result[0]
        self.infected = result[1]
        self.died = result[2]
        self.recovered = result[3]
        
    def get_ward_values(self):
        p = list((self.susceptible,self.infected,self.died,self.recovered))
        int_values = [int(i) for i in p]
        return int_values

def migrate_ward(ward1 ,ward2,step):
    if step < 75:
        movements = 5000
    else:
        movements = 5000 + step*100
    for i in range(movements):
        j = random.randint(1,ward1.total)
        if j < ward1.infected:
            ward1.infected = ward1.infected - 1
            ward2.infected = ward2.infected + 1
        elif j > ward1.infected and (j < ward1.infected + ward1.susceptible):
            ward1.susceptible = ward1.susceptible - 1
            ward2.susceptible = ward2.susceptible + 1
        elif j > ward1.infected + ward1.susceptible and (j < ward1.infected + ward1.susceptible + ward1.recovered):
            ward1.recovered = ward1.recovered - 1
            ward2.recovered = ward2.recovered + 1
                
       
def contact_rate(w,step):
    if mcmc:
        count = 0
        #infected = int(beta * infected)
        q = random.randint(0,1)
        for j in range(int(w.infected)):
            for i in range(betaOne-q):
                p = random.randint(1,w.total)
                if p <= w.susceptible:
                    count = count + 1
        if step > 75:
            j = 75*9
        else:
            j = step*9
        return  (365 / (365 + j ) ) * beta *count
    else:
        if step < 75:
            return int(r0_lockdown*w.infected - infected)
        return (r0_post_lockdown*w.infected- infected)

 
    
def transition_probability(contact,w):
    global vaccinated
    #tranistion from Susceptible
    prob_s_i = contact / (w.susceptible +1)
    prob_s_r = gamma 
    if prob_s_i > 1:
        prob_s_i = 1 - gamma
        
    prob_s_s = 1 - (prob_s_i + prob_s_r)
    prob_s_d = 0
    
    #transition from Infected
    prob_i_d = 0.003
    prob_i_r = 0.14
    prob_i_s = 0
    prob_i_i = 1 - (prob_i_d + prob_i_r)
    

    #transition from Recovered only to Suspectible
    prob_r_s = gammaOne * (w.recovered - vaccinated)/(w.recovered + 1)
    prob_r_r = 1 - prob_r_s
    prob_r_i = 0
    prob_r_d = 0
    
    #All probabbility from D state are 0 except D2D
    prob_d_d = 1
    prob_d_i = prob_d_r = prob_d_s = 0
    
    ## Build transition probability matrix
    P = np.matrix([[prob_s_s,prob_s_i,prob_s_d,prob_s_r],
                   [prob_i_s,prob_i_i,prob_i_d,prob_i_r],
                   [0.,0.,1.0,0.],
                   [prob_r_s,0.,0.,prob_r_r]])
    vaccinated = vaccinated + prob_s_r * w.susceptible

    return P

if __name__== "__main__":
    wards = []
    for i in range(numWards):
        wards.append(ward(population[i],0))
    wards[3].infected = 10
    wards[5].infected = 10
    

    plot_data = []
    for step in range(300):
        for i in range(numWards):
            ward_infected_data = []
            #contact = contact_rate(wards[i],step)
            contact = contact_rate(wards[i],step)
            P = transition_probability(contact,wards[i])
            result = wards[i].get_ward_values() * P
            wards[i].set_ward_values(result.tolist()[0])
            while True:
                j = random.randint(0,10)
                if i != j:
                    break
                    
          #  if i != (numWards -1):
           #      migrate_ward(wards[i],wards[i+1],step)
            #else:
             #   migrate_ward(wards[i],wards[0],step)
            migrate_ward(wards[i],wards[j],step)
                    
        for k in range(numWards):
            ward_infected_data.append(wards[k].get_ward_values()[1])
            #print(wards[k].get_ward_values())
            
        #print("######################################################")

        plot_data.append(np.array(ward_infected_data).flatten())
        print("Step",step,"Done")
    
        
    plot_data = np.array(plot_data)
    
    for i in range(numWards):
        plt.figure(1)
        plt.plot(plot_data[:, i], label= labels[i])
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Infected Population per ward')
    
    city_sum = []
    for i in range(300):
        city_sum.append(sum(plot_data[i]))
        
    plt.figure(2)
    plt.plot(city_sum,label = "Pune City Numbers")
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Pune City Infections')
    
        
  
    
    
    
   

        
    





        
           
    