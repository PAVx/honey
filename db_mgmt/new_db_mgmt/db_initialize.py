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
db_host0 = config.get(_db_info, 'host0')
db_host1 = config.get(_db_info, 'host1')
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

online_flag = True

# Connect to host, set cursor, create db if doesn't exist
try:
    db = MySQLdb.connect(host=db_host0, user=db_user, passwd=db_pass)
except:
    print "Unable to connect online. Going offline!"
    online_flag = False

def reset_db(db_host):
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
    cur = db.cursor()
    print("Resetting DBs...")
    # Create rover database
    cmd = ("DROP DATABASE IF EXISTS " + ground_db)
    cur.execute(cmd)
    cmd = ("CREATE DATABASE IF NOT EXISTS " + ground_db)
    cur.execute(cmd)
#may need to change collation to utf8_bin
    cmd = ("ALTER DATABASE `" + ground_db + "` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci")
    cur.execute(cmd);
    # Create drone database
    cmd = ("DROP DATABASE IF EXISTS " + drone_db)
    cur.execute(cmd)
    cmd = ("CREATE DATABASE IF NOT EXISTS " + drone_db)
    cur.execute(cmd)
#may need to change collation to utf8_bin
    cmd = ("ALTER DATABASE `" + drone_db + "` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci")
    cur.execute(cmd);
    print("DBs newly created and connected.\n")

def add_tables(db_host):
    #create rover table
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=ground_db)
    cur = db.cursor()
    cmd = ("CREATE TABLE IF NOT EXISTS `flight` (time timestamp, alert int, x_0 double, y_0 double, x_1 double, y_1 double )")
    cur.execute(cmd)
    print "Added rover table.\n"
    
    #create drone tables
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=drone_db)
    cur = db.cursor()
    for drone in drones_ref:
        #NEW DATABASE STRUCTURE
        #cmd = ("CREATE TABLE IF NOT EXISTS " + drone + "(time timestamp, loc_x int, loc_y int, loc_z int, ")
        cmd = ("CREATE TABLE IF NOT EXISTS " + drone + "(time timestamp, loc_x double, loc_y double, loc_z double, ")
        for sensor in sensors_ref:
            cmd = cmd + sensor + "_data" + " int, " + sensor + "_pts" + " int"
            if not(sensors_ref.index(sensor) == (len(sensors_ref)-1)):
                cmd = cmd + ", "
            else:
                cmd = cmd + ")"
        cur.execute(cmd)
        print "Added " + drone + "'s table."

# Main setup process        
print "Setting up database system...\n"
# If online systems are available, construct online database
if online_flag:
    print "Creating online database...\n"
    reset_db(db_host0)
    add_tables(db_host0)
# Construct local database either way
print "Creating local database...\n"
reset_db(db_host1)
add_tables(db_host1)
print "\nDatabases have been initialized! Set up done."
