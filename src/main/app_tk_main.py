#!/usr/bin/env python3
#
# app_tk_main.py
#
# Entry point for PyConsole
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
import sys
sys.path.append('..')
from main.imports import *

#=====================================================
# Main application class
#=====================================================
class AppMain:
    
    #-------------------------------------------------
    # Start processing and wait for user to exit the application
    def main(self):
        
        # Restore the model
        self.__m = Model()
        addToCache('model_inst', self.__m)
        self.__m.restore_model()
        
        # Create lib interface
        self.lib_if = Interface()
        addToCache("interface_inst", self.lib_if)
        
        # Init server
        self.lib_if.init_lib()
        
        # Create the UI
        ui = TkUi()
        ui.run()
        
        # Close the lib
        self.lib_if.close_lib()
        
#=====================================================
# Entry point
#=====================================================

#-------------------------------------------------
# Start processing and wait for user to exit the application
def main():
    try:
        app = AppMain()
        sys.exit(app.main())
        
    except Exception as e:
        print ('Exception from main code','Exception [%s][%s]' % (str(e), traceback.format_exc()))

#-------------------------------------------------
# Enter here when run as script        
if __name__ == '__main__':
    main()
