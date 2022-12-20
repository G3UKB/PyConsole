#!/usr/bin/env python
#
# sdr_script - Common User Interface classes - metering
# 
# User: bob
# Date: 13/12/14
# Copyright (C) 2013 by G3UKB Bob Cowdery
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

# System imports
import os,sys
from PyQt4 import QtCore, QtGui

# Application imports
from common.defs import *

"""

Main class for RX and TX metering

"""
class Meter(QtGui.QWidget):
    
    def __init__(self, w, direction, meter_mode):
        """
        Constructor
        
        Arguments:
            direction   --  CH_RX | CH_TX
            meter_mode  --  CH_RX = M_RX_S_PEAK | M_RX_S_AV | M_RX_IN_PEAK | M_RX_IN_AV | M_RX_AGC_GAIN | M_RX_AGC_PEAK | M_RX_AGC_AV
                        --  CH_TX = M_TX_MIC_PK | M_TX_MIV_AV | M_TX_EQ_PK | M_TX_EQ_AV | M_TX_LEV_PK | M_TX_LEV_AV | M_TX_LEV_GAIN | M_TX_COMP_PK | M_TX_COMP_AV | M_TX_ALC_PK | M_TX_ALC_AV | M_TX_ALC_GAIN | M_TX_OUT_PK | M_TX_OUT_AV
        """
        
        super(Meter, self).__init__(w)
        
        # We only deal with one RX and one TX mode at present so the actual mode is ignored right now
        self.__direction = direction
        if direction == CH_RX:
            self.__scale = (('1',0),('2',0),('3',0),('4',0),('5',0),('6',0),('7',0),('8',0),('9',0),('+10', 0.67),('+20',1.34))
            self.__st_dbm = -121.0
            self.__end_dbm = -121.0 + (9.0*6.0) + 20
        elif direction == CH_TX:
            self.__scale = (('0',0),('10',0),('20',0),('30',0),('40',0),('50',0))
            self.__st_dbm = 0.0
            self.__end_dbm = 50.0
        else:
            return
        self.__font = QtGui.QFont('Times', 8)
        self.__legend_pen = QtGui.QPen(QtGui.QColor(75,150,113))
        self.__value_pen = QtGui.QPen(QtGui.QColor(182,28,5))
        self.__value_pen.setWidth(4)
        
        self.__h_text_left = 10
        self.__h_text_base = 8
        self.__st_x = 10
        self.__end_x = 10
        self.__st_y = 15
        self.__dbpp = 0

    def paintEvent(self, e):
        
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHints(QtGui.QPainter.Antialiasing)
        qp.setPen(self.__legend_pen)
        qp.drawPath(self.__make_path())
        qp.setPen(self.__value_pen)
        qp.drawLine(self.__st_x, self.__st_y, self.__end_x, self.__st_y)
        qp.end()
    
    def update_meter(self, sig):
        
        rel_dbm = abs(self.__st_dbm) - abs(sig)
        px = rel_dbm * self.__dbpp
        self.__end_x = self.__st_x + px
        self.update()
    
    def __make_path(self):
        
        path = QtGui.QPainterPath()
        h_step = (self.width() - 35)/len(self.__scale)
        self.__dbpp = float(abs(self.__st_dbm) - abs(self.__end_dbm))/float(abs(self.__end_dbm))        
        for n in range(len(self.__scale)):
            path.addText(QtCore.QPointF(float((h_step*n) + self.__h_text_left + self.__scale[n][1]*h_step), float(self.__h_text_base)), self.__font, self.__scale[n][0])		
        
        return path