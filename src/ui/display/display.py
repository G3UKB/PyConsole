#!/usr/bin/env python
#
# display.py
#
# Python panadapter display GUI for the SDRLibEConsole application
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

"""
	Panadapter display for one receiver.
	Multi-instance for each active receiver.
	The widget is placed within the display window for display.
"""
class Panadapter(QWidget):
	
	def __init__(self, rx_id, width, height, freq_callback):
		"""
		Constructor
		
		Arguments:
			rx_id			--	RX ID this display belongs to
			width			-- 	Full display area width
			height			--	Full display area height
			freq_callback	--	callback for click tune
		"""
		
		super(Panadapter, self).__init__()
		
		self.__rx_id = rx_id
		self.__width = width
		self.__height = height
		self.__freq_callback = freq_callback
		
		# Set the back colour
		palette = QPalette()
		palette.setColor(QPalette.Background,QColor(43,63,68,255))
		self.setPalette(palette)

		# Initialise vars
		self.__center_freq = 7.1
		self.__bandwidth = 0.048
		self.__half_bandwidth = 0.048/2.0
		self.__filter_low = -2700
		self.__filter_high = -300
		self.__mouse_x = 0
		self.__mouse_y = 0
		self.__show_freq = False
		# Drawing params
		self.__top_border = 10
		self.__left_border = 50
		self.__right_border = 10
		self.__bottom_border = 25
		self.__h_text_base = 40
		self.__h_text_left = 35
		self.__v_text_left = 8
		self.__h_no = 11
		self.__pixels = None
		# Display ref and data holding
		self.__display_ob = None
		self.__display_data = None
		
		# Set the resources
		self.__grid_pen = QPen(QColor(39,83,109))
		self.__grid_pen.setWidth(1)
		self.__grid_pen.setStyle(Qt.DotLine)
		self.__legend_pen = QPen(QColor(178,178,178))
		self.__legend_pen.setWidth(1)
		self.__label_pen = QPen(QColor(255,0,0))
		self.__label_pen.setWidth(1)
		self.__filter_pen = QPen(QColor(0,255,0, 20))
		self.__filter_pen.setWidth(1)
		self.__filter_brush = QBrush(QColor(0,255,0, 20))
		self.__freq_pen = QPen(QColor(255,0,0))
		self.__freq_pen.setWidth(1)
		self.__data_pen = QPen(QColor(0,255,0))
		self.__data_pen.setWidth(1)
		self.__font = QFont('Times', 8)
		
		# Define the painter paths
		self.__painter_paths = {
			'grid': [[QPainterPath(), self.__grid_pen, None],],
			'legend': [[QPainterPath(), self.__legend_pen, None],],
			'label': [[QPainterPath(), self.__label_pen, None],],
			'dynamic': [
					[QPainterPath(), self.__filter_pen, self.__filter_brush],
					[QPainterPath(), self.__freq_pen, None]
				],
			'data': [[QPainterPath(), self.__data_pen, None],]
		}
		# Enable mouseMoveEvent()
		self.setMouseTracking(True)
		
		# Create a label for showing freq at cursor
		self.__freq_disp = QLabel('', self)
		self.__freq_disp.setStyleSheet("QLabel {color: rgb(255,0,0);  font: bold 12px}")
		self.__freq_disp.setText('')
		
		# Get the connector instance
		self.__con = getInstance('conn_inst')
		
		# Set display
		self.__pixels = width - self.__left_border - self.__right_border
		self.__con.set_display(rx_id, self.__pixels)
		
		# Refresh display every IDLE_TICKER ms
		QTimer.singleShot(IDLE_TICKER, self.timerEvent)
	
	#===========================================================================================
	# PUBLIC
		
	def setCenterFreq(self, freq):
		self.__center_freq = freq
		self.__makePainterPaths()
	
	def setBandwidth(self, bandwidth):
		self.__bandwidth = bandwidth
		self.__half_bandwidth = bandwidth/2.0
		self.__makePainterPaths()
		
	def setFilterLimits(self, filter_low, filter_high):
		self.__filter_low = float(filter_low)/1000000.0
		self.__filter_high = float(filter_high)/1000000.0
		self.__makePainterPaths()
		
	#===========================================================================================
	# Qt EVENTS
	
	def resizeEvent(self, e):
		# Save change
		self.__width = e.size().width()
		self.__height = e.size().height()
		self.__pixels = self.__width - self.__left_border - self.__right_border
		# Tell server width has changed
		# This changes the number of pixels returned to match the width
		self.__con.set_display_width(self.__rx_id, self.__pixels)
		
	def paintEvent(self, e):
		# Paint context
		qp = QPainter()
		qp.begin(self)
		qp.setRenderHints(QPainter.Antialiasing)
		# Paint according to the definition
		self.__freq_disp.setGeometry(self.__mouse_x, self.__mouse_y, 50, 20)
		for key, value in self.__painter_paths.items():
			for (path, pen, brush) in value:
				if pen != None: qp.setPen(pen)
				if brush != None: qp.setBrush(brush)
				qp.drawPath(path)
		qp.end()
		
	def mouseMoveEvent(self, e):		
		# Display a frequency label at the cursor position.
		self.__mouse_x = e.x() + 10
		self.__mouse_y = e.y() - 10
		#self.__freq_disp.setText('{:.3f}'.format(self.__st_freq + (self.__fpp*(e.x() - self.__left_border))))
		self.update()
	
	def enterEvent(self, e):
		self.__freq_disp.show()
		
	def leaveEvent(self, e):
		self.__freq_disp.hide()
		
	def mousePressEvent(self, e):
		freq = self.__st_freq + (self.__fpp*(e.x() - self.__left_border))
		self.__freq_callback(freq)
	
	def timerEvent(self):
		""" Process any waiting update """
		# Make context for rendering
		# Get data if ready
		r, self.__display_data = self.__con.get_display_data(self.__rx_id)
		#print(r,self.__display_data)
		if r:
			# Render
			self.__makePainterPaths()
			self.__process_pan_data()
			# Force a paint
			self.update()
		
		# Call again in IDLE_TICKER ms
		QTimer.singleShot(IDLE_TICKER, self.timerEvent)

	#===========================================================================================
	# PRIVATE
	
	def __makePainterPaths(self):
		# Set up the context to calculate the paths 
		v_no = int(self.__width/50)
		self.__h_space = self.__width - self.__left_border - self.__right_border
		h_step = self.__h_space/(v_no)
		self.__v_space = self.__height - self.__top_border - self.__bottom_border
		v_step = self.__v_space/(self.__h_no-1)
		self.__h_text_base = self.__top_border + self.__v_space + 15
		
		# Frequency calculations
		center_freq = self.__center_freq
		self.__st_freq = center_freq - self.__half_bandwidth
		end_freq = center_freq + self.__half_bandwidth
		span = end_freq - self.__st_freq
		f_span_step = float(span)/float(v_no)
		self.__fpp = float(self.__half_bandwidth * 2.0)/float(self.__h_space)
		center_freq_x = int(float(self.__left_border) + ((center_freq - self.__st_freq)/self.__fpp))
		
		# Filter calculations
		filter_low_x = int(float(self.__left_border) + (((center_freq - self.__st_freq) + self.__filter_low)/self.__fpp))
		filter_high_x = int(float(self.__left_border) + (((center_freq - self.__st_freq) + self.__filter_high)/self.__fpp))
		
		# db calculations
		self.__st_db = -140.0
		db_span_step = 10.0
		db_range = db_span_step * (self.__h_no - 1)
		self.__dbpp = float(float(self.__v_space)/db_range)
		
		# Clear (except data) and assign the painter paths
		for key, value in self.__painter_paths.items():
			for path in value:
				if key != 'data':
					path[0] = QPainterPath()
		grid_path = self.__painter_paths['grid'][0][0]
		legend_path = self.__painter_paths['legend'][0][0]
		label_path = self.__painter_paths['label'][0][0]
		filter_path = self.__painter_paths['dynamic'][0][0]
		freq_path = self.__painter_paths['dynamic'][1][0]
		
		# Create the grid
		for n in range (self.__h_no):
			grid_path.moveTo(*(self.__left_border, (v_step*n) + self.__top_border))
			grid_path.lineTo(*(self.__left_border + self.__h_space,  (v_step*n) + self.__top_border))
		for n in range (v_no+1):
			grid_path.moveTo(*((h_step*n) + self.__left_border, self.__top_border))
			grid_path.lineTo(*((h_step*n) + self.__left_border, self.__top_border + self.__v_space))
			
		# Create the legends
		for n in range (v_no):
			# Frequency
			legend_path.addText(QPointF(float(((h_step*n) + self.__h_text_left)), float(self.__h_text_base)), self.__font, "{:7.3f}".format(self.__st_freq+(n*f_span_step)))		
		for n in range (1, self.__h_no):
			# dBM
			legend_path.addText(QPointF(float(self.__v_text_left), float(self.__top_border + self.__v_space - (v_step*n))), self.__font, "{:5.1f}".format(self.__st_db+(n*db_span_step)))
		
		# Additional text
		label_path.addText(QPointF(10, float(self.__h_text_base - 20)), self.__font, 'dbM')
		label_path.addText(QPointF(float(self.__left_border + self.__h_space - 20), float(self.__h_text_base)), self.__font, 'MHz')
		
		# Dynamic data
		filter_path.addRect(filter_low_x, self.__top_border, filter_high_x - filter_low_x, self.__v_space)
		freq_path.moveTo(*(center_freq_x, self.__top_border))		
		freq_path.lineTo(*(center_freq_x, self.__top_border + self.__v_space))
	
	def __process_pan_data(self):
		""" Process and write the display data  """
		self.__painter_paths['data'][0][0] = QPainterPath()
		data_path = self.__painter_paths['data'][0][0]
		#data_path.moveTo(*(self.__left_border, self.height() - self.__bottom_border))
		data_path.moveTo(*(self.__left_border, self.__dbToY(self.__display_data[self.__pixels-1])))
		data_path.lineTo(*(self.__left_border, self.__dbToY(self.__display_data[self.__pixels-1])))
		index = self.__pixels-2
		for x_coord in range(self.__left_border + 1, self.__left_border + self.__h_space):
			data_path.lineTo(*(x_coord, self.__dbToY(self.__display_data[index])))
			if index > 0:
				index -= 1
		self.__display_data = None
				
	def __dbToY(self, dbm):
		
		# Not sure how to offset and scale this
		#rel_db = (abs(self.__st_db) - abs(int(dbm))) + 150
		rel_db = (abs(self.__st_db) - abs(int(dbm)))
		return (self.__top_border + self.__v_space) - (rel_db * self.__dbpp)

		