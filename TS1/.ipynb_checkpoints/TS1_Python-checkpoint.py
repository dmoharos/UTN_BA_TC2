#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:50:21 2023

@author: David
"""

from scipy.signal import TransferFunction
import matplotlib.pyplot as plt
import numpy as np


from pytc2.sistemas_lineales import pzmap, GroupDelay, bodePlot

w0 = 1
D= 1
qq = np.sqrt(2)/2

my_tf = TransferFunction( [1, -D], [1, 1] )


plt.close('all')

bodePlot(my_tf, fig_id=1, filter_description = 'Q={:3.3f}'.format(qq) )

pzmap(my_tf, fig_id=2, filter_description = 'Q={:3.3f}'.format(qq)) #S plane pole/zero plot

#GroupDelay(my_tf, fig_id=3, filter_description = 'Q={:3.3f}'.format(qq))