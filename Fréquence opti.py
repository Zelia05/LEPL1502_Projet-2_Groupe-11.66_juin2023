# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:02:01 2023

@author: maxi2
"""

import numpy as np
from matplotlib import pyplot as plt

frequence = np.linspace(10000,1000000,1000)
tau_metal = (1.091 * 10**-3)/330
tau_nometal = (0.645 * 10**-3)/330
print(tau_metal)
print(tau_nometal)
diff_V_max = np.empty(len(frequence))
Vcc = 6

def VL_charge(Min,tau):
    charge = Vcc +(Min-Vcc)*np.exp (- T_demi/tau)  
    return charge
def VL_decharge(Max,tau):
    decharge = Max*np.exp(- T_demi/tau)
    return decharge

# Optimisation de la différence de tension entre charge/décharge    

for i in range(len(frequence)): 

    T = 1/frequence[i] 
    T_demi = T/2
    min_nometal = 0
    min_metal = 0


    for j in range(0,100) : 

        max_nometal = VL_charge(min_nometal, tau_nometal)
        max_metal = VL_charge(min_metal, tau_metal)
        
        min_nometal = VL_decharge(max_nometal, tau_nometal)
        min_metal = VL_decharge(max_metal, tau_metal)
    
    Max = abs(max_metal- max_nometal)
    diff_V_max[i] = Max

# Recherche de la fréquence optimale
        
max_frequence = np.max(diff_V_max)
max_frequence_index = np.where(diff_V_max == max_frequence)
max_frequence_opti = frequence[max_frequence_index]
f_opti = max_frequence_opti[0]
print("la fréquence optimale est :",f_opti,"[Hz]")   
 
plt.plot(frequence, diff_V_max)
plt.title("Graphe de différence de Tension max")
plt.xlabel("Fréquence (hZ)")
plt.ylabel("Différence de Tension")
plt.savefig("Fréquence opti.pdf")
plt.show()

#Calcul de la résistance

C = 0.05*10**(-9)
R = 1/(2*f_opti*np.log(2)*C)
print("la résistance correspondant à cette fréquence est de :",R,"[Ohm]")
    


