#---------------------------------------------------------------------#

import numpy as np
import scipy.signal as sig
from pytc2.sistemas_lineales import analyze_sys, pretty_print_lti

#---------------------------------------------------------------------#

"""
num_T_lpn_fa= [1, 0, 9]
den_T_lpn_fa= [1, 1, 1]

T_lpn_fa= sig.TransferFunction(num_T_lpn_fa, den_T_lpn_fa)

pretty_print_lti(T_lpn_fa)
analyze_sys( T_lpn_fa, 'LowPass Notch Filter Order 2' )
"""

#---------------------------------------------------------------------#

"""
num_T_lpn_sa= [1/9, 0, 1]
den_T_lpn_sa= [1, 1, 1]

T_lpn_sa= sig.TransferFunction(num_T_lpn_sa, den_T_lpn_sa)

pretty_print_lti(T_lpn_sa)
analyze_sys( T_lpn_sa, 'LowPass Notch Filter Order 2' )
"""

#---------------------------------------------------------------------#

"""
num_T_lpn_ta= [1/9, 0, 1]
den_T_lpn_ta= np.polymul([1, 1, 1],[1, 1])

T_lpn_ta= sig.TransferFunction(num_T_lpn_ta, den_T_lpn_ta)

pretty_print_lti(T_lpn_ta)
analyze_sys( T_lpn_ta, 'LowPass Notch Filter Order 3' )
"""

#---------------------------------------------------------------------#

num_T_hpn= np.polymul([1, 0, 1/9],[1, 0])
den_T_hpn= np.polymul([1, 1, 1],[1, 1])

T_hpn = sig.TransferFunction(num_T_hpn, den_T_hpn)

pretty_print_lti(T_hpn)
analyze_sys( T_hpn, 'HighPass Notch Filter Order 3' )

#---------------------------------------------------------------------#