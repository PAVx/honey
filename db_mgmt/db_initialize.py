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
db_host = config.get(_db_info, 'host')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
db_inst = config.get(_db_info, 'dbin')
num_tables = int(config.get(_core_variables, 'n_channels'))
print ("Number of instruments to be configured: ", num_tables)
print("Configuration complete!\n")

# Connect to host, set cursor, create db if doesn't exist
db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass)
cur = db.cursor()

def reset_db():
    print("Resetting DB...")
    cmd = ("DROP DATABASE IF EXISTS " + db_inst)
    cur.execute(cmd)
    cmd = ("CREATE DATABASE IF NOT EXISTS " + db_inst)
    cur.execute(cmd)
    print("DB newly created and connected.\n")

def add_tables(n):
    for i in range(n):
        table_name = ("Instrument" + str(i) + "_data")
        cmd = ("CREATE TABLE IF NOT EXISTS " + table_name + "(time timestamp, loc_x int, loc_y int, loc_z int, meas_val int, pts int)")
        cur.execute(cmd)
        print("Added ", table_name)
        
reset_db()
db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_inst)
cur = db.cursor()
add_tables(num_tables)
