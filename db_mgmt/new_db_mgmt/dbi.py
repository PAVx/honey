#!/usr/bin/python
# filename: dbi.py
# simple script testing out our wrapper program

import MySQLdb
import creds
import time
import datetime
from random import randint
import ConfigParser
import os
import errno
import shutil
 

# Get config file
print("Configuring interface program... ")
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_db_info = 'DB_MASTER_INFO'
_inst_conf = 'CORE_VARIABLES'
db_host = config.get(_db_info, 'host')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
db_inst = config.get(_db_info, 'dbin')
num_tables = config.get(_inst_conf, 'n_channels')

# Get number of channels per drone
num_sensors = int(config.get(_inst_conf, 'n_channels'))
# Create instrument reference table
sensors_ref = []
for i in range(num_sensors):
    sensors_ref.append("sensor" + str(i))
print("Configuration complete!\n")

# Initialize the database object and cursor
db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
cur = db.cursor()

# Add entry function
def add_entry(target_db, target_t, x, y, z, sensordata_list, sensorpts_list):
        # Point to correct database
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=target_db)
        cur = db.cursor()
        #print("Adding entry... ")
        
        # Get time
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        # Build query
        sensor_str = ""
        add_data = (
                "INSERT INTO `" + target_t + "`(`time`, `loc_x`, `loc_y`, `loc_z`, "
                )
        second_half = "VALUES (%s, %s, %s, %s, "
        for sensor in sensors_ref:
                sensor_str =  sensor_str + "`" + sensor + "_data" + "`, `" + sensor + "_pts" + "`"
                second_half = second_half + "%s, %s"
                if not(sensors_ref.index(sensor) == (len(sensors_ref) - 1)):
                        sensor_str = sensor_str + ", "
                        second_half = second_half + ", "
                else:
                        sensor_str = sensor_str + ")"
                        second_half = second_half + ")"
        add_data = add_data + sensor_str + second_half

        # Assemble and insert data
        value_data = (timestamp, x, y, z)
        # Create measurement value and points part of argument
        for y in range(len(sensors_ref)):
                value_data = value_data + (sensordata_list[y], sensorpts_list[y])
        #print(add_data)
        #print(value_data)

        # Execute in SQL and commit to DB
        cur.execute(add_data, value_data)
        db.commit()
        print("Entry added to " + target_db + " -> " + target_t + "!")

def fetch_last_entry(target_db, table):
        # Point to correct database
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=target_db)
        cur = db.cursor()
        # Get the last entry
        print ("Most recent entry:\n    ")
        fetch_cmd = ("SELECT `time`, `loc_x`, `loc_y`, `loc_z`, `meas_val`, `pts` FROM `Instrument0_data` ORDER BY time DESC LIMIT 1")
        cur.execute(fetch_cmd)
        _print(cur)

def fetch_all_entries(target_db, target_t):
        # Point to correct database
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=target_db)
        cur = db.cursor()
        # Get all entries
        print ("ALL ENTRIES FOR " + target_db + " -> " + target_t + ":\n")
        fetch_cmd = ("SELECT * FROM `" + target_t + "` ORDER BY time")
        cur.execute(fetch_cmd)
        _print(cur)

def write_all_entries(target_db, target_t, log):
        # Point to correct database
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=target_db)
        cur = db.cursor()
        # Get all entries
        print ("ALL ENTRIES FOR " + target_db + " -> " + target_t + ":\n    ")
        fetch_cmd = ("SELECT * FROM `" + target_t + "` ORDER BY time")
        cur.execute(fetch_cmd)
        _write_channel(cur, log)

def manual_mysql(command):
        cmd = command
        cur.execute(cmd)
        db.commit()
        
# DB close function
def _exit(target_db):
        # Point to correct database
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=target_db)
        cur = db.cursor()
        # Close database
        cur.close()
        db.close()


def _print(result_cur):
        result = result_cur.fetchall()
        print_string = "|"
        for row in result:
                print_string = "| "
                for col in row:
                        this_string = str(col)
                        that_string = " | "
                        print_string = print_string  + this_string + that_string
                print print_string
# Write to a channel file
def _write_channel(result_cur, log):       
        result = result_cur.fetchall()
        #print_string = "|"
        for row in result:
                print_string = ""
                for col in row:
                        this_string = str(col)
                        that_string = ","
                        print_string = print_string  + this_string + that_string
                log.write(print_string)
                log.write("\n")

# Create a folder for the specified drone
def _make_folder(folder_name) :
        if not os.path.exists(folder_name):
                os.makedirs(folder_name)

# RUN PROGRAM
sample_meas = (43,42,41,39)
sample_pts = (1,2,3,5)
add_entry("jays", "jay0", randint(0,9), randint(0,9), randint(0,9), sample_meas, sample_pts)
fetch_all_entries("jays", "jay0")

