#!/usr/bin/env python
#
# modes.py
#
# Modes class for SDRLibEConnector server
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
# Modes provides a button panel for the available modes
#==============================================================================================

#=====================================================
# Modes main class
#===================================================== 
class Modes(ButtonBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self, id):
        """
        Constructor
        
        Arguments:  
            
        """
        super(Modes, self).__init__()
        
        # radio id
        self.__id = id
        
        # Get the connector instance
        self.__con = getInstance('interface_inst')
        
        # Add mode buttons
        self.__btns = (
            # btn(label), row, col, id 
            (QPushButton(mode_lookup[CH_LSB][1], self), 0, 0, CH_LSB),
            (QPushButton(mode_lookup[CH_USB][1], self), 0, 1, CH_USB),
            (QPushButton(mode_lookup[CH_DSB][1], self), 0, 2, CH_DSB),
            (QPushButton(mode_lookup[CH_CWL][1], self), 1, 0, CH_CWL),
            (QPushButton(mode_lookup[CH_CWU][1], self), 1, 1, CH_CWU),
            (QPushButton(mode_lookup[CH_FM][1], self), 1, 2, CH_FM),
            (QPushButton(mode_lookup[CH_AM][1], self), 2, 0, CH_AM),
            (QPushButton(mode_lookup[CH_DIGU][1], self), 2, 1, CH_DIGU),
            (QPushButton(mode_lookup[CH_SPEC][1], self), 2, 2, CH_SPEC),
            (QPushButton(mode_lookup[CH_DIGL][1], self), 3, 0, CH_DIGL),
            (QPushButton(mode_lookup[CH_SAM][1], self), 3,  1, CH_SAM),
            (QPushButton(mode_lookup[CH_DRM][1], self), 3, 2, CH_DRM),
        )
        for btn in self.__btns:
           self.add_button(btn[0], btn[1], btn[2], btn[3])
        
        # Connect click event
        self.btn_grp.buttonClicked.connect(self.__mode_evnt)
        
        # Get radio model
        self.__radio_model = Model.get_radio_model()
    
    #==============================================================================================
    # PUBLIC
    #==============================================================================================
    
    #-------------------------------------------------
    # Set context according to id
    def set_context(self, callback, x, y, direction):
        # Call base mathod
        self.set_base_context(callback, x, y, direction,self.__id)
        # Select the appropriate button
        button = self.btn_grp.button(self.__radio_model[self.__id]['MODE'])
        # Does not cause a click event
        button.setChecked(True)
        
    #==============================================================================================
    # PRIVATE
    #==============================================================================================
        
    #-------------------------------------------------
    # Button group click event
    def __mode_evnt(self, btn) :
        """
        Any button click event
        
        Arguments:  
            btn --  the QButton
            
        """
        if self.direction == CH_RX:
            # Execute mode change
            mode_id = self.btn_grp.id(btn)
            #self.__con.set_rx_mode(self.__id, mode_id)
            self.__con.set_mode(mode_id)
            # Tell parent what was selected
            self.callback(btn.text())
            # Update the model
            self.__radio_model[self.__id]['MODE'] = mode_id
            # Its a popup
            self.close()
        