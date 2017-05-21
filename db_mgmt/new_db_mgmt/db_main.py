#!/usr/bin/python
# filename: db_main.py
# Core database program

# TOOLS
import MySQLdb

# PROGRAMS
import dbi
import dbz
from dbs import drone_entry
import db_queue
import db_sync

# UTILITIES
from random import randint
import ConfigParser
import time
import RPi.GPIO as GPIO
import os
import shutil
import creds
import thread

# Configuration
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
_identifiers = 'IDENTIFIERS'
_db_info = 'DB_MASTER_INFO'

# Set sample size
n = int(config.get(_core_variables, 'n_samples'))
wait_time = 1/(float(config.get(_core_variables, 'sample_rate')))

# Load credential information
db_host0 = config.get(_db_info, 'host0')
db_host1 = config.get(_db_info, 'host1')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
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

# Create queues for local-to-cloud transfer
online_flag = True
cloud_queue = []
for drone in drones_ref:
    entry_queue = []
    cloud_queue.append(entry_queue)

# POLL FLAGS
new_settings_flag = False
new_data_flag = False

# Init poll function from dbz
dbz.init_poll()
 
# Data Construction Functions
def assemble_sensor_data(d, i):
    n = 10
    # Make 10 attempts
    while(n):
        n -= 1
        the_packet = dbz.poll(i)
        if the_packet:
            if the_packet.status_flag:
                drone_data[d] = the_packet.entry
                return True
                break
    return False

def assemble_channels(i):
    new_data = False
    for k in range(num_drones):
        new_settings_data &= assemble_sensor_data(k, i)
    return new_data

def fake_assemble_sensor_data(d, i):
    drone_data[d].t = randint(1, 100)
    drone_data[d].x = randint(1, 100)
    drone_data[d].y = randint(1, 100)
    drone_data[d].z = randint(1, 100)

def fake_assemble_channels(i):
    for k in range(num_drones):
        fake_assemble_sensor_data(k, i)

def n_average(lst):
    total = 0
    for val in lst:
        total += val
    return (total/len(lst))
        
def receive_status_packet(void):
    # Proceed assembling data in all channels       
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
            # Add entry to the appropriate queue to be moved to the cloud later
            cloud_queue[j].append(drone_data[j])
            # Add function: add_entry(inst_t, x, y, z, meas_val, pts)
            dbi.add_entry(db_host1,\
                          drone_db_real,\
                          drone,\
                          drone_data[j].x,\
                          drone_data[j].y,\
                          drone_data[j].z,\
                          drone_data[j].s)
                          #n_average(channels[j].meas_val),\
                          #n_average(channels[j].pts)) 
        
# Incrementer for the average counter
m = 0

# THREAD FUNCTIONS
def thread_poll_status(void):
    new_data_flag = assemble_channels(m)
    time.sleep(wait_time)

def thread_poll_profile(void):
    new_settings_flag = db_sync.db_update(db_host0, db_host1, ground_db)
    time.sleep(2)

# INITIALIZE THREADS
thread.start_new_thread(thread_poll_status, (,))
thread.start_new_thread(thread_poll_profile, (,))



while(1):
    if(new_settings_flag):
        print "MAKE CTRL PACKET LMAO XDDD~~~~~~"
    # Wait for the rising edge of a "clock tick"
    # GPIO.wait_for_edge(CLOCK_IN, GPIO.RISING)
    #time.sleep(0.5)

    # RESPONSES
    if new_data_flag:
        receive_status_packet()
        new_data_flag = False
    if new_settings_flag:
        pass
        new_settings_flag = False
        # Send Control Packets

    # Wait for tick
    # time.sleep(wait_time)

# Online data transfer
    online_flag = db_queue.online_queue(online_flag, cloud_queue, drones_ref)

GPIO.cleanup()
##dbi.fetch_all_entries("Instrument0_data")
##dbi._exit()

