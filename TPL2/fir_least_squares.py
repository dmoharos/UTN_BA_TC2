# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 12:27:45 2023

@author: David
"""

#------------------------------------------------------------------------------

#import sympy as sp
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
#from scipy.signal.windows import hamming, kaiser, blackmanharris
from pytc2.sistemas_lineales import plot_plantilla, group_delay

#------------------------------------------------------------------------------

def plot_freq_resp_fir(this_num, this_desc):

    wrad, hh = sig.freqz(this_num, 1.0)
    ww = wrad / np.pi
    
    plt.figure(1)

    plt.plot(ww, 20 * np.log10(abs(hh)), label=this_desc)

    plt.title('FIR designed by window method - Taps:' + str(cant_coef) )
    plt.xlabel('Frequencia normalizada')
    plt.ylabel('Modulo [dB]')
    plt.grid(which='both', axis='both')

    axes_hdl = plt.gca()
    axes_hdl.legend()
    
    plt.figure(2)

    phase = np.unwrap(np.angle(hh))

    plt.plot(ww, phase, label=this_desc)

    plt.title('FIR designed by window method - Taps:' + str(cant_coef))
    plt.xlabel('Frequencia normalizada')
    plt.ylabel('Fase [rad]')
    plt.grid(which='both', axis='both')

    axes_hdl = plt.gca()
    axes_hdl.legend()

    plt.figure(3)

    # ojo al escalar Omega y luego calcular la derivada.
    gd_win = group_delay(wrad, phase)

    plt.plot(ww, gd_win, label=this_desc)

    plt.ylim((np.min(gd_win[2:-2])-1, np.max(gd_win[2:-2])+1))
    plt.title('FIR diseñado por métodos directos - Taps:' + str(cant_coef))
    plt.xlabel('Frequencia normalizada')
    plt.ylabel('Retardo [# muestras]')
    plt.grid(which='both', axis='both')

    axes_hdl = plt.gca()
    axes_hdl.legend()    

#------------------------------------------------------------------------------

# Marginalmente muestreado:
# fs = 2*f_Nyquist = 44 kHz
f_Nyquist = 22e3

fs_plantilla = 2*f_Nyquist 
fpass1_plantilla = 2e3         # fpass_plantilla = 2 kHz
fstop1_plantilla = 4e3         # fstop_plantilla = 4 kHz
fstop2_plantilla = 6e3         # fstop_plantilla = 6 kHz
fpass2_plantilla = 8e3         # fpass_plantilla = 8 kHz

# Normalizamos por Nyquist
Omega_omega = f_Nyquist
fs          = fs_plantilla / Omega_omega
fpass1      = fpass1_plantilla / Omega_omega
fstop1      = fstop1_plantilla / Omega_omega
fpass2      = fpass2_plantilla / Omega_omega
fstop2      = fstop2_plantilla / Omega_omega

att_pass = 1                             # alpha_fpass = 1 dB
att_stop = 20                            # alpha_fstop = 20 dB

#-- Tamaño de la respuesta al impulso --
cant_coef   = 87


#-- Tipo de filtro --
filter_type = 'bandstop'


#-- Plantilla de requerimientos --
frecs = [ 0.0, fpass1   , fstop1   , fstop2   , fpass2   , 1.0 ]
gains = [ 0  , -att_pass, -att_stop, -att_stop, -att_pass, 0 ]     # dB

gains = 10**(np.array(gains)/20)


#-- Diseñamos los filtros --
#num_bh    = sig.firwin2( cant_coef, frecs, gains, window='blackmanharris' )
#num_hm    = sig.firwin2( cant_coef, frecs, gains, window='hamming' )
#num_ka    = sig.firwin2( cant_coef, frecs, gains, window=('kaiser',14) )
num_firls = sig.firls( cant_coef, frecs, gains, fs=fs )
#num_remez = sig.remez( cant_coef, frecs, gains[::2], fs=fs )
den = 1.0

#_,  hh_firls   = sig.freqz( num_bh,    den )
#_,  hh_firls   = sig.freqz( num_hm,    den )
#_,  hh_firls   = sig.freqz( num_ka,    den )
ww_rad, hh_win = sig.freqz( num_firls, den )
#_,  hh_remez   = sig.freqz( num_remez, den )

#plot_freq_resp_fir( num_bh, filter_type+ '-blackmanharris' )    
#plot_freq_resp_fir( num_hm, filter_type+ '-hamming' )    
#plot_freq_resp_fir( num_ka, filter_type+ '-kaiser-b14' )
plot_freq_resp_fir( num_firls, filter_type + '-firls' )
#plot_freq_resp_fir( num_remez, filter_type + '-remez' )


#-- Superponemos la plantilla del filtro requerido para mejorar 
#-- la visualización --
plt.figure(1)    
plot_plantilla( filter_type = filter_type,
                fpass       = [fpass1, fpass2], 
                ripple      = att_pass,
                fstop       = [fstop1, fstop2], 
                attenuation = att_stop,
                fs          = fs               )
axes_hdl = plt.gca()
axes_hdl.legend()


#-- Reordenamos las figuras en el orden habitual: 
#-- módulo-fase-retardo --
plt.figure(2)    
axes_hdl = plt.gca()
axes_hdl.legend()

plt.figure(3)    
axes_hdl = plt.gca()
axes_hdl.legend()

plt.show()

#------------------------------------------------------------------------------