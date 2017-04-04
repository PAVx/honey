# filename: dbj.py
# Create data file to be visualized

import MySQLdb
import creds
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
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_db_info = 'DB_MASTER_INFO'
_core_variables = 'CORE_VARIABLES'
#Create database interfacing variables
db_host = config.get(_db_info, 'host')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
num_sensors = int(config.get(_core_variables, 'n_channels'))

num_sensors = 1
max_entries = 20
db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
cur = db.cursor()
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

#Add data_packet to the end of the JSON file. Seems slow right now
def jfile_addentry2(filename, data_packet, k):
    data = {}
    dlen = len(data_packet)
    flen = dlen / 2
    data['time'] = k
    for i in range(num_sensors):
        data['sensor'+str(i)] = int(data_packet[0:flen])
        data['pts'+str(i)] = int(data_packet[flen:])
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

#Obtain the last n number of entries for a sensor from the specified table and place them in the JSON file
def json_pull(n, table, sensor_num, datafile):
        # Point to correct database
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db="jays")
        cur = db.cursor()
        # Get the last n entries
        fetch_cmd = ("SELECT `sensor"+str(sensor_num)+"_data`, `sensor"+str(sensor_num)+"_pts` FROM `jay"+str(table)+"` ORDER BY time ASC LIMIT " + str(n))
        cur.execute(fetch_cmd)
        # Obtain the dataset object
        dataset = cur.fetchall()
        # Print to ensure it is correct
        _print(dataset)
        k = 0
        # Each row is a DB entry
        for row in dataset:
            row_str = ""
            # Obtain each field value and add it to the packet string
            for col in row:
                field = str(col)
                row_str += field
            #Print the packet to debug
            print(row_str)
            jfile_addentry2(datafile, row_str, k)
            k += 1
            #Every entry except final one has a comma
            if(k < 20):
                jfile_addcomma(datafile)
            else:
                jfile_update(datafile)
     

def _print(result):
        print_string = "|"
        for row in result:
                print_string = "| "
                for col in row:
                        this_string = str(col)
                        that_string = " | "
                        print_string = print_string  + this_string + that_string
                print print_string	

#if __name__ == '__main__':
jfile_init()
#jfile_addentry(datafile, packet)
#jfile_addcomma(datafile)
max_len = 5 + (max_entries *(3+num_sensors)) + ((max_entries)-1)
i = 0
file_full = 0
state = 0
json_pull(20, 0, 0, datafile)
##while(1):
##        try:
##                packet = "%02d" % (i) + str(randint(0,9)) \
##                         + str(randint(0,9)) + str(randint(0,9))
##                i += 1
##                if(file_len(datafile) >= max_len):
##                        file_full = 1
##                #If the file is not full, just add an entry
##                if(file_full == 0):
##                        jfile_addentry(datafile, packet)
##                        jfile_addcomma(datafile)
##                        
##                #If file is full, add entry, pop the oldest value, and format
##                else:
##                        state = 0
##                        jfile_pop(datafile)
##                        state = 1
##                        jfile_addcomma2(datafile)
##                        state = 2
##                        jfile_addentry(datafile, packet)
##                        #jfile_update(datafile)
##                        
##        except KeyboardInterrupt:
##                break
##                if(state == 1):
##                        jfile_addcomma2(datafile)
##                        jfile_addentry(datafile, packet)
##                if(state == 2):
##                        jfile_addentry(datafile, packet)
