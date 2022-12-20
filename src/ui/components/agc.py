#!/usr/bin/env python
#
# agc.py
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
# AGC provides a button panel for the available modes
#==============================================================================================

#=====================================================
# AGC main class
#===================================================== 
class AGC(ButtonBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self, id):
        """
        Constructor
        
        Arguments:  
            
        """
        super(AGC, self).__init__()
        
        # radio id
        self.__id = id
        
        # Get the connector instance
        self.__con = getInstance('conn_inst')
        
        # Add mode buttons
        self.__btns = (
            # btn(label), row, col, id 
            (QPushButton(agc_lookup[CH_AGC_OFF][1], self), 0, 0, CH_AGC_OFF),
            (QPushButton(agc_lookup[CH_AGC_LONG][1], self), 0, 1, CH_AGC_LONG),
            (QPushButton(agc_lookup[CH_AGC_SLOW][1], self), 0, 2, CH_AGC_SLOW),
            (QPushButton(agc_lookup[CH_AGC_MED][1], self), 1, 0, CH_AGC_MED),
            (QPushButton(agc_lookup[CH_AGC_FAST][1], self), 1, 1, CH_AGC_FAST),
        )
        for btn in self.__btns:
           self.add_button(btn[0], btn[1], btn[2], btn[3])
        
        # Connect click event
        self.btn_grp.buttonClicked.connect(self.__agc_evnt)
        
        # Get radio model
        self.__radio_model = Model.get_radio_model()
    
    #==============================================================================================
    # PUBLIC
    #==============================================================================================
    
    #-------------------------------------------------
    # Set context according to id
    def set_context(self, callback, x, y, direction):
        # Call base mathod
        self.set_base_context(callback, x, y, direction, self.__id)
        # Select the appropriate button
        button = self.btn_grp.button(self.__radio_model[self.__id]['AGC'])
        # Does not cause a click event
        button.setChecked(True)
        
    #==============================================================================================
    # PRIVATE
    #==============================================================================================
        
    #-------------------------------------------------
    # Button group click event
    def __agc_evnt(self, btn) :
        """
        Any button click event
        
        Arguments:  
            btn --  the QButton
            
        """
        if self.direction == CH_RX:
            # Execute AGC change
            agc_id = self.btn_grp.id(btn)
            self.__con.set_agc(self.__id, agc_id)
            # Tell parent what was selected
            self.callback(btn.text())
            # Update the model
            self.__radio_model[self.__id]['AGC'] = agc_id
            # Its a popup
            self.close()
        