#! /usr/bin/python
# filename: dbz.py
# Library containing ZigBee/XBee interfacing functions with Pi

from xbee import XBee, ZigBee
from dbs import drone_entry
import serial
import time
import datetime
import ConfigParser
import a2d

#Determine number of instruments and thus the packet length
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
num_sensors = int(config.get(_core_variables, 'n_channels'))
num_samples = int(config.get(_core_variables, 'n_samples'))

#Initialize packet reading and writing parameters
#Data from sensors is currently 64 bits (8 bytes)
PACKET_LENGTH = 38
FREQUENCY = 5
waittime = 1 / FREQUENCY
PORT = '/dev/ttyUSB1'
BAUD = 9600
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
        data = ser.read(38)
        #print "HEY LOOK AT ME: " + str(a2d.convert(data))
        #print(data)
        #print("Binary encoded:")
        #bata = a2d.convert(data)
        #print(bata)
        data_rec = 1;
    except:
        pass
    finally:
        if(data_rec == 1):
            data_bytes = bytes(data)
            print(data_bytes)
            byte_array = a2d.b_array(data_bytes)
            a2d.print_array(byte_array)
            if(check_valid(byte_array) == 1):
                print("Valid start")
                
            #the_door = parse(data, i)
            #return the_door
        else:
            print("No packet received")

#Checks if status packet is received. Success = 1, Failure = 0
def check_valid(packet_start):
    if(packet_start[0] != 1):
        print("Invalid STX")
        return 0
    if(packet_start[1] != 2):
        print("Invalid SOH")
        return 0
    if(packet_start[2] != 1):
        print("Invalid Opcode")
        return 0
    if(packet_start[4] != 170):
        print("Invalid Dest")
        return 0
    return 1

        
# Obtains location, time, and sensor readings from received packet
def parse(data, i):
    ch = drone_entry()
    ch.x = a2d.convert(data[6:13])
    print "x=" + str(ch.x)
    ch.y = a2d.convert(data[14:21])
    print "y=" + str(ch.y)
    ch.z = 0
    ch.time = (data[22:29])
    ch.s[0].data[i] = a2d.convert(data[30:37])
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
