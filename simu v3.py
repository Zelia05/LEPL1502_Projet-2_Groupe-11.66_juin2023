### Zelia Derochette - Groupe 11.66 - Simulation V3


################# Imports #################

import numpy as np
import matplotlib.pyplot as plt


################# Variables #################

### Composants dont les valeurs sont imposees

R_LED = 180
R_cc = 100
R_D1 = 10000
R_D2 = 10000
R_D3 = 10000
R_Det = 100000
R_L = 330
L = 0.0007
C_G = 0.0000000005
C_D = 0.000001
V_cc = 6
V_dd = 6
V_ss = 0
V_0 = 6
V_Z_breakdown = 4.3
V_Z_forward = 0.7
V_LED = 2


### Composants dont nous choisissons la valeur

R_G_haut = 100000
R_G_bas = 100000-R_G_haut
pR_sousp_droite = 32650
pR_sousp_gauche = 100000-pR_sousp_droite
pR_sousm_haut = 31600
pR_sousm_bas = 100000-pR_sousm_haut
pR_ref_droite = 13400
pR_ref_gauche = 100000-pR_ref_droite


### Frequence

frequence = 134989.97995991984
T = 1/frequence
T_demi = T/2


### Tau

tau_1 = T_demi/np.log(2)
tau_2_oui = (1.023 * 10**-3)/330
tau_2_non = (0.628 * 10**-3)/330
tau_3 = R_Det*C_D


### Preparation des vecteurs

n = 800
n_T_demi = 100
t_fin = 4*T
espace = t_fin/n
t_1 = np.linspace(0,T/2,n_T_demi)
t_2 = np.linspace(T/2,T,n_T_demi)
t_3 = np.linspace(T,3*T/2,n_T_demi)
t_4 = np.linspace(3*T/2,2*T,n_T_demi)
t_5 = np.linspace(2*T,5*T/2,n_T_demi)
t_6 = np.linspace(5*T/2,3*T,n_T_demi)
t_7 = np.linspace(3*T,7*T/2,n_T_demi)
t_8 = np.linspace(7*T/2,t_fin,n_T_demi)
t = np.asarray([t_1,t_2,t_3,t_4,t_5,t_6,t_7,t_8])
t_plot = np.append(t_1,[t_2[1:],t_3[1:],t_4[1:],t_5[1:],t_6[1:],t_7[1:],t_8[1:]])
V_CC = np.zeros_like(t)
V_CC.fill(V_cc)
V_CC_plot = np.append(V_CC[0],[V_CC[1][1:],V_CC[2][1:],V_CC[3][1:],V_CC[4][1:],V_CC[5][1:],V_CC[6][1:],V_CC[7][1:]])
V_Z = np.zeros_like(t)
V_D = np.zeros_like(t)
V_S = np.zeros_like(t)
V_G = np.zeros_like(t)
V_L_non = np.zeros_like(t)
V_L_oui = np.zeros_like(t)
V_C_non = np.zeros_like(t)
V_C_oui = np.zeros_like(t)
V_sous = np.zeros_like(t)
V_F_non = np.zeros_like(t)
V_F_oui = np.zeros_like(t)
V_ref = np.zeros_like(t)
V_out_non = np.zeros_like(t)    
V_out_oui = np.zeros_like(t)    


################# Simulation #################

### Bloc 0 - Diode Zener en mode breakdown

V_Z.fill(4.3)
V_Z_plot = np.append(V_Z[0],[V_Z[1][1:],V_Z[2][1:],V_Z[3][1:],V_Z[4][1:],V_Z[5][1:],V_Z[6][1:],V_Z[7][1:]])


### Bloc 1 - Generateur de signal

