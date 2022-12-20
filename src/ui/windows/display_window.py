#!/usr/bin/env python
#
# display_window.py
#
# Single window for graphical displays
# 
# Copyright (C) 2020 by G3UKB Bob Cowdery
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
# Display window class for SDRLibEConsole
#==============================================================================================

class DisplayWindow(QMainWindow):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self, title, rx_id ):
        
        super(DisplayWindow, self).__init__()
        
        # The id is RX_1 to RX_3
        self.__rx_id = rx_id
        
        # Set temp dims
        self.__width = 400
        self.__height = 200
        
        #-------------------------------------------------
        # Get instances
        
        #-------------------------------------------------
        # Set title
        self.setWindowTitle(title)
        # Set the back colour
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(59,59,59,255))
        self.setPalette(palette)
        # Temp set a size
        self.setGeometry(100,100,self.__width, self.__height)
        
        # Temp for RX1
        self.__display_inst = Panadapter(1, self.__width, self.__height, self.freq_callback)
        
        self.__setup_ui()
        #-------------------------------------------------
        # Get app model
        #self.__app_model = Model.get_app_model()
        
        # Set window metrics
        #metrics = Model.get_app_model()['METRICS']
        #if id in metrics:
        #    self.setGeometry(metrics[id][0], metrics[id][1], metrics[id][2], metrics[id][3])
        
        # Get radio model
        #self.__radio_model = Model.get_radio_model()
     
    # Temp until real callback
    def freq_callback(self, f):
        print(f)
    
    #==============================================================================================
    # PUBLIC
    #==============================================================================================
    
    #-------------------------------------------------
    # Window metrics
    #-------------------------------------------------
    
    #-------------------------------------------------
    # Save window metrics
    #def saveMetrics(self):
    #    Model.get_app_model()['METRICS'][self.__id] = [self.x(),self.y(),self.width(),self.height()]
        
    #==============================================================================================
    # OVERRIDES
    #==============================================================================================
    
    #==============================================================================================
    # EVENTS
    #==============================================================================================

    #==============================================================================================
    # PRIVATE
    #==============================================================================================
    # Setup UI contents
    def __setup_ui(self) :
        
        # Set the display in the window
        self.setCentralWidget(self.__display_inst)

    