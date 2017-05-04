#!/usr/bin/python

import MySQLdb
import creds
import time
from datetime import datetime
from random import randint
import ConfigParser

# Get config file
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_db_info = 'DB_MASTER_INFO'
_inst_conf = 'CORE_VARIABLES'
db_host0 = config.get(_db_info, 'host0')
db_host1 = config.get(_db_info, 'host1')
db_user = config.get(_db_info, 'user')
db_pass = creds.db_pass
db_inst = config.get(_db_info, 'dbin')
num_tables = config.get(_inst_conf, 'n_channels')

#SELECT * FROM `jay0` WHERE 1 ORDER BY time DESC LIMIT 3

def table_sync(updated_host, outdated_host, db, table):
    # Set the hosts and connections
    host0 = updated_host
    host1 = outdated_host
    db0 = MySQLdb.connect(host=host0, user=db_user, passwd=db_pass, db=db)
    cur0 = db0.cursor()
    db1 = MySQLdb.connect(host=host1, user=db_user, passwd=db_pass, db=db)
    cur1 = db1.cursor()

    # By default, the updated host is the newer one
    newer = host0
    older = host1
    new_cur = cur0
    old_cur = cur1

    # In case of some error, switch the newer and older
    if num_rows(host0, db, table) < num_rows(host1, db, table):
        newer = host1
        older = host0
        new_cur = cur1
        old_cur = cur0

    # Calculate the difference of entries
    diff = num_rows(newer, db, table) - num_rows(older, db, table)

    # If the difference exists, update the new table
    if diff:
        print "Changes detected: " + str(diff)
        # Select the rows to be updated, the most recent ones
        cmd = "SELECT * FROM `" + table + "` WHERE 1 ORDER BY time DESC LIMIT " + str(diff)
        new_cur.execute(cmd)
        updates = new_cur.fetchall()
        #print updates
        for update in updates:
            str_update = "Updating entry: " + str(update)
            print str_update
            # Insert new rows into the old table
            cmd = "INSERT INTO `" + table + "` VALUES " + str(string_literalize(update))
            old_cur.execute(cmd)
        db0.commit()
        db1.commit()
    else:
        print db + "->" + table + " is synced across hosts."

def num_rows(host, db, table):
    db = MySQLdb.connect(host=host, user=db_user, passwd=db_pass, db=db)
    cur = db.cursor()
    cmd = "SELECT COUNT(*) FROM `" + table + "` WHERE 1"
    cur.execute(cmd)
    the_count = int(cur.fetchone()[0])
    return the_count

def get_cols(host, db, table):
    # SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'jays' AND TABLE_NAME = 'jay0'
    db_conn = MySQLdb.connect(host=host, user=db_user, passwd=db_pass, db=db)
    cur = db_conn.cursor()
    cmd = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '" + db + "' AND TABLE_NAME = '" + table + "'"
    cur.execute(cmd)
    names = cur.fetchall()
    col_names = ()
    for name in names:
        col_names + (name[0],)
    print col_names
    return col_names

def string_literalize(update):
    literalized = ()
    for i in range(len(update)):
        literalized += (str(update[i]),)
    return literalized        

# Program to test script
table_sync(db_host0, db_host1, "jays", "jay0")
#get_cols(db_host1, "jays", "jay0")
