#!/usr/bin/python
# filename: db_init.py
# init file used to create tables

import MySQLdb
import ConfigParser
import creds

# Get config file
print("Configuring interface program... ")
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_db_info = 'DB_MASTER_INFO'
_core_variables = 'CORE_VARIABLES'
_identifiers = 'IDENTIFIERS'
# Load credential information
db_host = config.get(_db_info, 'host')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
# Load identifiers for ground and drones
# ground_db = config.get(_db_info, 'dbin')
ground_db = config.get(_identifiers, 'rover')
drone_db = config.get(_identifiers, 'drone')
# Get number of drones in system
num_drones = int(config.get(_core_variables, 'n_drones'))
# Create drone reference table
drones_ref = []
for i in range(num_drones):
    drones_ref.append(drone_db + str(i) + "DB")
# Get number of channels per drone
num_tables = int(config.get(_core_variables, 'n_channels'))
# Create instrument reference table
channels_ref = []
for i in range(num_tables):
    channels_ref.append("channel" + str(i) + "_data")
print ("Number of channels to be configured: ", num_tables)
print("Configuration complete!\n")

# Connect to host, set cursor, create db if doesn't exist
db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
cur = db.cursor()

def reset_db():
    print("Resetting DBs...")
    # Create rover database
    cmd = ("DROP DATABASE IF EXISTS " + ground_db)
    cur.execute(cmd)
    cmd = ("CREATE DATABASE IF NOT EXISTS " + ground_db)
    cur.execute(cmd)
    for drone in drones_ref:
        cmd = ("DROP DATABASE IF EXISTS " + drone)
        cur.execute(cmd)
        cmd = ("CREATE DATABASE IF NOT EXISTS " + drone)
        cur.execute(cmd)
    print("DBs newly created and connected.\n")

def add_tables(n):
    for drone in drones_ref:
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=drone)
        cur = db.cursor()
        for ch in channels_ref:
            cmd = ("CREATE TABLE IF NOT EXISTS " + ch + "(time timestamp, loc_x int, loc_y int, loc_z int, meas_val int, pts int)")
            cur.execute(cmd)
            print "Added " + drone + "'s " + ch

# Main setup process        
print "Setting up database system..."
reset_db()
add_tables(num_tables)
print "Databases have been initialized! Set up done."
