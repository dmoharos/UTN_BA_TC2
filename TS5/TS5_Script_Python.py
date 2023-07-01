import scipy.signal as sig
import sympy as sp
import numpy as np
from numpy import pi

import matplotlib as mpl
from IPython.display import display, Markdown

from pytc2.sistemas_lineales import tf2sos_analog
from pytc2.sistemas_lineales import pretty_print_lti
from pytc2.sistemas_lineales import pretty_print_SOS
from pytc2.sistemas_lineales import analyze_sys

#----------------------------------------------------------------------------#

def calculoEpsilonFiltro (alfa_max):
    return round(np.sqrt(10**(alfa_max/10)-1), 4)

#----------------------------------------------------------------------------#

def calculoOrdenFiltro(alfa_min_s1, Omega_s1, alfa_min_s2, Omega_s2):
    
    for N_s1 in range(1,10):
        C_nn = (np.cosh(N_s1*(np.arccosh(Omega_s1))))**2
        att = 10*np.log10(1+(eps**2)*C_nn)
        #print('Para N_s1= {:d}: ¿att = {:3.4f} dB >= α_min= {:d}?'.format(N_s1, att, alfa_min_s1))
        if att >= alfa_min_s1:
            break
    
    for N_s2 in range(1,10):
        C_nn = (np.cosh(N_s2*(np.arccosh(Omega_s2))))**2
        att = 10*np.log10(1+(eps**2)*C_nn)
        #print('Para N_s2= {:d}: ¿att = {:3.4f} dB >= α_min= {:d}?'.format(N_s2, att, alfa_min_s2))
        if att >= alfa_min_s1:
            break
    
    if N_s1 >= N_s2:
        N= N_s1
    else:
        N= N_s2
    return N

#----------------------------------------------------------------------------#

omega_0 = 2*pi*22e3                  # rad/s
Q = 5

alfa_max = 0.5                       # dB
alfa_min_s1 = 16                     # dB
alfa_min_s2 = 24                     # dB

f_s1_plantilla = 17e3                # Hz
f_s2_plantilla = 36e3                # Hz

omega_s1 = 2*pi*f_s1_plantilla       # rad/s
omega_s2 = 2*pi*f_s2_plantilla       # rad/s

omega_1, omega_2= sp.symbols("w1, w2")

sistema= sp.solve([ 
                  ((omega_0)/Q) +omega_1 -omega_2,
                  ((omega_0**2)/omega_1) -omega_2
                  ], 
                  [omega_1, omega_2])

omega_1 = float(sistema[1][0])
omega_2 = float(sistema[1][1])

Omega_omega= omega_0
omega_s1= omega_s1 / Omega_omega
omega_1= omega_1 / Omega_omega
omega_0= omega_0 / Omega_omega
omega_2= omega_2 / Omega_omega
omega_s2= omega_s2 / Omega_omega

omega_s1= round(omega_s1, 4)
omega_1= round(omega_1, 4)
omega_0= round(omega_0, 4)
omega_2= round(omega_2, 4)
omega_s2= round(omega_s2, 4)

Omega_s1= Q*(omega_s1**2-1)/omega_s1
Omega_s2= Q*(omega_s2**2-1)/omega_s2

# Desestimamos el signo (-) por ser |T_LP| una función par
Omega_s1= -Omega_s1


eps = calculoEpsilonFiltro(alfa_max)
eps_2 = round(eps**2, 4)

N = calculoOrdenFiltro(alfa_min_s1, Omega_s1, alfa_min_s2, Omega_s2)

Cn3 = [4, 0, -3, 0]             # Coeficientes del polinomio grado 3 de Chevyshev
Cn6 = np.polymul(Cn3, Cn3)      # Elevamos al cuadrado el denominador
Cn6 = Cn6 * eps**2              # Multiplicamos por ε^2
Cn6[6]= Cn6[6] + 1              # Sumamos 1 al término independiente
num_T_lp= [np.sqrt(1/Cn6[0])]   # Hacemos mónico el polinomio numerador
Cn6 = Cn6 / Cn6[0]              # Hacemos mónico el polinomio denominador
Cn6[4]= -Cn6[4]                 # Cambiamos de signo al coeficiente del término cuadrático producto 
                                # del reeemplazo de w^2= s^2/j^2
Cn6[0]= -Cn6[0]                 # Cambiamos de signo al coeficiente del término séxtico producto 
                                # del reeemplazo de w^2= s^2/j^2

p_T_lp = np.roots(Cn6)        
den_T_lp= np.poly([p_T_lp for p_T_lp in p_T_lp if p_T_lp.real < 0])

num_T_bp, den_T_bp= sig.lp2bp(num_T_lp, den_T_lp, omega_0, bw= 1/Q)
T_bp_sos = tf2sos_analog(num_T_bp, den_T_bp)
analyze_sys(T_bp_sos, sys_name='Filtro pasa banda Chevyshev orden 3')

