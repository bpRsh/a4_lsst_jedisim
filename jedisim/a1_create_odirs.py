#!python3
# -*- coding: utf-8 -*-

# Imports
from __future__ import print_function, unicode_literals, division, absolute_import
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
import numpy as np
from util import replace_outfolder, run_process

# Global Variables
config_path = "physics_settings/config.sh"


def config_dict(config_path):
    """Create a dictionary of variables from input file."""

    # Parse config file and make a dictionary
    with open(config_path, 'r') as f:
        config = {}
        string_regex = re.compile('"(.*?)"')
        value_regex = re.compile('[^ |\t]*')

        for line in f:
            if not line.startswith("#"):
                temp = []
                temp = line.split("=")
                if temp[1].startswith("\""):
                    config[temp[0]] = string_regex.findall(temp[1])[0]
                else:
                    config[temp[0]] = value_regex.findall(temp[1])[0]
    return config



# Create config dictionary
def update_config():
    config = config_dict(config_path)
    config_record = copy.deepcopy(config)
    prefix = config['output_folder'] + config['prefix'] 
    keys = ['HST_image',            'HST_convolved_image',
            'LSST_averaged_image',  'LSST_averaged_noised_image',
            'catalog_file',         'dislist_file',
            'distortedlist_file',   'convolvedlist_file']
    for key in keys:
        config[key] = prefix + config[key]
        
    # Add keys for 90 degree rotated case
    pre = '90_' + config_record['prefix']
    for key in keys:
        key90 = '90_' + key
        config[key90] = config['90_output_folder'] + pre + config_record[key]
        
    return config


def replace_outfolders_jedi():
    """Replace old output folders before running new simulation.
    
    :Example:
    
       jedisim_out/out0
       
       jedisim_out/rescaled_lsst
       
       simdatabase/bulge_disk_f8
       
       jedisim_out/out0/convolved/
       
       jedisim_out/out0/distorted_0_to_12/
       
       jedisim_out/out0/stamp_0_to_12/
       
    """
    config = update_config()
    outfolders = [config["output_folder"][0:-1],
                  config["rescaled_outfolder"],
                  config["color_outfolder"],
                  config['output_folder']+ 'convolved/'
                  ]
    for outfolder in outfolders:
        replace_outfolder(outfolder)
        
    # Make stamps and distorted folders
    # e.g. jedisim_out/out0/stamp_0 to stamp_12
    # e.g. jedisim_out/out0/distorted_0 to stamp_12
    for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
        postage_path   = config['output_folder'] + "stamp_"     + str(x)
        distorted_path = config['output_folder'] + "distorted_" + str(x)
        if not os.path.exists(postage_path):
            os.makedirs(postage_path)
        if not os.path.exists(distorted_path):
            os.makedirs(distorted_path)

def d90_replace_outfolders_jedi():
    """Replace old output folders before running new simulation.
    
    :Example:
    
       jedisim_out/out90
       
       jedisim_out/rescaled_lsst90
       
       jedisim_out/out90/convolved/
       
       jedisim_out/out90/distorted_0_to_12/
       
       jedisim_out/out90/stamp_0_to_12/
       
    """
    config = update_config()
    outfolders = [config["90_output_folder"],
                  config["rescaled_outfolder90"],
                  config['90_output_folder']+ 'convolved/'
                  ]
    for outfolder in outfolders:
        replace_outfolder(outfolder)
        
    # Make stamps and distorted folders
    # e.g. jedisim_out/out90/stamp_0 to stamp_12
    # e.g. jedisim_out/out90/distorted_0 to stamp_12
    for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
        postage_path   = config['90_output_folder'] + "stamp_"     + str(x)
        distorted_path = config['90_output_folder'] + "distorted_" + str(x)
        if not os.path.exists(postage_path):
            os.makedirs(postage_path)
        if not os.path.exists(distorted_path):
            os.makedirs(distorted_path)
            

def main():
    """Run main function."""
    
    # Create output folders.
    replace_outfolders_jedi()
    
    # Create output dirs for 90 degree roated case
    d90_replace_outfolders_jedi()
    
    # Testing
    config = update_config()
    

if __name__ == "__main__":
    #  Run the main program
    main()



