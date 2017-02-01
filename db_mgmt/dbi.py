#!/usr/bin/python
# filename: dbi.py
# simple script testing out our wrapper program

import MySQLdb
import creds
import time
import datetime
from random import randint
import ConfigParser

# Get config file
#print("Configuring interface program... ")
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_db_info = 'DB_MASTER_INFO'
db_host = config.get(_db_info, 'host')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
db_inst = config.get(_db_info, 'dbin')
#print("Configuration complete!\n")

# Initialize the database object and cursor
db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_inst)
cur = db.cursor()

# Add entry function
def add_entry(inst_t, x, y, z, meas_val, pts):
        #print("Adding entry... ")
	# Get time
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	# Build query
	add_data = (
		"INSERT INTO `" + inst_t + "`(`time`, `loc_x`, `loc_y`, `loc_z`, `meas_val`, `pts`)"
		"VALUES (%s, %s, %s, %s, %s, %s)"
	)
	#insert data
	value_data = (timestamp, x, y, z, meas_val, pts)
	#print(value_data)	
	cur.execute(add_data, value_data)
	db.commit()
	print("Entry added.\n")

def fetch_last_entry(table):
        print ("Most recent entry:\n    ")
        fetch_cmd = ("SELECT `time`, `loc_x`, `loc_y`, `loc_z`, `meas_val`, `pts` FROM `Instrument0_data` ORDER BY time DESC LIMIT 1")
        cur.execute(fetch_cmd)
        _print(cur)

def fetch_all_entries(table):
        print ("List all entries:\n    ")
        fetch_cmd = ("SELECT * FROM `Instrument0_data` ORDER BY time")
        cur.execute(fetch_cmd)
        _print(cur)

def manual_mysql(command):
        cmd = command
        cur.execute(cmd)
        db.commit()
        
# DB close function
def _exit():
	cur.close()
	db.close()


def _print(result_cur):
        result = cur.fetchall()
        print_string = "|"
        for row in result:
                print_string = "| "
                for col in row:
                        this_string = str(col)
                        that_string = " | "
                        print_string = print_string  + this_string + that_string
                print print_string

# RUN PROGRAM
##add_entry("Instrument0_data", randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9))
##fetch_all_entries("Instrument0_data")
##_exit()
