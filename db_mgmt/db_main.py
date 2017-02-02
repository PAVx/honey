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
# Set sample size
n = int(config.get(_core_variables, 'n_samples'))
num_instr = int(config.get(_core_variables, 'n_channels'))
wait_time = 1/(float(config.get(_core_variables, 'sample_rate')))
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
        if m >= n:
            m = 0
            for j in range(num_instr):
                # Create table name
                table_name = ("Instrument" + str(j) + "_data")
                # Add function: add_entry(inst_t, x, y, z, meas_val, pts)
                dbi.add_entry(table_name,\
                              channels[j].x,\
                              channels[j].y,\
                              channels[j].z,\
                              n_average(channels[j].meas_val),\
                              n_average(channels[j].pts))        

        # Wait for tick
        time.sleep(wait_time)

    except KeyboardInterrupt:
        GPIO.cleanup()
        for l in range(num_instr):
            table_name = ("\nInstrument" + str(l) + "_data")
            print table_name
            dbi.fetch_all_entries(table_name)
        dbi._exit()
        break

##GPIO.cleanup()
##dbi.fetch_all_entries("Instrument0_data")
##dbi._exit()