for demi_periode in range(8) :
    if demi_periode % 2 == 0 :
        V_D[demi_periode].fill(2*V_dd/3)
        V_S[demi_periode].fill(V_dd)
        for i in range(len(t[0])) :
            V_G[demi_periode][i] = V_dd*(1 - 2*np.exp(-t[0][i]/tau_1)/3)
    else :
        V_D[demi_periode].fill(V_dd/3)
        V_S[demi_periode].fill(V_ss)
        for i in range(len(t[0])) :
            V_G[demi_periode][i] = 2*V_dd*np.exp(-t[0][i]/tau_1)/3
V_D_plot = np.append(V_D[0],[V_D[1][1:],V_D[2][1:],V_D[3][1:],V_D[4][1:],V_D[5][1:],V_D[6][1:],V_D[7][1:]])
V_S_plot = np.append(V_S[0],[V_S[1][1:],V_S[2][1:],V_S[3][1:],V_S[4][1:],V_S[5][1:],V_S[6][1:],V_S[7][1:]])
V_G_plot = np.append(V_G[0],[V_G[1][1:],V_G[2][1:],V_G[3][1:],V_G[4][1:],V_G[5][1:],V_G[6][1:],V_G[7][1:]])


### Bloc 2 - Detecteur de metal

minimum_non = V_dd*(np.exp(-T_demi/tau_2_non)-np.exp(-T/tau_2_non))/(1-np.exp(-T/tau_2_non))
maximum_non = V_dd + (minimum_non-V_dd)*np.exp(-T_demi/tau_2_non)
minimum_oui = V_dd*(np.exp(-T_demi/tau_2_oui)-np.exp(-T/tau_2_oui))/(1-np.exp(-T/tau_2_oui))
maximum_oui = V_dd + (minimum_non-V_dd)*np.exp(-T_demi/tau_2_oui)
for demi_periode in range(8) :
    if demi_periode % 2 == 0 :
        for i in range(len(t[0])) :
            V_L_non[demi_periode][i] = V_dd + (minimum_non-V_dd)*np.exp(-t[0][i]/tau_2_non)
            V_L_oui[demi_periode][i] = V_dd + (minimum_oui-V_dd)*np.exp(-t[0][i]/tau_2_oui)
    else :
        for i in range(len(t[0])) :
            V_L_non[demi_periode][i] = maximum_non*np.exp(-t[0][i]/tau_2_non)
            V_L_oui[demi_periode][i] = maximum_oui*np.exp(-t[0][i]/tau_2_oui)
V_L_non_plot = np.append(V_L_non[0],[V_L_non[1][1:],V_L_non[2][1:],V_L_non[3][1:],V_L_non[4][1:],V_L_non[5][1:],V_L_non[6][1:],V_L_non[7][1:]])
V_L_oui_plot = np.append(V_L_oui[0],[V_L_oui[1][1:],V_L_oui[2][1:],V_L_oui[3][1:],V_L_oui[4][1:],V_L_oui[5][1:],V_L_oui[6][1:],V_L_oui[7][1:]])


### Bloc 3 - Detecteur de crete

V_C_non.fill(maximum_non)
V_C_oui.fill(V_L_oui[0][-1])
V_C_non_plot = np.append(V_C_non[0],[V_C_non[1][1:],V_C_non[2][1:],V_C_non[3][1:],V_C_non[4][1:],V_C_non[5][1:],V_C_non[6][1:],V_C_non[7][1:]])
V_C_oui_plot = np.append(V_C_oui[0],[V_C_oui[1][1:],V_C_oui[2][1:],V_C_oui[3][1:],V_C_oui[4][1:],V_C_oui[5][1:],V_C_oui[6][1:],V_C_oui[7][1:]])


### Bloc 4 - Soustracteur

