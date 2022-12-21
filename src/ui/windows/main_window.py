#!/usr/bin/env python
#
# main_wimndow.py
#
# Main window for the SDRLibEConsole application
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
# The main window for SDRLibEConsole
#==============================================================================================

#=====================================================
# Main window class
# The main window runs RX1 and has all common controls
# Auxiliary windows run the other radios
#=====================================================
class MainWindow(WindowBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        
        WindowBase.__init__(self, 'Control [Radio-1]', RX_1)
        
        #-------------------------------------------------
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Stopped",0)
        self.statusBar.setStyleSheet("QStatusBar {background-color: rgb(102,102,102); color: rgb(147,11,11); font: bold 12px}")
        
        #-------------------------------------------------
        # Set up toolbar
        exitAct = QAction(self.style().standardIcon(QStyle.SP_TitleBarCloseButton), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.__exit_evnt)
        
        runAct = QAction(self.style().standardIcon(QStyle.SP_MediaPlay), 'Run', self)
        runAct.setShortcut('Ctrl+R')
        runAct.triggered.connect(self.__run)
        
        stopAct = QAction(self.style().standardIcon(QStyle.SP_MediaStop), 'Stop', self)
        stopAct.setShortcut('Ctrl+S')
        stopAct.triggered.connect(self.__stop)
        
        dispAct = QAction(self.style().standardIcon(QStyle.SP_ToolBarHorizontalExtensionButton), 'Disp', self)
        dispAct.setShortcut('Ctrl+D')
        dispAct.triggered.connect(self.__disp)
        
        self.__num_rx = QComboBox()
        self.__num_rx.addItems(('1','2','3'))
        self.__num_rx.activated.connect(self.__num_rx_evnt)
        self.__num_rx.setStyleSheet("QComboBox {background-color: rgb(59,59,59); selection-background-color: rgb(59,59,59)}")
        self.__num_rx.setCurrentIndex(self.__num_rx.findText(str(Model.get_num_rx())))
        
        self.__r2Act = QAction('Radio-2', self)
        self.__r2Act.setShortcut('Ctrl+2')
        self.__r2Act.triggered.connect(self.__r2)
        
        self.__r3Act = QAction('Radio-3', self)
        self.__r3Act.setShortcut('Ctrl+3')
        self.__r3Act.triggered.connect(self.__r3)
        
        self.toolbar = self.addToolBar('ToolBar')
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(runAct)
        self.toolbar.addAction(stopAct)
        self.toolbar.addAction(dispAct)
        self.toolbar.addWidget(self.__num_rx)
        self.toolbar.addAction(self.__r2Act)
        self.toolbar.addAction(self.__r3Act)
        self.toolbar.setStyleSheet("QToolBar {background-color: rgb(102,102,102); color: red; font: bold 12px}")
        
        #-------------------------------------------------
        # Set main panel and grid
        panel = QWidget()
        self.setCentralWidget(panel)
        main_grid = QGridLayout()
        panel.setLayout(main_grid)
        
        #-------------------------------------------------
        # Populate
        self.setup_ui(main_grid)
    
        #-------------------------------------------------
        # Set visibility
        self.__set_visibility(Model.get_num_rx())
        
    #==============================================================================================
    # EVENTS
    #==============================================================================================
    
    #-------------------------------------------------
    # Run button event
    def __run(self) :
        
        # Perform a server warmstart
        self.con.run_lib()
        self.statusBar.showMessage("Running",0)
        self.statusBar.setStyleSheet("QStatusBar {background-color: rgb(102,102,102); color: rgb(0,64,0); font: bold 12px}")
        
    #-------------------------------------------------
    # Stop button event        
    def __stop(self):
        # Stop radio
        state = Model.get_state_model()
        self.con.close_lib()
        self.statusBar.showMessage("Stopped",0)
        self.statusBar.setStyleSheet("QStatusBar {background-color: rgb(102,102,102); color: rgb(147,11,11); font: bold 12px}")
        state['RADIO-RUN'] = False
        
    #-------------------------------------------------
    # Display button event        
    def __disp(self):
        # Invoke displays
        self.__disp = DisplayWindow("Panadapter", 0)
        self.__disp.show()
            
    #-------------------------------------------------
    # Exit button event
    def closeEvent(self, win) :
       self. __exit_evnt()
       
    def __exit_evnt(self) :
        QApplication.quit()
        qApp.quit()
    
    #-------------------------------------------------
    # Set number of radios
    def __num_rx_evnt(self):
        # Potentially the number of receivers has changed.
        num_rx = int(self.__num_rx.currentText())
        if num_rx != Model.get_num_rx():
            # Changed
            Model.set_num_rx(num_rx)
            # Stop and restart the server and set up everything again
            if not self.con.restart():
                print("Failed to restart server!")
            # Change the UI enablement and close aux receivers
            self.__set_visibility(num_rx)
            
    #-------------------------------------------------
    # Set number of radios
    def __set_visibility(self, num_rx):
       
        if num_rx == 1:
            self.__r2Act.setEnabled(False)
            self.__r3Act.setEnabled(False)
            if getInstance('aw2_inst') != None: getInstance('aw2_inst').hide()
            if getInstance('aw3_inst') != None: getInstance('aw3_inst').hide()
        elif num_rx == 2:
            self.__r2Act.setEnabled(True)
            self.__r3Act.setEnabled(False)
            if getInstance('aw23_inst') != None: getInstance('aw3_inst').hide()
        if num_rx== 3:
            self.__r2Act.setEnabled(True)
            self.__r3Act.setEnabled(True)
        # Show stopped
        self.statusBar.showMessage("Stopped",0)
        self.statusBar.setStyleSheet("QStatusBar {background-color: rgb(102,102,102); color: rgb(147,11,11); font: bold 12px}")
                
    #-------------------------------------------------
    # Invoke radios 2-3
    def __r2(self):
        getInstance('aw2_inst').show()
        
    def __r3(self):
        getInstance('aw3_inst').show()
        
    #==============================================================================================
    # PRIVATE
    #==============================================================================================
    

    