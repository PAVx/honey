#!/usr/bin/python
# filename: db_main.py
# core database program

import dbi
from random import randint
import ConfigParser
import time
import RPi.GPIO as GPIO

# Configuration
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
_identifiers = 'IDENTIFIERS'
# Set sample size
n = int(config.get(_core_variables, 'n_samples'))
wait_time = 1/(float(config.get(_core_variables, 'sample_rate')))
# Load identifiers for ground and drones
# ground_db = config.get(_db_info, 'dbin')
ground_db = config.get(_identifiers, 'rover')
drone_db = config.get(_identifiers, 'drone')
# Get number of drones in system
num_drones = int(config.get(_core_variables, 'n_drones'))
# Create drone reference table
drones_ref = []
for i in range(num_drones):
    drones_ref.append(drone_db + str(i) + "DB")
# Get number of instruments/channels
num_instr = int(config.get(_core_variables, 'n_channels'))
# Create instrument/channel reference table
channels_ref = []
for i in range(num_instr):
    channels_ref.append("channel" + str(i) + "_data")
print "Sample size set to ", n, " every ", wait_time, " seconds." 

# Some clock stuff
CLOCK_IN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLOCK_IN, GPIO.IN)


# Instrument Channels
class channel:
    time = 0
    x = 0
    y = 0
    z = 0
    meas_val = [0] * n
    pts = [0] * n

channels = [channel for count in range(num_instr)]

# Data Construction Functions
def assemble_ch_data(ch, i):
    channels[ch].meas_val[i] = randint(0,100)
    channels[ch].pts[i] = randint(0,100)
    channels[ch].time = randint(0,100)
    channels[ch].x = randint(0,100)
    channels[ch].y = randint(0,100)
    channels[ch].z = randint(0,100)

def assemble_channels(i):
    for k in range(num_instr):
        assemble_ch_data(k, i)

def n_average(lst):
    total = 0
    for val in lst:
        total += val
    return (total/len(lst))
        
        
# Incrementer for the average counter
m = 0



while(1):
    try: 
        # Wait for the rising edge of a "clock tick"
        # GPIO.wait_for_edge(CLOCK_IN, GPIO.RISING)

        # Proceed assembling data in all channels
        assemble_channels(m)
        
        print "."

        # Check for nth measurement and store to database.
        m = m + 1

        # At the end of n samples, perform averaging
        if m >= n:
            m = 0
            for drone in drones_ref:
                for ch in channels_ref:
                    # Get index for channel storage
                    j = channels_ref.index(ch)
                    # Add function: add_entry(inst_t, x, y, z, meas_val, pts)
                    dbi.add_entry(drone,\
                                  ch,\
                                  channels[j].x,\
                                  channels[j].y,\
                                  channels[j].z,\
                                  n_average(channels[j].meas_val),\
                                  n_average(channels[j].pts))        

        # Wait for tick
        time.sleep(wait_time)

    except KeyboardInterrupt:
        GPIO.cleanup()
        for drone in drones_ref:
            for ch in channels_ref:
                print "\n", drone, "\n", ch
                dbi.fetch_all_entries(drone, ch)
            dbi._exit(drone)
        print "\n ALL ENTRIES LISTED! Program closing."
        break

##GPIO.cleanup()
##dbi.fetch_all_entries("Instrument0_data")
##dbi._exit()

