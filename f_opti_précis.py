# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:46:30 2023

@author: maxi2
"""

import cmath
import numpy as np
from matplotlib import pyplot as plt

# ---- Constants ----
Vcc = 6 #V, voltage of the power supply
R_L = 330 #Ohms, resistor in the circuit RL

L1 = 0.628*10**-3 #mH, inductance without metal
L2 = 1.023*10**-3 #mH, inductance with metal
tau1 = L1/R_L
tau2 = L2/R_L

# ---- Periods ---- 
frequences = np.linspace(10000,1000000,500)



# ---- Paramètre de la simulation ---- 
n = 100 #nombre d'itérations
num_values = 100 #nombre de valeurs pour la simulation



delta_V_max_stability = np.empty(len(frequences))




# ---- Functions ----
def V_L_Charge_func(t, Min, Vcc,i,tau,T_demi) : 
    V_L_Charge = lambda t : Vcc + (Min-Vcc)*np.e**(-(t-i*T_demi)/tau)
    return V_L_Charge(t)
def V_L_Discharge_func(t, Max, Vcc,i,tau,T_demi) : 
    V_L_Discharge = lambda t : Max*np.e**(-(t-i*T_demi)/tau)

    return V_L_Discharge(t)

# ---- Calculations ---- 

for count,f in enumerate(frequences) : 
    print("---------------------------------------------------------------")
    print(f"La fréquence est de {f} Hz")
    T = 1/f #s, period of the signal
    T_demi = T/2 #s, half period of the signal
    Min1 = 0
    Min2 = 0


    for i in range(0,200,2) : 
        j = i//2
        #Nous allons calculer à n reprises les courbes de charge et de décharge


        Max1 = V_L_Charge_func((i+1)*T_demi, Min1, Vcc, i, tau1, T_demi)
        Max2 = V_L_Charge_func((i+1)*T_demi, Min2, Vcc, i, tau2, T_demi)
        
        Min1 = V_L_Discharge_func((j+1)*T, Max1, Vcc, i+1, tau1, T_demi)
        Min2 = V_L_Discharge_func((j+1)*T, Max2, Vcc, i+1, tau2, T_demi)
        print(Max2)

     
    print("difference between the last maximums : ", Max1-Max2)
    delta_V_max = abs(Max1-Max2)
    print(delta_V_max)
    delta_V_max_stability[count] = delta_V_max
    


    



# ---- Plot ----

plt.plot(frequences, delta_V_max_stability, label="Delta V_max")
plt.xlabel("Frequence (hZ)")
plt.ylabel("Delta (delta)")
plt.show()

print("---------------------------------------------------------------")
# ---- Get frequence for max delta ----
max_delta = np.max(delta_V_max_stability)
max_delta_index = np.where(delta_V_max_stability == max_delta)
max_delta_frequences = frequences[max_delta_index]
f_opti = max_delta_frequences[0]
print("La fréquence pour laquelle la différence de tension maximale est la plus grande est de : ",f_opti , "Hz")


# ----- Get the corresponding resistance -----

Cg = 0.05*10**(-9) #F, capacitance of the first bloc

Vth1 = 1*Vcc/3
Vth2 = 2*Vcc/3

R = 1/(-2*Cg*f_opti*np.log((Vth2-Vcc)/(Vth1-Vcc)))
print("La résistance est de : ", R, "Ohms")
