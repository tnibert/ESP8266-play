#! /bin/bash
# these are some example

# run code one time like so
ampy -b 115200 -p /dev/ttyUSB0 run touchpad.py

# load code onto system (persistent across restarts)
#ampy -b 115200 -p /dev/ttyUSB0 put main.py
