#!/usr/bin/env python
#
# button_base.py
#
# Base class for button groups for modes, filters etc
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
# Provides a base for popup button panels
#==============================================================================================

#=====================================================
# Button base main class
#===================================================== 
class ButtonBase(QWidget):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        """
        Constructor
        
        Arguments:  
            
        """
        
        super(ButtonBase, self).__init__()
        
        # Set the back colour
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(41,41,41,255))
        self.setPalette(palette)
        self.setWindowFlags(
            Qt.CustomizeWindowHint |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setWindowOpacity(0.97)
        
        # Set the layout
        self.__grid = QGridLayout()
        #self.__grid.setSpacing(0)
        margins = QMargins()
        margins.setLeft = 0
        margins.setRight = 0
        margins.setTop = 0
        margins.setBottom = 0
        self.__grid.setContentsMargins(margins)
        self.setLayout(self.__grid)
        
        # Create an exclusive button group
        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
    
    #==============================================================================================
    # PUBLIC
    #==============================================================================================
    
    #-------------------------------------------------
    # Set context   
    def set_base_context(self, callback, x, y, direction, id):
        """
        Set Context
        
        Arguments:  
            callback    --  callback here with mode string
            x           --  x coord of main window
            y           --  y coord of main window
            direction   --  RX or TX
            id          --  the id of this instantiation (radio id)
            
        """
        self.callback = callback
        self.direction = direction
        # Position at top right corner of invoking button
        self.id = id
        self.move( x, y)
    
    #==============================================================================================
    # PRIVATE
    #==============================================================================================
        
    #-------------------------------------------------
    # Add a button to the grid   
    def add_button(self, btn, row, col, id):
        """
        Add button to grid
        
        Arguments:  
            btn --  the QButton
            row --  grid row
            col --  grid col
            id  --  id to give button
            
        """
        btn.setCheckable(True)
        btn.setStyleSheet("QPushButton {background-color: rgb(59,59,59); color: rgb(148,148,148); font: bold 10px;} QPushButton:checked {background-color: rgb(98,98,98);}")
        self.__grid.addWidget(btn, row, col)
        self.btn_grp.addButton(btn)
        self.btn_grp.setId(btn, id)
    
    
        