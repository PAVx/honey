#!/usr/bin/python
# filename: dbs.py
# Declaration of channel struct

import ConfigParser

# Configuration
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
# Set sample size
m = int(config.get(_core_variables, 'n_channels'))
n = int(config.get(_core_variables, 'n_samples'))

class sensor():
    avg_data = 0
    data = [0] * n
    pts = 0

class drone_entry():
    t = 0
    x = 0
    y = 0
    z = 0
    s = []
    for i in range(m):
        sen = sensor()
        s.append(sen)


