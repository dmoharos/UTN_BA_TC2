# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 12:08:51 2023

@author: David
"""


from scipy import signal as sig
import numpy as np
from pytc2.sistemas_lineales import analyze_sys

#------------------------------------------------------------------------------#

#-- LPF Butterworth 2º orden --
num_butter_ord_2 = [ 1 ]
den_butter_ord_2 = [ 1, np.sqrt(2), 1 ]
my_tf_butter_ord_2 = sig.TransferFunction( num_butter_ord_2, den_butter_ord_2 )

#-- Norma de frecuencia --
fc = 1e3
Omega_omega = fc

#fs = 10e3
fs = 100e3
#-- Normalización --
fs = fs / Omega_omega
#-- Kernel de la transformación bilineal --
k = 2*fs
            
#-- Coeficientes de denominador de T_LPF(z) --
a2 = k**2 +k*np.sqrt(2) +1
a1 = 2 -2*k**2
a0 = k**2  -k*np.sqrt(2) +1

#-- Generación de la T_LPF(z) --
numz = [ 1, 2, 1 ]
denz =  [ a2, a1, a0 ]
my_df = sig.TransferFunction( numz, denz, dt = 1/fs )

#-- Respuestas de módulo, fase, retardo y pzmap
analyze_sys( my_tf_butter_ord_2, "LPF Butterworth 2º orden" )
#analyze_sys( my_df, "Filtro Digital con fs = 10 kHz", fs = fs )
analyze_sys( my_df, "Filtro Digital con fs = 100 kHz", fs = fs )

#------------------------------------------------------------------------------#

"""

#-- HPF Butterworth 2º orden --
num_butter_ord_2 = [ 1, 0, 0 ]
den_butter_ord_2 = [ 1, np.sqrt(2), 1 ]
my_tf_butter_ord_2 = sig.TransferFunction( num_butter_ord_2, den_butter_ord_2 )

#-- Frecuencia de corte --
fc = 6e3

#-- Norma de frecuencia --
Omega_omega = fc

#-- Frecuencia de muestreo --
fs1 = 10e3
fs2 = 100e3

#-- Normalización --
fs1 = fs1 / Omega_omega
fs2 = fs2 / Omega_omega
#-- Kernel de la transformación bilineal --
k1 = 2*fs1
k2 = 2*fs2
          
#-- Coeficientes de denominador de T_HPF(z) --
a21 = k1**2 +k1*np.sqrt(2) +1
a11 = 2 -2*k1**2
a01 = k1**2  -k1*np.sqrt(2) +1

a22 = k2**2 +k2*np.sqrt(2) +1
a12 = 2 -2*k2**2
a02 = k2**2  -k2*np.sqrt(2) +1

#-- Generación de la T_HPF(z) --
numz1 = k1**2*np.array([ 1, -2, 1 ])
denz1 =  np.array([ a21, a11, a01 ])
my_df1 = sig.TransferFunction( numz1, denz1, dt = 1/fs1 )

numz2 = k2**2*np.array([1, -2, 1])
denz2 =  np.array([a22, a12, a02])
my_df2 = sig.TransferFunction( numz2, denz2, dt = 1/fs2 )

#-- Respuestas de módulo, fase, retardo y pzmap
analyze_sys(my_tf_butter_ord_2, "HPF Butterworth 2º orden")
#analyze_sys(my_df1, "Filtro Digital con fs = 10 kHz", fs = fs1 )
analyze_sys(my_df2, "Filtro Digital con fs = 100 kHz", fs = fs2 )

#------------------------------------------------------------------------------#

"""