# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 12:08:51 2023

@author: David
"""


from scipy import signal as sig
#import matplotlib.pyplot as plt
import numpy as np
from pytc2.sistemas_lineales import analyze_sys


#-- LPF Butterworth 2º orden --
num_butter_ord_2 = [ 1 ]
den_butter_ord_2 = [ 1, np.sqrt(2), 1 ]
my_tf_butter_ord_2 = sig.TransferFunction( num_butter_ord_2, den_butter_ord_2 )

#-- Norma de frecuencia --
fc = 1e3
Omega_omega = fc

fs = 10e3
#-- Normalización --
fs = fs / Omega_omega
#-- Kernel de la transformación bilineal --
k = 2*fs
            
#-- Coeficientes de denominador de T_LPF(z) --
a2 = k**2 +k*np.sqrt(2) +1
a1 = 2 -2*k**2
a0 = k**2  -k*np.sqrt(2) +1

#-- Generación de la T_LPF(z) --
numz = [1, 2, 1]
denz =  [a2, a1, a0]
my_df = sig.TransferFunction( numz, denz, dt = 1/fs )

#-- Respuestas de módulo, fase, retardo y pzmap
analyze_sys(my_tf_butter_ord_2, "LPF Butterworth 2º orden", fs = fs )
analyze_sys(my_df, "Filtro DIgital con fs = 10 kHz", fs = fs )