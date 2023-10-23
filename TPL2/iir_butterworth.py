# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:36:21 2023

@author: David
"""

#------------------------------------------------------------------------------

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
from pytc2.sistemas_lineales import plot_plantilla

#------------------------------------------------------------------------------        

# Tipo de aproximación.
aprox_name = 'butter'

# Requerimientos de plantilla
filter_type = 'lowpass'

# Plantillas normalizadas a Nyquist y en dB
# Marginalmente muestreado:
# fs = 2*f_Nyquist = 44 kHz
f_Nyquist = 22e3

fs_plantilla = 2*f_Nyquist 
fpass_plantilla = 1e3         # fpass_plantilla = 1 kHz
fstop_plantilla = 6e3         # fstop_plantilla = 2 kHz

Omega_omega = f_Nyquist
fs          = fs_plantilla / Omega_omega
fpass       = fpass_plantilla / Omega_omega
fstop       = fstop_plantilla / Omega_omega

ripple      = 1               # alpha_max_plantilla = 1 dB
attenuation = 20              # alpha_min_plantilla = 20 dB


# Variables 
all_sys = []
analog_filters = []
digital_filters = []

filter_names = []
analog_filters_names = []
digital_filters_names = []


# Cálculo del filtro
order, wcutof   = sig.buttord( 2*np.pi*fpass*fs/2,
                               2*np.pi*fstop*fs/2, 
                               ripple, 
                               attenuation, 
                               analog = True      )

orderz, wcutofz = sig.buttord( fpass, 
                               fstop,
                               ripple,
                               attenuation,
                               analog = False )


# Diseño del filtro analógico
num, den = sig.iirfilter( order, 
                          wcutof, 
                          rp = ripple, 
                          rs = attenuation, 
                          btype = filter_type, 
                          analog = True, 
                          ftype = aprox_name  )

my_analog_filter = sig.TransferFunction( num, den )
my_analog_filter_desc = aprox_name + '_ord_' + str( order ) + '_analog'

all_sys.append( my_analog_filter )
filter_names.append( my_analog_filter_desc )


# Diseño del filtro digital
numz, denz = sig.iirfilter( orderz, 
                            wcutofz, 
                            rp = ripple, 
                            rs = attenuation, 
                            btype = filter_type, 
                            analog = False,
                            ftype = aprox_name  )

my_digital_filter = sig.TransferFunction( numz, denz, dt = 1/fs )
my_digital_filter_desc = aprox_name + '_ord_' + str( orderz ) + '_digital'

all_sys.append( my_digital_filter )
filter_names.append( my_digital_filter_desc )


# Plantilla de diseño
plt.figure(1)
plt.cla()

npoints = 1000
w_nyq = 2*np.pi*fs/2

w, mag, _ = my_analog_filter.bode( npoints )
plt.plot( w/w_nyq, mag, label = my_analog_filter_desc )

w, mag, _ = my_digital_filter.bode( npoints )  
plt.plot( w/w_nyq, mag, label = my_digital_filter_desc ) 

plt.title( 'Plantilla de diseño' )
plt.xlabel( 'Frecuencia normalizada a Nyq [#]' )
plt.ylabel( 'Amplitud [dB]' )
plt.grid( which = 'both', axis = 'both')

plt.gca().set_xlim([0, 1])

plot_plantilla( filter_type = filter_type,
                fpass       = fpass, 
                ripple      = ripple,
                fstop       = fstop,
                attenuation = attenuation, 
                fs          = fs          )

