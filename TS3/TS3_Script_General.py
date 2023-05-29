# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:42:03 2023

@author: David
"""

#----------------------------------------------------------------------#

# Inicialización e importación de módulos

# Módulos externos
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math as m
import scipy.signal as sig

fig_sz_x = 10
fig_sz_y = 9
fig_dpi = 150 # dpi

fig_font_size = 12

mpl.rcParams['figure.figsize'] = (fig_sz_x, fig_sz_y)
mpl.rcParams['figure.dpi'] = fig_dpi
#plt.rcParams.update({'font.size':fig_font_size})

#----------------------------------------------------------------------#

# Importación de las funciones de PyTC2

from pytc2.sistemas_lineales import analyze_sys
from pytc2.sistemas_lineales import pretty_print_bicuad_omegayq
from pytc2.sistemas_lineales import tf2sos_analog
from pytc2.sistemas_lineales import pretty_print_SOS
from pytc2.general import print_subtitle

"""
#----------------------------------------------------------------------#

## Cálculo de e^2 y N

alfa_max = 1    # dB
alfa_min = 12   # dB
omega_p = 1     # norm omega_p
omega_s = 2     # norm omega_s

eps = np.sqrt(10**(alfa_max/10)-1)

print('eps = {:3.3f}  -  eps**2 = {:3.3f}'.format(eps, eps**2))

for N in range(1,9):
    att = 10 * np.log10(1 + eps**2*omega_s**(2*N))     
    print('alpha_{:d} = {:3.3f} dB'.format(N,att))

num = [1]
den = [-16*eps**2, 0, -24*eps**2, 0, -9*eps**2, 0, 1]

# a = 1/(16*eps**2)
# b = 3/2
# c = 9/16

# num = [a]
# den = [-1, 0, -b, 0, -c, 0, a]

print(np.roots(den))

# z,p,k = sig.cheb1ap(this_order, this_ripple)

z,p,k = sig.cheb1ap(3, alfa_max)

num, den = sig.zpk2tf(z,p,k)

this_sos = tf2sos_analog(num, den)

pretty_print_SOS(this_sos)

analyze_sys(this_sos)
    
"""

alfa_max = 0.4  # dB
alfa_min = 48   # dB
omega_p = 1     # norm omega_p
omega_s = 3     # norm omega_s

eps = np.sqrt(10**(alfa_max/10)-1)

print('eps = {:3.3f}  -  eps**2 = {:3.3f}'.format(eps, eps**2))

for N in range(1,9):
    C_nn = (np.cosh(N*(np.arccosh(omega_s))))**2
    att = 10*np.log10(1+(eps**2)*C_nn)    
    print('alpha_{:d} = {:3.3f} dB'.format(N,att))

# num = [1]
# den = [-16*eps**2, 0, -24*eps**2, 0, -9*eps**2, 0, 1]

# a = 1/(16*eps**2)
# b = 3/2
# c = 9/16

# num = [a]
# den = [-1, 0, -b, 0, -c, 0, a]

# print(np.roots(den))
    
"""
k = 256*eps**2
a = 640*eps**2/k
b = 560*eps**2/k  
c = 200*eps**2/k    
d = 25*eps**2/k
e = 1/k

num = [e]
den = [1, 0, -a, 0, b, 0, -c, 0, d, 0, e]  
print(np.roots(den))   
this_sos = tf2sos_analog(num, den)
pretty_print_SOS(this_sos)
"""

z,p,k = sig.cheb1ap(5, alfa_max)
num, den = sig.zpk2tf(z,p,k)
this_sos = tf2sos_analog(num, den)
#pretty_print_SOS(this_sos)
analyze_sys(this_sos)
    
    