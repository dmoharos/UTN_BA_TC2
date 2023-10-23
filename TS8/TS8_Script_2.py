# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:18:32 2023

@author: David
"""

from scipy import signal as sig
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from pytc2.sistemas_lineales import group_delay, pzmap, analyze_sys

# ---------------------------------------------------------------------------------------- #
# Resolución numérica
# ---------------------------------------------------------------------------------------- #

#-- HPF Butterworth 2º orden --
num_butter_ord_2 = [ 1, 0, 0 ]
den_butter_ord_2 = [ 1, np.sqrt(2), 1 ]
my_tf_butter_ord_2 = sig.TransferFunction( num_butter_ord_2, den_butter_ord_2 )

#-- Frecuencia de corte --
fc = 6e3

#-- Norma de frecuencia --
Omega_omega = fc

#-- Frecuencia de muestreo --
fs10 = 10e3
fs100 = 100e3

#-- Normalización --
fs10  /= Omega_omega
fs100 /= Omega_omega

#-- Kernel de la transformación bilineal --
k_10 = 2*fs10
k_100 = 2*fs100

#-- Coeficientes de denominador de T_HPF(z) --
a2_10 = k_10**2 +k_10*np.sqrt(2) +1
a1_10 = 2 -2*k_10**2
a0_10 = k_10**2  -k_10*np.sqrt(2) +1

a2_100 = k_100**2 +k_100*np.sqrt(2) +1
a1_100 = 2 -2*k_100**2
a0_100 = k_100**2  -k_100*np.sqrt(2) +1


#-- Generación de la T_HPF(z) --
numz10 = k_10**2 * np.array([1, -2, 1])
denz10 =  np.array([a2_10, a1_10, a0_10])

numz100 = k_100**2 * np.array([1, -2, 1])
denz100 =  np.array([a2_100, a1_100, a0_100])

my_df10 = sig.TransferFunction( numz10, denz10, dt = 1/fs10 )
my_df100 = sig.TransferFunction( numz100, denz100, dt = 1/fs100 )


"""
ww, hh = sig.freqz( numz, denz, worN=1000 )
plt.figure(1)
plt.plot( ww, group_delay( ww, np.unwrap( np.angle( hh ) ) ) )
plt.grid( visible = 'True', which = 'both', axis = 'both' )
plt.legend()
plt.show()
"""

#-- Respuestas de módulo, fase, retardo y pzmap
plt.close("all")
analyze_sys(my_tf_butter_ord_2, "HPF Butterworth 2º orden")
analyze_sys(my_df10, "Filtro Digital con fs = 10 kHz")#, fs = fs )
analyze_sys(my_df100, "Filtro Digital con fs = 100 kHz")#, fs = fs )
