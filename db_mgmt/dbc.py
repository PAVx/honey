#!/usr/bin/python
# filename: dbc.py
# channel struct

import ConfigParser

# Configuration
config_file_name = "dbi_conf"
config = ConfigParser.ConfigParser()
config.readfp(open(r'dbi_conf'))
_core_variables = 'CORE_VARIABLES'
# Set sample size
n = int(config.get(_core_variables, 'n_samples'))

class channel():
    time = 0
    x = 0
    y = 0
    z = 0
    meas_val = [0] * n
    pts = [0] * n