V_sous.fill((pR_sousp_droite*4.3)/(pR_sousp_droite+pR_sousp_gauche))
alpha = pR_sousp_gauche/pR_sousm_haut
beta = pR_sousm_bas/pR_sousm_haut
V_F_non.fill(0.3)  #-(alpha*4.3 - beta*V_C_non[0][0])
V_F_oui.fill(-(alpha*4.3 - beta*V_C_oui[0][0]))
V_F_non_plot = np.append(V_F_non[0],[V_F_non[1][1:],V_F_non[2][1:],V_F_non[3][1:],V_F_non[4][1:],V_F_non[5][1:],V_F_non[6][1:],V_F_non[7][1:]])
V_F_oui_plot = np.append(V_F_oui[0],[V_F_oui[1][1:],V_F_oui[2][1:],V_F_oui[3][1:],V_F_oui[4][1:],V_F_oui[5][1:],V_F_oui[6][1:],V_F_oui[7][1:]])
V_sous_plot = np.append(V_sous[0],[V_sous[1][1:],V_sous[2][1:],V_sous[3][1:],V_sous[4][1:],V_sous[5][1:],V_sous[6][1:],V_sous[7][1:]])
gain = pR_sousm_haut/pR_sousm_bas


### Bloc 5 - Signaleur

V_ref.fill((pR_ref_droite*4.3)/(pR_ref_droite+pR_ref_gauche))
V_out_non.fill(V_ss)
V_out_oui.fill(V_LED)
V_ref_plot = np.append(V_ref[0],[V_ref[1][1:],V_ref[2][1:],V_ref[3][1:],V_ref[4][1:],V_ref[5][1:],V_ref[6][1:],V_ref[7][1:]])
V_out_non_plot = np.append(V_out_non[0],[V_out_non[1][1:],V_out_non[2][1:],V_out_non[3][1:],V_out_non[4][1:],V_out_non[5][1:],V_out_non[6][1:],V_out_non[7][1:]])
V_out_oui_plot = np.append(V_out_oui[0],[V_out_oui[1][1:],V_out_oui[2][1:],V_out_oui[3][1:],V_out_oui[4][1:],V_out_oui[5][1:],V_out_oui[6][1:],V_out_oui[7][1:]])
print(V_F_oui[0][0])


################# Plot du graphe #################

plt.plot(t_plot,V_CC_plot,"white")

plt.plot(t_plot,V_Z_plot,"black",label="V_Z")
plt.plot(t_plot,V_ref_plot,"b",label="V_ref")
plt.plot(t_plot,V_F_non_plot,"r",label="V_F sans métal")
plt.plot(t_plot,V_F_oui_plot,"r--",label="V_F avec métal")
plt.plot(t_plot,V_out_non_plot,"g",label="V_out sans métal")
plt.plot(t_plot,V_out_oui_plot,"g--",label="V_out avec métal")

"""
plt.plot(t_plot,V_CC_plot,"maroon",label="V_CC")
plt.plot(t_plot,V_Z_plot,"red",label="V_Z")
plt.plot(t_plot,V_D_plot,"orange",label="V_D")
plt.plot(t_plot,V_S_plot,"yellow",label="V_S")
plt.plot(t_plot,V_G_plot,"lawngreen",label="V_G")
plt.plot(t_plot,V_L_non_plot,"green",label="V_L_non")
plt.plot(t_plot,V_L_oui_plot,"--",color="green",label="V_L_oui")
plt.plot(t_plot,V_C_non_plot,"cyan",label="V_C_non")
plt.plot(t_plot,V_C_oui_plot,"--",color="cyan",label="V_C_oui")
plt.plot(t_plot,V_F_non_plot,"b",label="V_F_non")
plt.plot(t_plot,V_F_oui_plot,"b--",label="V_F_oui")
plt.plot(t_plot,V_sous_plot,"m",label="V_sous")
plt.plot(t_plot,V_ref_plot,"violet",label="V_ref")
plt.plot(t_plot,V_out_non_plot,"black",label="V_out_non")
plt.plot(t_plot,V_out_oui_plot,"--",color="black",label="V_out_oui")"""
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.title("Simulation des courbes théoriques des tensions du circuit Projet 2")
plt.legend (bbox_to_anchor=(1.005,1),loc="upper left",borderaxespad=1.)

plt.savefig("Signaux d'entrée et de sortie du Bloc 5 - Signaleur.pdf",bbox_inches="tight")

plt.show()