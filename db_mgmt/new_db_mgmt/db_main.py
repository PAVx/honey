#!/usr/bin/python
# filename: db_main.py
# Core database program

import dbi
import dbz
from dbs import drone_entry
from random import randint
import ConfigParser
import time
import RPi.GPIO as GPIO
import os
import shutil

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
ground_db = config.get(_identifiers, 'rover')
drone_db = config.get(_identifiers, 'drone')
drone_db_real = drone_db + "s"

# Get number of drones in system
num_drones = int(config.get(_core_variables, 'n_drones'))

# Create drone reference table
drones_ref = []
for i in range(num_drones):
    drones_ref.append(drone_db + str(i))
    
# Get number of sensors
num_sensors = int(config.get(_core_variables, 'n_channels'))

# Create instrument/channel reference table
sensors_ref = []
for i in range(num_sensors):
    sensors_ref.append("sensor" + str(i))
print "Sample size set to ", n, " every ", wait_time, " seconds." 

# Some clock stuff
CLOCK_IN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLOCK_IN, GPIO.IN)

# Create array of channels to contain data sent from a drone
drone_data = [drone_entry for count in range(num_drones)]

# Init poll function from dbz
dbz.init_poll()
 
# Data Construction Functions
def assemble_sensor_data(d, i):
    drone_data[d] = dbz.poll(i)

def assemble_channels(i):
    for k in range(num_drones):
        assemble_sensor_data(k, i)

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
        # At the end of n samples, perform averaging and store to database
        m = m + 1        
        if m >= n:
            m = 0
            # TEST THE DOOR            
            for drone in drones_ref:
                # Get index for channel storage
                j = drones_ref.index(drone)
                for i in range(len(sensors_ref)):
                    drone_data[j].s[i].avg_data = n_average(drone_data[j].s[i].data)
                    drone_data[j].s[i].pts = drone_data[j].s[i].avg_data / 2
                # Add function: add_entry(inst_t, x, y, z, meas_val, pts)
                dbi.add_entry(drone_db_real,\
                              drone,\
                              drone_data[j].x,\
                              drone_data[j].y,\
                              drone_data[j].z,\
                              drone_data[j].s)
                              #n_average(channels[j].meas_val),\
                              #n_average(channels[j].pts))        

        # Wait for tick
        # time.sleep(wait_time)

    except KeyboardInterrupt:
        GPIO.cleanup()
        #delete the entire folder if it exists from a previous run
        if os.path.exists("data"):
            shutil.rmtree("data")
        #make the data folder
        dbi._make_folder("data")
        for drone in drones_ref:
            dbi._make_folder("data/" + drone)
            #make the drone folders here
            print "\n", drone
            log = open("data/" + "/" + drone + "_log.csv", 'w')
            print("File opened. Writing to file...")
            dbi.write_all_entries(drone_db_real, drone, log)
            log.close()
            #dbi.fetch_all_entries(drone, ch)
            dbi._exit(drone)
        print "\n ALL ENTRIES LISTED! Program closing."
        break

##GPIO.cleanup()
##dbi.fetch_all_entries("Instrument0_data")
##dbi._exit()

