#!/usr/bin/env python
#
# Tk UI for RustSDR
# 
# Copyright (C) 2023 by G3UKB Bob Cowdery
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

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from functools import partial

#=====================================================
# User Interface
#=====================================================
class TkUi:
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        # Create the root Tk object
        self.root = Tk()
        # Create a style object
        self.style = ttk.Style()
        # Set a decent theme
        self.style.theme_use('alt')
        self.root.configure(bg='dark slate gray')
        
        # Set some styles
        self.style.configure('B.TFrame', background='dark slate gray')
        self.style.configure('MHz.TLabel', font='helvetica 30', background='dark slate gray', foreground='blue', padding=20)
        self.style.configure('KHz.TLabel', font='helvetica 30', background='dark slate gray', foreground='blue', padding=20)
        self.style.configure('Hz.TLabel', font='helvetica 25', background='dark slate gray', foreground='orange', padding=20)
        self.style.configure('Sep.TLabel', font='helvetica 30', background='dark slate gray', foreground='black', padding=2)
        self.style.configure('Mode.TButton', font='helvetica 10', background='dark slate gray', foreground='chocolate', padding=2)
        self.style.configure('Filt.TButton', font='helvetica 10', background='dark slate gray', foreground='chocolate', padding=2)
        self.style.configure('Cont.TButton', font='helvetica 12', background='dark slate gray', foreground='orange', padding=2)

        # Component state
        self.vfo_digits = []
        self.__last_freq = 7100000
        self.modes = []
        self.filters = []
        
        # Canvas on which to build graphics
        self.__canvas_w = 600
        self.__canvas_h = 300
        self.canvas = Canvas(width=self.__canvas_w, height=self.__canvas_h)
        # To hold the newly created images
        self.images = []
        
        # Drawing parameters
        # db
        self.__high_db = -20
        self.__low_db = -140
        self.__db_step = 20
        self.__v_step = int((abs(self.__low_db) + self.__high_db) / self.__db_step)
        # freq
        self.__span_freq = 48000
        self.__f_step = 6000
        self.__h_step = int(self.__span_freq / self.__f_step)
        # margins
        self.__l_margin = 40
        self.__r_margin = 30
        self.__t_margin = 20
        self.__b_margin = 30
        # spec
        self.__v_space = self.__canvas_h - self.__t_margin - self.__b_margin
        self.__h_space = self.__canvas_w - self.__l_margin - self.__r_margin
        self.__db_range = abs(self.__low_db) + self.__high_db
        self.__dbpp = float(float(self.__v_space)/self.__db_range)
        # colors
        self.__grid_color = 'slate gray'
        self.__plot_color = 'yellow'
        
        # Get the connector instance
        self.__con = getInstance('interface_inst')
        self.init = False

    # Enter main UI loop
    def run (self):
        # Build the UI
        self.build_ui()
        # Create a timer event
        self.root.after(100, self.timer_evnt)
        # Main loop exits when window is closed
        self.root.mainloop()
    
    #-------------------------------------------------
    # Builder methods
    #
    # Build UI
    def build_ui(self):
        # A form for each major component
        vfo_frm = ttk.Frame(self.root, padding=10)
        vfo_frm.configure(style='B.TFrame')
        mode_frm = ttk.Frame(self.root, padding=10)
        mode_frm.configure(style='B.TFrame')
        filter_frm = ttk.Frame(self.root, padding=10)
        filter_frm.configure(style='B.TFrame')
        control_frm = ttk.Frame(self.root, padding=10)
        control_frm.configure(style='B.TFrame')
        
        vfo_frm.grid(column=0, row=0, columnspan=2, sticky='N')
        mode_frm.grid(column=0, row=1, sticky='N')
        filter_frm.grid(column=0, row=2, sticky='N')
        control_frm.grid(column=0, row=3, sticky='S')
        self.canvas.grid(column=1, row=1, rowspan=3)
        
        # Build components
        self.build_vfo(vfo_frm)
        self.build_modes(mode_frm)
        self.build_filters(filter_frm)
        self.build_control(control_frm)
        self.build_display(self.canvas)
     
    def build_vfo(self, frm):
        # VFO is 9 digits in sets of 3 MHz, KHZ and Hz
        for dig in  range(0,3):
            l = ttk.Label(frm, style='MHz.TLabel', text="0")
            l.grid(column=dig, row=0)
            self.vfo_digits.append(l)
            binding = [self.on100MHz,self.on10MHz,self.on1MHz]
            l.bind("<MouseWheel>", binding[dig])
        ttk.Label(frm, style='Sep.TLabel', text="-").grid(column=3, row=0)
        for dig in  range(4,7):
            l = ttk.Label(frm, style='KHz.TLabel', text="0")
            l.grid(column=dig, row=0)
            self.vfo_digits.append(l)
            binding = [self.on100KHz,self.on10KHz,self.on1KHz]
            l.bind("<MouseWheel>", binding[dig-4])
        ttk.Label(frm, style='Sep.TLabel', text="-").grid(column=7, row=0)
        for dig in  range(8,11):
            l = ttk.Label(frm, style='Hz.TLabel', text="0")
            l.grid(column=dig, row=0)
            self.vfo_digits.append(l)
            binding = [self.on100Hz,self.on10Hz,self.on1Hz]
            l.bind("<MouseWheel>", binding[dig-8])
        self.__adjust_vfo(self.__last_freq)
        
    def build_modes(self, frm):
        # Build modes in a 4x4 matrix
        modes = ('LSB','USB','DSB','CWU','CWL','FM','AM','DIGU','SPEC','DIGL','SAM','DRM')
        index = 0
        for row in range(0,4):
            for col in range(0,3):
                m = ttk.Button(frm, style='Mode.TButton', text=modes[index], command = partial( self.set_mode, index))
                m.grid(column=col, row=row)
                self.modes.append(m)
                index += 1
        
    def build_filters(self, frm):
        # Build filters in a 4x4 matrix
        filt = ('6.0K','4.0K','2.7K','2.4K','2.1K','1.0K','500Hz','250Hz','100Hz')
        index = 0
        for row in range(0,3):
            for col in range(0,3):
                f = ttk.Button(frm, style='Filt.TButton', text=filt[index], command = partial( self.set_filter, index))
                f.grid(column=col, row=row)
                self.filters.append(f)
                index += 1
        
    def build_control(self, frm):
        start = ttk.Button(frm, style='Cont.TButton', text="Start", command = self.start_lib)
        start.grid(column=0, row=1)
        stop = ttk.Button(frm, style='Cont.TButton', text="Stop", command = self.stop_lib)
        stop.grid(column=1, row=1)
    
    def build_display(self, canvas):
        self.create_rectangle(0, 0, 600, 300, fill='dark slate gray')
        self.h_grid(self.canvas)
        self.v_grid(self.canvas)
        if self.init: self.spec(self.canvas)
    
    def h_grid(self, canvas ):
        y_inc = (self.__canvas_h - self.__t_margin - self.__b_margin) / self.__v_step
        for step in range(0, self.__v_step + 1):
            # Draw line
            self.canvas.create_line(self.__l_margin, self.__t_margin + (y_inc * step), self.__canvas_w - self.__r_margin , self.__t_margin + (y_inc * step), fill=self.__grid_color)
            # Draw legend
            self.canvas.create_text(10, self.__t_margin + (y_inc * step), anchor=W, font="Purisa 10", fill="#fb0", text=str(self.__high_db - (self.__db_step * step)))
    
    def v_grid(self, canvas ):
        x_inc = (self.__canvas_w - self.__l_margin - self.__r_margin) / self.__h_step
        f_start = float((self.__last_freq - (self.__span_freq/2))/1000000.0)
        for step in range(0, self.__h_step + 1):
            # Draw line
            self.canvas.create_line(self.__l_margin + (x_inc * step), self.__t_margin, self.__l_margin + (x_inc * step), self.__canvas_h - self.__b_margin, fill=self.__grid_color)
            # Draw legend
            f = str("%.3f" % round(f_start + float((self.__f_step * step)/1000000.0) ,3))
            self.canvas.create_text(self.__l_margin - 15 + (x_inc * step), self.__canvas_h - 10, anchor=W, font="Purisa 10", fill="#fb0", text=f)
    
    def spec(self, canvas):
        # Get data if ready
        d = self.__con.get_disp_data()
        # We have one value for each pixel in the display area
        for pix in range(0, self.__h_space, 2):
            self.canvas.create_line(pix, self.__db_to_y(d[pix]), pix+1, self.__db_to_y(d[pix+1]), fill=self.__plot_color)
        
    def __db_to_y(self, dbm):
        # Not sure how to offset and scale this
        #rel_db = (abs(self.__st_db) - abs(int(dbm))) + 150
        rel_db = (abs(self.__low_db) - abs(int(dbm)))
        return (self.__t_margin + self.__v_space) - (rel_db * self.__dbpp)
            
    #-------------------------------------------------
    # Utility methods
    #
    #-------------------------------------------------
    # Rewrite the VFO digits with current frequency
    def __adjust_vfo(self, freq):
        """
        Set the VFO to the given frequency
        
        freq    --  freq to set in Hz
        
        """
        
        freq_str = str(freq).zfill(9)
        self.vfo_digits[0].config(text=freq_str[0])
        self.vfo_digits[1].config(text=freq_str[1])
        self.vfo_digits[2].config(text=freq_str[2])
        self.vfo_digits[3].config(text=freq_str[3])
        self.vfo_digits[4].config(text=freq_str[4])
        self.vfo_digits[5].config(text=freq_str[5])
        self.vfo_digits[6].config(text=freq_str[6])
        self.vfo_digits[7].config(text=freq_str[7])
        self.vfo_digits[8].config(text=freq_str[8])
        
        self.__last_freq = freq
    
    def __inc_freq(self, evnt, inc):
        v = inc
        if evnt.delta < 0:
            inc = -inc            
        self.__last_freq = self.__last_freq + inc
        self.__adjust_vfo(self.__last_freq)
        if self.init: self.__con.set_freq(self.__last_freq)
        
    # Used to create rectangles with alpha as this requires use of PIL lib
    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = root.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    
    #-------------------------------------------------
    # Event methods
    #
    # On VFO digit scroll
    def on100MHz(self, evnt):
        self.__inc_freq(evnt, 100000000)
    def on10MHz(self, evnt):
        self.__inc_freq(evnt, 10000000)
    def on1MHz(self, evnt):
        self.__inc_freq(evnt, 1000000)
    def on100KHz(self, evnt):
        self.__inc_freq(evnt, 100000)
    def on10KHz(self, evnt):
        self.__inc_freq(evnt, 10000)
    def on1KHz(self, evnt):
        self.__inc_freq(evnt, 1000)
    def on100Hz(self, evnt):
        self.__inc_freq(evnt, 100)
    def on10Hz(self, evnt):
        self.__inc_freq(evnt, 10)
    def on1Hz(self, evnt):
        self.__inc_freq(evnt, 1)
    
    # On timer
    def timer_evnt(self):
        # Build displays
        if self.init: self.build_display(self.canvas)
        self.root.update()
        self.root.after(100, self.timer_evnt)
        
    #-------------------------------------------------
    # Control methods
    #
    def start_lib(self):
        self.__con.run_lib()
        sleep(1)
        # Set our display width
        self.__con.set_disp_width(self.__h_space)
        # Create a timer event
        self.root.after(100, self.timer_evnt)
        self.init = True
    
    def stop_lib(self, ):
        if self.init: self.__con.close_lib()
        self.init = False
        
    def set_mode(self, mode):
        if self.init: self.__con.set_mode(mode)
    
    def set_filter(self, filt):
        if self.init: self.__con.set_filter(filt)
        
