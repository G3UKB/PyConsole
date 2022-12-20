#!/usr/bin/env python
#
# defs.py
#
# All common definitions for PyConsole
# 
# Copyright (C) 2022 by G3UKB Bob Cowdery
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#    
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#    
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    
#  The author can be reached by email at:   
#     bob@bobcowdery.plus.com
#

#=====================================================
# Radios
RX_1 = 1

#=====================================================
# Channel type
CH_RX = 0
CH_TX = 1
CH_MON = 2

#=====================================================
# Frequency
MIN_FREQ = 0.1
MAX_FREQ = 60.0
VFO_UP = 0
VFO_DOWN = 1

#=====================================================
# RX modes
CH_LSB = 0
CH_USB = 1
CH_DSB = 2
CH_CWL = 3
CH_CWU = 4
CH_FM = 5
CH_AM = 6
CH_DIGU = 7
CH_SPEC = 8
CH_DIGL = 9
CH_SAM = 10
CH_DRM = 11

mode_lookup = (
    (CH_LSB, 'LSB'),
    (CH_USB, 'USB'),
    (CH_DSB, 'DSB'),
    (CH_CWL, 'CW-L'),
    (CH_CWU, 'CW-U'),
    (CH_FM, 'FM'),
    (CH_AM, 'AM'),
    (CH_DIGU, 'DIG-U'),
    (CH_SPEC, 'SPEC'),
    (CH_DIGL, 'DIG-L'),
    (CH_SAM, 'SAM'),
    (CH_DRM, 'DRM'),
)

#=====================================================
# RX filter
CH_BP_OFF = 0
CH_BP_ON = 1
CH_BP_WIN_4_TERM = 0
H_BP_WIN_7_TERM = 1

# Filters
CH_6K0 = 0
CH_4K0 = 1
CH_2K7 = 2
CH_2K4 = 3
CH_2K1 = 4
CH_1K0 = 5
CH_500 = 6
CH_250 = 7
CH_100 = 8

filter_lookup = (
    (CH_6K0, 100, 6100, '6.0 KHz'),
    (CH_4K0, 100, 4100, '4.0 KHz'),
    (CH_2K7, 300, 3000, '2.7 KHz'),
    (CH_2K4, 300, 2700, '2.4 KHz'),
    (CH_2K1, 300, 2400, '2.1 KHz'),
    (CH_1K0, 300, 1300, '1.0 KHz'),
    (CH_500, 500, 1000, '500 Hz'),
    (CH_250, 600, 850, '250 Hz'),
    (CH_100, 700, 800, '100 Hz')
)

#=====================================================
# AGC mode
CH_AGC_OFF = 0
CH_AGC_LONG = 1
CH_AGC_SLOW = 2
CH_AGC_MED = 3
CH_AGC_FAST = 4

agc_lookup = (
    (CH_AGC_OFF, 'OFF'),
    (CH_AGC_LONG, 'LONG'),
    (CH_AGC_SLOW, 'SLOW'),
    (CH_AGC_MED, 'MED'),
    (CH_AGC_FAST, 'FAST')       
)

#=====================================================
# Displays
IDLE_TICKER = 100
