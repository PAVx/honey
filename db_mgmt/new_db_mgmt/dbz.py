#! /usr/bin/python
# filename: dbz.py
# Library containing ZigBee/XBee interfacing functions with Pi

from xbee import XBee, ZigBee
from dbs import drone_entry
import serial
import time
import datetime
import ConfigParser

#Determine number of instruments and thus the packet length
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
num_sensors = int(config.get(_core_variables, 'n_channels'))
num_samples = int(config.get(_core_variables, 'n_samples'))

#Initialize packet reading and writing parameters
#Data from sensors is currently 64 bits (8 bytes)
PACKET_LENGTH = 23 + (8*num_sensors)
FREQUENCY = 5
waittime = 1 / FREQUENCY
PORT = '/dev/ttyUSB0'
#Change this when we decide for sure on a baud rate
#BAUD = 9600
BAUD = 38400
ser = serial.Serial(PORT, BAUD)
xbee = XBee(ser)
ser.flushInput()
ser.flushOutput()
# Construct the door
global the_door

def init_poll():
    # Construct the door
    the_door = drone_entry()
    
# Reads in data packet from serial port, parses retrieved packet
def poll(i):
    data_rec = 0;
    try:
        ser.flushInput()
        data = ser.read(PACKET_LENGTH)
        data_rec = 1;
    except:
        pass
    finally:
        if(data_rec == 1):
            the_door = parse(data, i)
            return the_door
        else:
            print("No packet received")

        
# Obtains location, time, and sensor readings from received packet
def parse(data, i):
    ch = drone_entry()
    ch.x = int(data[6:10])
    ch.y = int(data[10:14])
    ch.z = int(data[14:18])
    ch.time = int(data[18:23])
    ch.s[0].data[i] = int(data[23:])
    return ch

def parse2(data, i):
    ch = channel()
    ch.x = int(data[7:11])
    ch.y = int(data[11:15])
    ch.z = int(data[15:19])
    ch.time = int(data[19:24])
    ch.meas_val[i] = int(data[24:-1])
    ch.pts[i] = 0
    return ch

# Example code used to create functions in this file. Not relevant anymore.
def main():

    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    try:
        
        # Open serial port
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        while(1):
                ser.flushInput()
                the_door = ser.read(PACKET_LENGTH) 
                
                print the_door
                #out = ser.write("HI JESS ")
                time.sleep(waittime)
                
        
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    
if __name__ == '__main__':
    main()
    #poll2()
    #init_poll()
