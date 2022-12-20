#!/usr/bin/env python
#
# aux_wimndow.py
#
# Auxiliary windows for the SDRLibEConsole application
# 
# Copyright (C) 2019 by G3UKB Bob Cowdery
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

#==============================================================================================
# Auxiliary windows for SDRLibEConsole
#==============================================================================================

#=====================================================
# Aux window class
# The aux windows run RX2/3/TX and potentially any other windows.
#=====================================================
class AuxWindow(WindowBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self, title, type, id):
        
        WindowBase.__init__(self, title, id)
        
        #-------------------------------------------------
        # Set main panel and grid
        panel = QWidget()
        self.setCentralWidget(panel)
        main_grid = QGridLayout()
        panel.setLayout(main_grid)
        
        #-------------------------------------------------
        # Populate
        self.setup_ui(main_grid)
    
    #==============================================================================================
    # EVENTS
    #==============================================================================================
    
    #-------------------------------------------------
    # Exit button event
    def closeEvent(self, win) :
       self.close()
         
    #==============================================================================================
    # PRIVATE
    #==============================================================================================
    

    