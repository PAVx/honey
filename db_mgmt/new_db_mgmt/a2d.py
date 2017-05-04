#!/usr/bin/python

def convert(_in):
    sum = 0
    l = len(_in)
    for c in range(len(_in)):
        sum += ord(_in[c])*(2**(8*(l-1-c)))
    return sum

def b_array(packet):
    byte_array = []
    for a in packet:
        val = int(ord(a))
        byte_array.append(val)
    return byte_array

def print_array(byte_array):
    for a in byte_array:
        print(a)

#def parse_loc(byte_array):


#def parse_data(byte_array):
