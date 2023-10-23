# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 21:17:14 2023

@author: David
"""

from scipy import signal as sig
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from pytc2.sistemas_lineales import group_delay, pzmap

#-- Cuantos más 0's agrego, mayor cantidad de medios ciclos de seno
#-- aparecen comprimidos en el ancho de banda.
#-- Recordar la simetría respecto a la cantidad de muestras
#num = np.array([1,0,0,0,0,0,0,0,0,0,-1])


#-------------------------------------------------------------------

#03.a.1
#num = np.array( [1, 1] )
#den = np.array( [1, 0] )

#03.a.2
#num = np.array( [1, 1, 1] )
#den = np.array( [1, 0, 0] )

#03.b.1
num_1 = np.array( [1, -1] )
den_1 = np.array( [1, 0] )

#03.b.2
num_2 = np.array( [1, 0, -1] )
den_2 = np.array( [1, 0, 0] )


wrad1, hh1 = sig.freqz( num_1, den_1, worN=1000 )
wrad2, hh2 = sig.freqz( num_2, den_2, worN=1000 )
#-- Normalizamos por pi rad --
ww1 = wrad1 / np.pi
ww2 = wrad2 / np.pi
#-- Normalizamos por Nyquist --
fs = 2

plt.close( 'all' )



#-- Diagrama de polos y ceros --

#pzmap( sig.TransferFunction( num, den, dt = 1/fs ) )


#-- Respuesta de modulo --

plt.figure(1)

abs_value1 = abs( hh1 )
#abs_value1 = 20 * np.log10( abs( hh1 ) )
plt.plot( ww1, abs_value1, label = '$|H_1(\Omega)|$')
abs_value2 = abs( hh2 )
#abs_value2 = 20 * np.log10( abs( hh2 ) )
plt.plot( ww2, abs_value2,  label = '$|H_2(\Omega)|$')

ww3 = np.linspace(0, 1, 1000)
hh3 = ww3 * np.pi
plt.plot( ww3, hh3,  label = '$|H_3(\Omega)|_{derivador-ideal}$' )

Omega = sp.symbols('\Omega')

Omega_h13 = sp.nsolve( sp.sin( Omega / 2 ) -0.475*Omega, Omega, 1 ) / np.pi
Omega_h23 = sp.nsolve( sp.sin( Omega ) -0.475*Omega, Omega, 1 ) / np.pi

hh_31 = Omega_h13 * np.pi
hh_32 = Omega_h23 * np.pi

hh_13 = 2 * np.sin( float(Omega_h13) * np.pi/ 2 )
hh_23 = 2 * np.sin( float(Omega_h23) * np.pi )

plt.plot(Omega_h13, hh_31, 'x', color='red', ms=5)
plt.plot(Omega_h13, hh_13, 'x', color='red', ms=5)

plt.plot(Omega_h23, hh_32, 'x', color='red', ms=5)
plt.plot(Omega_h23, hh_23, 'x', color='red', ms=5)


plt.title( 'Magnitude response' )
plt.xlabel( 'Normalized angular frequency []' )
plt.ylabel( 'Magnitude [dB]' )
plt.grid( which = 'both', axis = 'both' )
plt.legend()
plt.show()


error_1 = []
error_2 = []
i = 0
for hh in hh3:
    if hh != 0:
        error_1.append( ( hh - abs_value1[i] ) / hh * 100)
        error_2.append( ( hh - abs_value2[i] ) / hh * 100)
        i+= 1
    else:
        error_1.append(0)
        error_2.append(0)
        i+= 1

def find_nearest( array, target = 5 ):
    return min( array, key = lambda x: abs(x - target) )

plt.figure(2)
#plt.plot( ww1, abs_value1, label = '$|H_1(\Omega)|$')
#plt.plot( ww3, hh3,  label = '$|H_3(\Omega)|_{derivador-ideal}$' )
plt.plot(ww1, error_1, label = 'Error derivador 1° orden')
plt.plot(ww2, error_2, label = 'Error derivador 2° orden')

ww_error_1 = 0
ww_error_2 = 0
hh_error_1 = 0
hh_error_2 = 0 
j = 0
for ww in ww1:
    if error_1[j] <= 5:
        ww_error_1 = ww
        hh_error_1 = error_1[j]
    if error_2[j] <= 5:
        ww_error_2 = ww
        hh_error_2= error_2[j]
    j+= 1
    
plt.plot(ww_error_1, hh_error_1, 'x', color='red', ms=5)
plt.plot(ww_error_2, hh_error_2, 'x', color='red', ms=5)

plt.grid( which = 'both', axis = 'both' )
plt.legend()
plt.show()

"""
#-- Respuesta de fase --

plt.figure(3)

phase_value = np.unwrap( np.angle( hh ) )
plt.plot( ww, phase_value )

plt.title('Phase response')
plt.xlabel('Normalized angular frecuency []')
plt.ylabel('Phase [rad]')
plt.grid( which = 'both', axis = 'both')
plt.show()



#-- Respuesta de retardo de fase --

plt.figure(4)
gd_value = group_delay( wrad, phase_value )
plt.plot( ww, gd_value )

#plt.ylim( np.min(gd_value) -1, np.max(gd_value) +1 )
plt.title( 'Group delay response' )
plt.xlabel( 'Normalized angular frecuency []' )
plt.ylabel( 'Group delay [sec]' )
plt.grid( which='both', axis='both' )
plt.show()
"""


