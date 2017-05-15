#!/usr/bin/python
# filename: db_main.py
# Core database program

import MySQLdb
import dbi
import dbz
from dbs import drone_entry
from random import randint
import ConfigParser
import os
import shutil
import creds

# Configuration
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
_identifiers = 'IDENTIFIERS'
_db_info = 'DB_MASTER_INFO'

# Set sample size
n = int(config.get(_core_variables, 'n_samples'))
wait_time = 1/(float(config.get(_core_variables, 'sample_rate')))

# Load credential information
db_host0 = config.get(_db_info, 'host0')
db_host1 = config.get(_db_info, 'host1')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass

def online_queue(online_flag, drone_queue, cloud_queue):
    if online_flag:
        try:
        # Connect to the cloud database
            db = MySQLdb.connect(host=db_host0, user=db_user, passwd=db_pass, db=ground_db)
            cur = db.cursor()
        except:
            print "Could not store to the cloud. Check connection."
            online_flag = False
        #try:
        #print cloud_queue
        if(online_flag and cloud_queue):
            for q in range(len(cloud_queue)):
                print "Current Queue Length: " + str(len(cloud_queue[q]))
                while(len(cloud_queue[q])):
                    drone_queue = cloud_queue[q]
                    print "From the cloud: " + str(drone_queue)
                    queued_entry = drone_queue.pop(0)
                    print "Popped entry: " + str(queued_entry)
                    dbi.add_entry(db_host0,\
                                  drone_db_real,\
                                  drones_ref[q],\
                                  queued_entry.x,\
                                  queued_entry.y,\
                                  queued_entry.z,\
                                  queued_entry.s)
                print "Queue has been cleared!"
    return online_flag
