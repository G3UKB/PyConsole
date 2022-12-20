import time
from ctypes import *

import os
os.add_dll_directory('E:\\Projects\\RustSDRLib\\trunk\\rust_sdr_lib\\libs')

lib = cdll.LoadLibrary("rustsdrlib.dll")

init = lib.sdrlib_init
start = lib.sdrlib_run
stop = lib.sdrlib_close
freq = lib.sdrlib_freq
mode = lib.sdrlib_mode
filt = lib.sdrlib_filter
disp = lib.sdrlib_disp_data

init()
start()
time.sleep(1)
freq(7150000)
print("Set freq")
time.sleep(2)
freq(7180000)
print("Set freq")
time.sleep(2)
mode(2)
print("Set mode")
time.sleep(2)
filt(4)
print("Set filter")
time.sleep(2)

disp.restype = POINTER(c_float)
x = POINTER(c_float)

x = disp()
print("Got disp")
print("**********\n")
for n in range (300):
    print(x[n])
print("**********\n")
time.sleep(2)
print("Term")
stop()
print("Done")
