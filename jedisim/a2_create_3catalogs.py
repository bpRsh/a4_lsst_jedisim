#!python3
# -*- coding: utf-8 -*-
""" This program creates 3 catalog files viz catalog, convolvedlist and distortedlist.

    This program also creates simdatabase/bulge_disk_f8 sample galaxies from
    combining bulge and disk components of original input galaxies with 
    algorithm $pix3[ii] = ((1-m)*pix1[ii])+(m*pix2[ii]);$
    Jedicatalog will read these files.

:Runtime:
  30 seconds (July 27, 2017)
  
"""
# Import
from __future__ import print_function, unicode_literals, division, absolute_import
import time
import re
import copy
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

def get_bulge_disk_weights():
    """Get bulge disk weights for jedicolor."""
    config = update_config()
    infile = config['jedicolor_args_infile']
    b,d = np.genfromtxt(infile,delimiter=None,usecols=(0,1),dtype=float,unpack=True)
    
    return b,d


def run_jedicolor_jedicatalog():
    config = update_config()
    b,d = get_bulge_disk_weights()
    
    # Create 302 bulge_disk_f8 sample galaxies from original galaxies.
    run_process("jedicolor", ['./executables/jedicolor',
        config['color_infile'],
        str(b[0]), str(d[0])  
        ])
    
    # Make the catalog of galaxies (three text files)
    run_process("jedicatalog", ["./executables/jedicatalog",
        config_path])

def update_outfolder_angle_catalog():
    """Update the output folder name and rotate angle by 90 degree for catalog.txt.
    
    Changes ::
    
      jedisim_out/out0/trial1_catalog.txt
      jedisim_out/out90/trial1_catalog.txt
      
      name                                              x           y   angle               redshift    pixscale    old_mag     old_rad     new_mag     new_rad     stamp_name                                  dis_name
      simdatabase/bulge_disk_f8/bdf8_255.fits	3165.936523	4969.229004	332.907227	1.500000	0.060000	24.766600	0.232020	25.990000	0.176100	jedisim_out/out0/stamp_12/stamp_12419.fits.gz	jedisim_out/out0/distorted_12/distorted_12419.fits
      simdatabase/bulge_disk_f8/bdf8_255.fits	3165.936523	4969.229004	62.90722699999998	1.500000	0.060000	24.766600	0.232020	25.990000	0.176100	jedisim_out/out90/stamp_12/stamp_12419.fits.gz	jedisim_out/out90/distorted_12/distorted_12419.fits
      
    """
          
    config = update_config()
    ifile = config['catalog_file']
    ofile = config['90_catalog_file']
    old_catalog_file = open(ifile, 'r')
    catalog_file = open(ofile, 'w')
    angle0, angle90 = 0, 0
    for old_line in old_catalog_file:
        l = old_line.split("\t")
        angle0 = float(l[3])
        angle90 = angle0 + 90
        if angle90 >= 360:
            angle90 -= 360
        l[3] = str(angle90)
        l[-1] = l[-1].replace(config['output_folder'], config['90_output_folder'])
        l[-2] = l[-2].replace(config['output_folder'], config['90_output_folder'])
        line = "\t".join(l)
        catalog_file.write(line)
        
    # Debug
    # print('last angle0 = ', angle0)
    # print('last angle90 = ', angle90)
    old_catalog_file.close()
    catalog_file.close()


def update_outfolder_convolvedlist():
    """Update the output folder name in convilvedlist.txt.
    
    Changes ::
    
      jedisim_out/out0/trial1_convolvedlist.tx
      jedisim_out/out90/trial1_convolvedlist.txt
      
      jedisim_out/out0/convolved/convolved_band_0.fits
      jedisim_out/out90/convolved/convolved_band_0.fits
      
    """
    config = update_config()
    old_convolvedlist_file = open(config['convolvedlist_file'], 'r')
    convolvedlist_file = open(config['90_convolvedlist_file'], 'w')
    for old_line in old_convolvedlist_file:
        line = old_line.replace(config['output_folder'],
                                config['90_output_folder'])
        convolvedlist_file.write(line)
    old_convolvedlist_file.close()
    convolvedlist_file.close()


def update_outfolder_distortedlist():
    """Update the output folder name in distortedlist.txt.
    
    Changes ::
    
      jedisim_out/out0/trial1_distortedlist.txt
      jedisim_out/out90/trial1_distortedlist.txt
      
      jedisim_out/out0/distorted_0/distorted_0.fits
      jedisim_out/out90/distorted_0/distorted_0.fits
            
    """
    config = update_config()
    old_distortedlist_file = open(config['distortedlist_file'], 'r')
    distortedlist_file = open(config['90_distortedlist_file'], 'w')
    for old_line in old_distortedlist_file:
        line = old_line.replace(config['output_folder'],
                                config['90_output_folder'])
        distortedlist_file.write(line)
    old_distortedlist_file.close()
    distortedlist_file.close()


def main():
    """Run main function."""
    
    # Create 3 catalogs.
    run_jedicolor_jedicatalog()
    
    # Update 3 catalogs for rotated case.
    update_outfolder_angle_catalog()
    update_outfolder_convolvedlist()
    update_outfolder_distortedlist()


if __name__ == "__main__":
    # Run main
    main()

    # # Beginning time
    # program_begin_time = time.time()
    # begin_ctime        = time.ctime()
    # 
    # #  Run the main program
    # main()
    # 
    # # Print the time taken
    # program_end_time = time.time()
    # end_ctime        = time.ctime()
    # seconds          = program_end_time - program_begin_time
    # m, s             = divmod(seconds, 60)
    # h, m             = divmod(m, 60)
    # d, h             = divmod(h, 24)
    # print("nBegin time: ", begin_ctime)
    # print("End   time: ", end_ctime, "\n")
    # print("Time taken: {0: .0f} days, {1: .0f} hours, \
    #   {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))



