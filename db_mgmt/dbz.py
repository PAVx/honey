#! /usr/bin/python
# filename: dbz.py
# zigbee/xbee interfacing program

from xbee import XBee, ZigBee
import serial
import time
import datetime

FREQUENCY = 5
waittime = 1 / FREQUENCY
PORT = '/dev/ttyUSB1'
BAUD = 9600
ser = serial.Serial(PORT, BAUD)
xbee = XBee(ser)
ser.flushInput()
ser.flushOutput()


def main():

    """
    Sends an API AT command to read the lower-order address bits from 
    an XBee Series 1 and looks for a response
    """
    try:
        
        # Open serial port
        ser = serial.Serial('/dev/ttyUSB1', 9600)
        while(1):
                data = ser.read()
                print data
                out = ser.write("garbage")
                time.sleep(waittime)
                
        
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    
if __name__ == '__main__':
    main()