"""
frm = ttk.Frame(root, padding=10)
frm1 = ttk.Frame(root, padding=10)

frm.grid()
frm1.grid(column=0, row=2)

l = ttk.Label(frm, text="Hello World!")
l.grid(column=0, row=0)
l.bind("<MouseWheel>", onMouseWheel)

s.configure('B1.TButton', font='helvetica 14', background='red', foreground='blue', padding=20)
b = ttk.Button(frm, style='B1.TButton', text="Quit", command=root.destroy)
b.grid(column=1, row=0)

b1 = ttk.Button(frm1, style='B1.TButton', text="Quit", command=root.destroy)
b1.grid(column=0, row=0)
b2 = ttk.Button(frm1, style='B1.TButton', text="Quit", command=root.destroy)
b2.grid(column=1, row=0)
b3 = ttk.Button(frm1, style='B1.TButton', text="Quit", command=root.destroy)
b3.grid(column=0, row=1)
b4 = ttk.Button(frm1, style='B1.TButton', text="Quit", command=root.destroy)
b4.grid(column=1, row=1)
b5 = ttk.Button(frm1, style='B1.TButton', text="Quit", command=root.destroy)
b5.grid(column=2, row=0)
b6 = ttk.Button(frm1, style='B1.TButton', text="Quit", command=root.destroy)
b6.grid(column=2, row=1)

create_rectangle(10, 10, 200, 100, fill='blue')
create_rectangle(50, 50, 250, 150, fill='green', alpha=.5)
create_rectangle(80, 80, 150, 120, fill='#800000', alpha=.8)
canvas.grid(column=0, row=1)

root.mainloop()
"""


