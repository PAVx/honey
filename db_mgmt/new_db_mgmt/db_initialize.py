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
ground_db = config.get(_identifiers, 'rover')
drone_t = config.get(_identifiers, 'drone')
drone_db = drone_t + "s"

# Get number of drones in system
num_drones = int(config.get(_core_variables, 'n_drones'))
# Create drone reference table
drones_ref = []
for i in range(num_drones):
    drones_ref.append(drone_t + str(i))
    
# Get number of channels per drone
num_sensors = int(config.get(_core_variables, 'n_channels'))
# Create instrument reference table
sensors_ref = []
for i in range(num_sensors):
    sensors_ref.append("sensor" + str(i))
print ("Number of sensor channels to be configured: ", num_sensors)
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
    # Create rover database
    cmd = ("DROP DATABASE IF EXISTS " + drone_db)
    cur.execute(cmd)
    cmd = ("CREATE DATABASE IF NOT EXISTS " + drone_db)
    cur.execute(cmd)
    print("DBs newly created and connected.\n")

def add_tables():
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=drone_db)
    cur = db.cursor()
    for drone in drones_ref:
        #NEW DATABASE STRUCTURE
        cmd = ("CREATE TABLE IF NOT EXISTS " + drone + "_data" + "(time timestamp, loc_x int, loc_y int, loc_z int, ")
        for sensor in sensors_ref:
            cmd = cmd + sensor + "_data" + " int, " + sensor + "_pts" + " int"
            if not(sensors_ref.index(sensor) == (len(sensors_ref)-1)):
                cmd = cmd + ", "
            else:
                cmd = cmd + ")"
        cur.execute(cmd)
        print "Added " + drone + "'s table."

# Main setup process        
print "Setting up database system..."
reset_db()
add_tables()
print "\nDatabases have been initialized! Set up done."
