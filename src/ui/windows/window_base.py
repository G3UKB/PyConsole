#!/usr/bin/env python
#
# window_base.py
#
# Base class for top level windows
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
# Base window class for SDRLibEConsole
#==============================================================================================

#=====================================================
# Base window class
# The base class for receiver and tansmitter windows
#=====================================================
class WindowBase(QMainWindow):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self, title, id ):
        
        super(WindowBase, self).__init__()
        
        # The id is RX_1 to RX_3 or TX_1
        self.__id = id
        
        #-------------------------------------------------
        # Get instances
        # TDB These need to be for each instance
        self.con = getInstance('interface_inst')
        self.mode_win = getInstance('mode_win')
        self.filter_win = getInstance('filter_win')
        self.agc_win = getInstance('agc_win')
        self.audio_win = getInstance('audio_win')
        
        #-------------------------------------------------
        # Set title
        self.setWindowTitle(title)
        # Set the back colour
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(59,59,59,255))
        self.setPalette(palette)
        
        #-------------------------------------------------
        # Get app model
        self.__app_model = Model.get_app_model()
        
        # Set window metrics
        metrics = Model.get_app_model()['METRICS']
        if id in metrics:
            self.setGeometry(metrics[id][0], metrics[id][1], metrics[id][2], metrics[id][3])
        
        # Get radio model
        self.__radio_model = Model.get_radio_model()
        
    #-------------------------------------------------
    # Setup UI contents
    def setup_ui(self, main_grid) :
        
        # Right side button grid
        # Note add the grid directly as a layout not in a panel else space cannot be removed
        self.__side_grid = QGridLayout()
        main_grid.addLayout(self.__side_grid, 0, 1)
        self.__side_grid.setSpacing(0)
        margins = QMargins()
        margins.setLeft = 0
        margins.setRight = 0
        margins.setTop = 0
        margins.setBottom = 0
        self.__side_grid.setContentsMargins(margins)
        
        #-------------------------------------------------
        # Right side buttons
        # Mode button
        self.mode_btn = QPushButton('Mode>', self)
        self.__set_button(self.__side_grid, self.mode_btn, 0, 0, self.__mode_evnt, mode_lookup[self.__radio_model[1]['MODE']][1], 1)
        # Filter button
        self.filter_btn = QPushButton('Filter>', self)
        self.__set_button(self.__side_grid, self.filter_btn, 1, 0, self.__filter_evnt, filter_lookup[self.__radio_model[1]['FILTER']][3], 1)
        # AGC button
        self.agc_btn = QPushButton('AGC>', self)
        self.__set_button(self.__side_grid, self.agc_btn, 2, 0, self.__agc_evnt, agc_lookup[self.__radio_model[1]['AGC']][1], 1)
        # Audio button
        self.audio_btn = QPushButton('Audio>', self)
        self.__set_button(self.__side_grid, self.audio_btn, 3, 0, self.__audio_evnt, "Audio>", 1)
        
        #-------------------------------------------------
        # VFO control
        vfo_grid = QGridLayout()
        main_grid.addLayout(vfo_grid, 0, 0)
        self.__vfo = Vfo(self.con, CH_RX, self.__id)
        self.__vfo.addVfo(self, vfo_grid)
    
    #==============================================================================================
    # PUBLIC
    #==============================================================================================
    
    #-------------------------------------------------
    # Callbacks
    #-------------------------------------------------
    # Callback for current mode
    def setMode(self, mode):    
        self.mode_btn.setText(mode)
    
    #-------------------------------------------------
    # Callback for current filter
    def setFilter(self, filter):    
        self.filter_btn.setText(filter)
    
    #-------------------------------------------------
    # Callback for current AGC setting
    def setAGC(self, agc):    
        self.agc_btn.setText(agc)
    
    #-------------------------------------------------
    # Callback for audio setting
    def setAudio(self, audio):    
        pass
    
    #-------------------------------------------------
    # Window metrics
    #-------------------------------------------------
    
    #-------------------------------------------------
    # Save window metrics
    def saveMetrics(self):
        Model.get_app_model()['METRICS'][self.__id] = [self.x(),self.y(),self.width(),self.height()]
        
    #==============================================================================================
    # OVERRIDES
    #==============================================================================================
    
    #-------------------------------------------------
    # Mouse wheel event for VFO
    def wheelEvent(self, event):
        # Forward event to VFO
        if event.angleDelta().y() >= 0:
            self.__vfo.doWheelEvent(VFO_UP)
        else:
            self.__vfo.doWheelEvent(VFO_DOWN)
    
    #==============================================================================================
    # EVENTS
    #==============================================================================================

    #-------------------------------------------------
    # Mode button event
    def __mode_evnt(self) :
        self.__modes = Modes(self.__id)
        self.__modes.set_context(self.setMode, self.x() + self.width() + 20, self.y() + 32, CH_RX)
        self.__modes.show()
    
    #-------------------------------------------------
    # Filter button event
    def __filter_evnt(self) :
        self.__filter = Filters(self.__id)
        self.__filter.set_context(self.setFilter, self.x() + self.width() + 20, self.y() + 32, CH_RX)
        self.__filter.show()
    
    #-------------------------------------------------
    # AGC button event
    def __agc_evnt(self) :
        self.agc = AGC(self.__id)
        self.agc.set_context(self.setAGC, self.x() + self.width() + 20, self.y() + 32, CH_RX)
        self.agc.show()
    
    #-------------------------------------------------
    # Audio button event
    def __audio_evnt(self) :
        self.audio = AudioOptions(self.__id)
        self.audio.set_context(self.setAudio, self.x() + self.width() + 20, self.y() + 32 , CH_RX)
        self.audio.show()
        
    #==============================================================================================
    # PRIVATE
    #==============================================================================================
    
    #-------------------------------------------------
    # Set up button
    def __set_button(self, grid, button, row, col, callback, text, style ):
        if style == 1 :
            button.setStyleSheet("QPushButton {background-color: rgb(59,59,59); color: rgb(148,148,148); font: bold 10px}")
        elif style == 2 :
            button.setStyleSheet("QPushButton {background-color: rgb(59,59,59); color: rgb(148,148,148); font: bold 12px}")
        grid.addWidget(button, row, col)
        button.clicked.connect(callback)
        button.setText(text)
        button.setMaximumSize(50,20)
    