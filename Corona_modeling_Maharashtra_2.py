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
S = N - 4
I = 4
R = 0
D = 0
betaOne = 2 # infection rate
beta = 0.25  # Probability of Infection , Considering Quarantine , people measures
betaLockdown = 0.2
gamma = 0.0 # recovery rate  - Vaccination
gammaOne = 0.005 ## Recovered to Susceptible
vaccinated = 0
numWards = 11
#responseFactor = 9

r0_lockdown = 2
r0_post_lockdown = 1.4
mcmc = 1
days = 400
sigma = 3

labels = [ 'KhadakWasla','Parvati' ,'Kothrud','Kasba Peth','Camp','Wadgaon Sheri','Hadpsar',
           'Bhosari','Pimpri','Chinchwad','Shivaji Nagar']

population =[584522,425206,485829,348868,349744,548397,605110,529521,424425,622176,366840]

lockdownInterval = [[10,90],[400,430]]
lockdown = False

class ward(object):
    def __init__(self,total=500000,infected=0):
        self.total = total
        self.susceptible = total
        self.exposed = infected
        self.infected = 0
        self.died = 0
        self.recovered = 0
    
    def set_ward_values(self,result):
        self.susceptible = result[0]
        self.exposed = result[1]
        self.infected = result[2]
        self.died = result[3]
        self.recovered = result[4]
        
    def get_ward_values(self):
        p = list((self.susceptible,self.exposed,self.infected,self.died,self.recovered))
        int_values = [int(i) for i in p]
        return int_values

def migrate_ward(ward1 ,ward2,step):
    if step < 75:
        movements = 500
    else:
        movements = 500 + step*50
    for i in range(movements):
        j = random.randint(1,ward1.total)
        if j < ward1.exposed:
            ward1.exposed = ward1.exposed - 1
            ward2.exposed = ward2.exposed + 1
        elif j > ward1.exposed and (j < ward1.exposed +  ward1.infected):
            ward1.infected = ward1.infected - 1
            ward2.infected = ward2.infected + 1
        elif j > ward1.infected + ward1.exposed and (j < ward1.infected + ward1.susceptible + ward1.exposed):
            ward1.susceptible = ward1.susceptible - 1
            ward2.susceptible = ward2.susceptible + 1
        elif j > ward1.infected + ward1.susceptible + ward1.exposed and (j < ward1.exposed + ward1.infected + ward1.susceptible + ward1.recovered):
            ward1.recovered = ward1.recovered - 1
            ward2.recovered = ward2.recovered + 1
                
       
def contact_rate(w,step,responseFactor):
    global lockdown , lockdownInterval,betaOne
    if mcmc:
        count = 0
        #print(w.infected)
        #infected = int(beta * infected)
        q = random.randint(0,1)
        #print(w.exposed)
        for j in range(int(w.exposed)):
            for i in range(betaOne):
                p = random.randint(1,w.total)
                if p <= w.susceptible:
                    count = count + 1
#      if step > 75:
#           j = 75*responseFactor
 #       else:
  #          j = step*responseFactor
   #     return  (365.0 / (365 + j ) ) * beta *count
        for i in range(len(lockdownInterval)):
            if step in range(lockdownInterval[i][0],lockdownInterval[i][1]):
                lockdown = True
            
        if lockdown == True:
            return  betaLockdown * count * responseFactor/100
        else:
            return  beta * count * responseFactor/100
                
    else:
        #print(w.infected)

        if step < 75:
            return int(r0_lockdown*w.exposed*betaLockdown)
        return int(r0_post_lockdown* w.exposed*beta)

 
    
def transition_probability(contact,w):
    global vaccinated
    #tranistion from Susceptible
    prob_s_e = contact / (w.susceptible +1)
    #print(prob_s_e)
    prob_s_i = 0
    prob_s_r = gamma 
    if prob_s_i > 1:
        prob_s_i = 1 - gamma
        
    prob_s_s = 1 - (prob_s_e + prob_s_r)
    prob_s_d = 0
    
    prob_e_i = 1.0/sigma
    prob_e_s = 0
    prob_e_e = 1 - prob_e_i - 0.005
    prob_e_d = 0
    prob_e_r = 0.005
    
    

    
    #transition from Infected
    prob_i_d = 0.02
    prob_i_e = 0
    prob_i_r = 0.14
    prob_i_s = 0
    prob_i_i = 1 - (prob_i_d + prob_i_r)
    

    #transition from Recovered only to Suspectible
    prob_r_s = gammaOne
    prob_r_r = 1 - prob_r_s
    prob_r_i = 0
    prob_r_d = 0
    prob_r_e = 0
    
    #All probabbility from D state are 0 except D2D
    prob_d_d = 1
    prob_d_i = prob_d_r = prob_d_s = prob_d_e = 0
    
    ## Build transition probability matrix
    P = np.matrix([[prob_s_s,prob_s_e,prob_s_i,prob_s_d,prob_s_r],
                   [prob_e_s,prob_e_e,prob_e_i,prob_e_d,prob_e_r],
                   [prob_i_s,prob_i_e,prob_i_i,prob_i_d,prob_i_r],
                   [0.,0.,0.,1.0,0.],
                   [prob_r_s,0.,0.,0.,prob_r_r]])
    vaccinated = vaccinated + prob_s_r * w.susceptible

    return P

def iteration(responseFactor):
    wards = []
    for i in range(numWards):
        wards.append(ward(population[i],0))
    wards[3].exposed = 50
    wards[5].exposed = 50
    

    plot_data = []
    for step in range(days):
        for i in range(numWards):
            ward_infected_data = []
            #contact = contact_rate(wards[i],step)
            contact = contact_rate(wards[i],step,responseFactor)
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
            ward_infected_data.append(wards[k].get_ward_values()[2])
            #print(wards[k].get_ward_values())
            
        #print("######################################################")

        plot_data.append(np.array(ward_infected_data).flatten())
        #print("Step",step,"Done")
    
        
    plot_data = np.array(plot_data)
    
    for i in range(numWards):
        plt.figure(1)
        plt.plot(plot_data[:, i], label= labels[i])
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Infected Population per ward')
    
    city_sum = []
    for i in range(days):
        city_sum.append(sum(plot_data[i]))
        
    plt.figure(2)
    plt.plot(city_sum,label = "Pune City Numbers for reponse " + str(responseFactor))
    plt.legend()
    plt.xlabel('Time - Iteration')
    plt.ylabel('Pune City Infections')
    plt.show()
    
    
if __name__== "__main__":
    for i in range(90,95):
        iteration(i)
  
    
    
    
   

        
    





        
           
    