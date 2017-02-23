#! /usr/bin/python
# filename: dbz.py
# zigbee/xbee interfacing program

from xbee import XBee, ZigBee
from dbc import channel
import serial
import time
import datetime

PACKET_LENGTH = 36
FREQUENCY = 5
waittime = 1 / FREQUENCY
PORT = '/dev/ttyUSB0'
BAUD = 9600
ser = serial.Serial(PORT, BAUD)
xbee = XBee(ser)
ser.flushInput()
ser.flushOutput()
# Construct the door
the_door = channel()


def poll(i):

    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    try:
        data = ser.read(PACKET_LENGTH)
        the_door = parse(data, i)
        return the_door
        
    except KeyboardInterrupt:
        break

def parse(data, i):
    ch = channel()
    ch.x = int(data[7:10])
    ch.y = int(data[11:14])
    ch.z = int(data[15:18])
    ch.time = int(data[19:23])
    ch.meas_val[i] = int(data[24:33])
    ch.pts[i] = 0
    return ch

def main():

    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    try:
        
        # Open serial port
        # ser = serial.Serial('/dev/ttyUSB0', 9600)
        while(1):
                the_door = ser.read(7)
                
                print the_door
                out = ser.write("HI JESS ")
                time.sleep(waittime)
                
        
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    
if __name__ == '__main__':
    main()
