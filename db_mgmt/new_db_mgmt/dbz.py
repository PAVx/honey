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
import struct

#Determine number of instruments and thus the packet length
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
num_sensors = int(config.get(_core_variables, 'n_channels'))
num_samples = int(config.get(_core_variables, 'n_samples'))

#Initialize packet reading and writing parameters
#Data from sensors is currently 64 bits (8 bytes)
PACKET_LENGTH = 30
FREQUENCY = 5
waittime = 1 / FREQUENCY
PORT = '/dev/ttyUSB0'
BAUD = 9600
ser = serial.Serial(PORT, BAUD)
xbee = XBee(ser)
ser.flushInput()
ser.flushOutput()
# Construct the door
global the_door

class packet():
    status_flag = 0
    src = 0
    dest = 0
    entry = drone_entry()
    roll = 0
    pitch = 0
    batt = 0

def init_poll():
    # Construct the door
    the_door = packet()
    
# Reads in data packet from serial port, parses retrieved packet
def poll(i):
    data_rec = False
    try:
        data = ser.read(PACKET_LENGTH)
        #print(data)
        data_rec = True
    except:
        pass
    finally:
        if data_rec:
            data_bytes = bytes(data)
            #print(data_bytes)
            byte_array = a2d.b_array(data_bytes)
            #a2d.print_array(byte_array)
            if check_valid(byte_array):
                print("Valid start")
                the_door = parse(byte_array, i)
                return the_door
            else:
                return False
        else:
            print("No packet received")

#Checks if status packet is received. Success = 1, Failure = 0
def check_valid(packet_start):
    if(packet_start[0] != 1):
        #print("Invalid SOH")
        return False
    if(packet_start[1] != 2):
        #print("Invalid STX")
        return False
    if(packet_start[2] != 1):
        #print("Invalid Status Packet")
        return False
    if(packet_start[4] != 170):
        #print("Invalid Dest")
        return False
    return True

        
# Obtains location, time, and sensor readings from received packet
def parse(data, i):
    # Construct packet
    pac = packet()
    # Set flag to be true automatically as this is called after a check_valid
    pac.status_flag = True
    # Populate src and dest
    pac.src = (data[3])
    pac.dest = (data[4])
    # Parse data
    pac.entry.y = parse_loc(data[5:9])
    print "x=" + str(pac.entry.y)
    pac.entry.x = parse_loc(data[9:13])
    print "y=" + str(pac.entry.x)
    pac.entry.time = parse_dub(data[13:21])
    pac.entry.z = parse_int(data[21:23])
    print "z=" + str(pac.entry.z)
    pac.roll = parse_int(data[23:25])
    pac.pitch = parse_int(data[25:27])
    pac.batt = parse_int(data[27])
    #pac.entry.s[0].data[i] = parse_dub(data[21:29])
    pac.entry.s[0].data[i] = data[28]
    batt = data[27]
    print "batt=" + str(pac.batt)
    print "##BATTERY LEVEL##:", str(batt)
    print "data for ", i, ": ", pac.entry.s[0].data[i]
    # Return packet
    return pac

def parse_dub(byte_array):
    #print "byte_array: ", byte_array
    hex_string = ""
    for i in range(len(byte_array)):
        #print "iter: ", i
        hex_val = hex(byte_array[i])
        hex_string += hex_val[2:].zfill(2)
    #print("DUB: 0x"+hex_string)
    parsed = struct.unpack('!d', hex_string.decode('hex'))[0]
    return parsed

def parse_loc(byte_array):
    print "byte_array: ", byte_array
    hex_string = ""
    for i in range(len(byte_array)):
        #print "iter: ", i
        hex_val = hex(byte_array[i])
        hex_string += hex_val[2:].zfill(2)
    #print("0x"+hex_string)
    parsed = struct.unpack('!f', hex_string.decode('hex'))[0]
    return parsed

def parse_int(byte_array):
    #print "byte_array: ", byte_array
    hex_string = ""
    l = 0
    try:
        l = len(byte_array)
    except TypeError:
        return byte_array
    for i in range(l):
        #print "iter: ", i
        hex_val = hex(byte_array[l-i-1])
        hex_string += hex_val[2:].zfill(2)
    #print("0x"+hex_string)
    parsed = struct.unpack('H', hex_string.decode('hex'))[0]
    return parsed
##    data_sum = 0
##    l = 0
##    try:
##        l = len(byte_array)
##    except:
##        len = 1
##    for i in range(l):
##        data_sum += (byte_array[i] * pow(2, 8*(l-(i+1))))
        

# MAIN FUNCTION: takes in sample iterationreturns false OR the packet class
def get_packet(i):
    return poll(i)
    
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
