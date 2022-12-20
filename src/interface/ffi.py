#!/usr/bin/env python
#
# ffi.py
#
# Interface to the Rust back end lib
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

# Import all
from main.imports import *


#=====================================================
# Main model class
#=====================================================
class Interface:
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        
        # Load the library
        self.lib = cdll.LoadLibrary("rustsdrlib.dll")
        
        # Get a handle to all methods
        self.f_init = self.lib.sdrlib_init
        self.f_start = self.lib.sdrlib_run
        self.f_stop = self.lib.sdrlib_close
        self.f_freq = self.lib.sdrlib_freq
        self.f_mode = self.lib.sdrlib_mode
        self.f_filt = self.lib.sdrlib_filter
        self.f_disp = self.lib.sdrlib_disp_data
        
        # Pointer to display data
        self.f_disp.restype = POINTER(c_float)
        self.disp_ptr = POINTER(c_float)

    #=====================================================
    # PUBLIC
    #=====================================================
    def run_lib(self):
        
        #Initialise sets up the context
        self.f_init()
        
        # Start runs the lib main thread which starts everything
        self.f_start()
    
    def close_lib(self):
        # Tidy close lib
        self.f_stop()
        
    #=====================================================
    # Call level interface
    def set_freq(self, freq):
        # Set frequency in Hz
        self.f_freq(freq)
    
    def set_mode(self, mode):
        # Set mode from mode set
        self.f_mode(mode)
        
    def set_filter(self, filt):
        # Set filter from filter set
        self.f_filt(filt)
     
    def get_disp_data(self):
        # Return a pointer to display data
        return f_disp()
        