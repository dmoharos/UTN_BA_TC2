# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 19:43:30 2023

@author: David
"""

#-------------------------------------------------------------------------------------------------------------------#

# Inicializamos e importamos módulos

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

#-------------------------------------------------------------------------------------------------------------------#

# Importamos las funciones de PyTC2

from pytc2.sistemas_lineales import analyze_sys
from pytc2.sistemas_lineales import pretty_print_bicuad_omegayq
from pytc2.sistemas_lineales import tf2sos_analog
from pytc2.sistemas_lineales import pretty_print_SOS, pretty_print_lti
from pytc2.general import print_subtitle

#-------------------------------------------------------------------------------------------------------------------#

# Calculamos e^2
alfa_max = 1                        # dB
alfa_min = 20                       # dB

f_s_plantilla = 1.2e3               # Hz
f_p_plantilla = 4.6e3               # Hz

omega_p_plantilla = 2*m.pi*f_p_plantilla
norm_w = omega_p_plantilla
omega_p_plantilla /= norm_w
omega_p_pb_prototipo = 1/omega_p_plantilla

omega_s_plantilla = 2*m.pi*f_s_plantilla
omega_s_plantilla /= norm_w
omega_s_pb_prototipo = 1/omega_s_plantilla

print('#---------------------------------------------------------------------------------------------#')
print(' ')
print('-- Datos de plantilla - Filtro pasa altos objetivo --')
print(' ')

print('α_min = {}'.format(alfa_min))
print('α_max = {}'.format(alfa_max))
print('fs = {}'.format(f_s_plantilla))
print('fp = {}'.format(f_p_plantilla))

print(' ')

print('ωp_n = {:3.4f}'.format(omega_p_plantilla))
print('ωs_n = {:3.4f}'.format(omega_s_plantilla))

print(' ')
print('-- Dominio transformado - Filtro pasa bajos prototipo --')
print(' ')

print('ωp = {:3.4f}'.format(omega_p_pb_prototipo))
print('ωs = {:3.4f}'.format(omega_s_pb_prototipo))

print(' ')
print('#---------------------------------------------------------------------------------------------#')
print(' ')
print('-- ε: Grado de libertad de la funcion --')
print(' ')

print('ε = sqrt(10^(α_max/10)-1)')
eps = np.sqrt(10**(alfa_max/10)-1)

print(' ')

print('ε = {:3.4f}'.format(eps))
print('ε^2 = {:3.4f}'.format(eps**2))

print(' ')
print('#---------------------------------------------------------------------------------------------#')

#-------------------------------------------------------------------------------------------------------------------#

# Calculamos N
# Iteramos alfa_min
print(' ')
print('-- N: Orden del filtro --')
print(' ')
print('α_min = 10*log(1 + ε^2*C_n^2) con C_n^2= cosh^2(N*cosh^(-1)(ω_s))')
print(' ')

for N in range(1,10):
    C_nn = (np.cosh(N*(np.arccosh(omega_s_pb_prototipo))))**2
    att = 10*np.log10(1+(eps**2)*C_nn)    
    print('Para N= {:d}: ¿att = {:3.4f} dB >= α_min= {:d}?'.format(N, att, alfa_min))
    if att >= alfa_min:
        break

print(' ')

# Elegimos N de forma tal que α_min >= 20 dB:
print('N= {:d}'.format(N))

print(' ')
print('#---------------------------------------------------------------------------------------------#')

#-------------------------------------------------------------------------------------------------------------------#

# De la resolución analítica, obtenemos |T(jw)|^2:
# En función de eps^2:
num = [0.9826, 0, 0]
den = [1, 0.995, 0.907]


print(' ')
print('-- p_i: Polos en el semiplano izquierdo obtenidos con roots(p) --')
print('-- del polinomio denominador obtenido de forma analítica --')
print(' ')


den_aux= np.array(np.roots(den))
num_p= 0
for i in range(len(np.roots(den))):
    if den_aux[i].real < 0:
        print('p_{:d}= {}'.format(num_p, den_aux[i]))
        num_p+=1

print(' ')
print('#---------------------------------------------------------------------------------------------#')

#-------------------------------------------------------------------------------------------------------------------#

# Obtenemos singularidades con la función de aproximación de Chevyshev del
# filtro pasa bajos prototipo: cheb1ap(N, rp)
z, p, k = sig.cheb1ap(N, alfa_max)

#-------------------------------------------------------------------------------------------------------------------#

# Transformamos las singularidades que nos devuelve cheb1ap(N, rp) para obtener 
# el numerador y el denominador de la T_LP(s) del filtro pasa bajos prototipo 
# con zpk2tf(z,p,k):
num_lp, den_lp = sig.zpk2tf(z,p,k)

#-------------------------------------------------------------------------------------------------------------------#

# Transformamos la T_LP(s) del filtro pasa bajos prototipo para obtener 
# el numerador y el denominador de la T_HP(s) con lp2hp(num, den):
num_hp, den_hp = sig.lp2hp(num_lp, den_lp)

print(' ')
print('-- p_i: Polos en el semiplano izquierdo obtenidos con cheb1ap(N, rp) --')
print('-- coincidentes con los obtenidos con roots(p) de forma analítica --')
print(' ')

print('{}'.format(np.roots(den_hp)))

print(' ')
print('#---------------------------------------------------------------------------------------------#')


#-------------------------------------------------------------------------------------------------------------------#

# Transformamos (factorizamos) la T(s) en secciones de segundo orden (SOS) con la función tf2sos_analog()
#this_sos = tf2sos_analog(num_hp, den_hp)
t_hp= sig.TransferFunction(num_hp, den_hp)
#-------------------------------------------------------------------------------------------------------------------#

# Imprimimos la T(s) en formato T(s)= num/den con la funcion pretty_print_SOS():
print(' ')
print('-- Función transferencia T(s): --')
print(' ')


#pretty_print_SOS(this_sos, mode='omegayq')
pretty_print_lti(num_hp, den_hp)

print(' ')
print('#---------------------------------------------------------------------------------------------#')
print(' ')

#-------------------------------------------------------------------------------------------------------------------#

# Representamos módulo, fase, diagrama de polos y ceros y retardo de fase con la analyze_sys() que tiene, entre
# otras cosas, indicadores (w0 y Q) de las singularidades en el diagrama de polos y ceros


print('-- Módulo, fase, diagrama de polos y ceros y retardo de fase --')
print(' ')

analyze_sys(t_hp, sys_name='Filtro pasa alto Chevyshev 2do orden')

#-------------------------------------------------------------------------------------------------------------------#
