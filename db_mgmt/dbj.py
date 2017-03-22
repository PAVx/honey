# filename: json_gen2.py
# Experimenting with json API

import os
import shutil
import ConfigParser
import json
#For debug
from random import randint
import time

##################################
#Uncomment when integrated to Pi3#
##################################
#Determine the number of sensors
#config_file_name = "dbi_conf"
#config = ConfigParser.ConfigParser()
#config.readfp(open(r'dbi_conf'))
#_core_variables = 'CORE_VARIABLES'
#num_sensors = int(config.get(_core_variables, 'n_channels'))

num_sensors = 1
max_entries = 20

datafile = "JSONData.json"

#Initialize the JSON file
def jfile_init():
	if(os.path.isfile(datafile)):
            
		os.remove(datafile)
	jfile = open(datafile, 'w')
	jfile.write("[\n [" + "\n"
                    + " \n]")
	jfile.close()

#Read the entire JSON file and save all but the last line
def jfile_scan(filename):
        readfile = open(filename)
        lines = readfile.readlines()
        readfile.close()
        lines = lines[:-1]
        return lines

#Add data_packet to the end of the JSON file. Seems slow right now
def jfile_addentry(filename, data_packet):
    data = {}
    data['time'] = int(data_packet[0:2])
    for i in range(num_sensors):
        data['sensor'+str(i)] = int(data_packet[i+2])
    #data['sensor0'] = 9
        json_data = (json.dumps(data,
                indent=4, separators=(',', ': ')))
    #print json_data
    lines = jfile_scan(filename)
    jfile = open(filename, 'w')
    jfile.writelines([item for item in lines])
    #jfile.write("\n")
    jfile.write(json_data)
    jfile.write("\n ]\n]")
    jfile.close()

def jfile_addcomma(filename):
    #jfile = open(filename)
    lines = jfile_scan(filename)
    jfile = open(filename, 'w')
    jfile.writelines([item for item in lines[:-1]])
    jfile.write(",\n\n")
    jfile.close()

def jfile_addcomma2(filename):
    lines = jfile_scan(filename)
    jfile = open(filename, 'w')
    jfile.writelines([item for item in lines[:-1]])
    jfile.write("}\n,\n\n")
    jfile.close()
    

#Correctly formats the last entry in the JSON file
def jfile_update(filename):
        lines = jfile_scan(filename)
        jfile = open(filename, 'w')
        jfile.writelines([item for item in lines[:-1]])
        jfile.write("\n ]\n]")
        jfile.close()
        
        
#Return a line count of the file
def file_len(filename):
        jfile = open(filename)
        for i, l in enumerate(jfile):
                pass
        return i+1
        jfile.close()

#Remove the oldest (first) entry
def jfile_pop(filename):
        entry_len = 4 + num_sensors
        jfile = open(filename)
        lines = jfile.readlines()
        first_half = lines[:3]
        second_half = lines[(3+entry_len):-1]
        new_list = first_half + second_half
        jfile.close()
        jfile = open(filename, 'w')
        jfile.writelines([item for item in new_list])
        jfile.close()        
	

#if __name__ == '__main__':
print "Here i come i am cinnamon"
jfile_init()
#jfile_addentry(datafile, packet)
#jfile_addcomma(datafile)
max_len = 5 + (max_entries *(3+num_sensors)) + ((max_entries)-1)
i = 0
file_full = 0
state = 0
while(1):
        try:
                packet = "%02d" % (i) + str(randint(0,9)) \
                         + str(randint(0,9)) + str(randint(0,9))
                i += 1
                if(file_len(datafile) >= max_len):
                        file_full = 1
                #If the file is not full, just add an entry
                if(file_full == 0):
                        jfile_addentry(datafile, packet)
                        jfile_addcomma(datafile)
                        
                #If file is full, add entry, pop the oldest value, and format
                else:
                        state = 0
                        jfile_pop(datafile)
                        state = 1
                        jfile_addcomma2(datafile)
                        state = 2
                        jfile_addentry(datafile, packet)
                        #jfile_update(datafile)                       
                        #jfile_update(datafile)
                        #time.sleep(1)
##                        jfile_pop(datafile)
##                        jfile_addentry(datafile, packet)
##                        jfile_update(datafile)
                        #break;
        except KeyboardInterrupt:
                break
                if(state == 1):
                        jfile_addcomma2(datafile)
                        jfile_addentry(datafile, packet)
                if(state == 2):
                        jfile_addentry(datafile, packet)
        
