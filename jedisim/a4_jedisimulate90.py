#!python3
# -*- coding: utf-8 -*-
"""This program is for simulation for 90 degree rotated case.

:Runtime:

  2 hr 45 minutes for 21 for loop and one run (July 28, 2017)
  
"""

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
    # Imports
    import re

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
    

def d90_psf_rescaled_lsst_outfile_lst():
    psf90 =  ['psf/psf%d.fits' % i for i in range(21)]
    rescaled_lsst_outfile90 = ['jedisim_out/rescaled_lsst90/rescaled_lsst90_%d.fits'
                              % i for i in range(21) ]
                              
    return psf90, rescaled_lsst_outfile90


def get_bulge_disk_weights():
    config = update_config()
    infile = config['jedicolor_args_infile']
    b,d = np.genfromtxt(infile,delimiter=None,usecols=(0,1),dtype=float,unpack=True)
    
    return b,d

def d90_run_7programs_loop():
    config = update_config()
    b, d = get_bulge_disk_weights()
    psf90, rescaled_lsst_outfile90 = d90_psf_rescaled_lsst_outfile_lst()
    for i in range(0, 21):
    # for i in range(0, 1):

        # The jedicolor creates 302 fitsfiles inside config['output_folder_bulge']
        run_process("jedicolor", ['./executables/jedicolor',
                                  config['color_infile'],
                                  str(b[i]), str(d[i])
                                  ])

        # Make postage stamp images that fit the catalog parameters
        run_process("jeditransform", ['./executables/jeditransform',
                                      config['90_catalog_file'],
                                      config['90_dislist_file']
                                      ])

        # Lens the galaxies one at a time
        run_process("jedidistort", ['./executables/jedidistort',
                                    config['nx'],
                                    config['ny'],
                                    config['90_dislist_file'],
                                    config['lenses_file'],
                                    config['pix_scale'],
                                    config['lens_z']
                                    ])

        # Combine the lensed galaxies onto one large image
        run_process("jedipaste", ['./executables/jedipaste',
                                  config['nx'],
                                  config['ny'],
                                  config['90_distortedlist_file'],
                                  config['90_HST_image']
                                  ])

        # Convonlve the large image with the PSF.
        # This creates one image for each band of the image.
        run_process("jediconvolve", ['./executables/jediconvolve',
                                     config['90_HST_image'],
                                     psf90[i],
                                     config['90_output_folder'] + 'convolved/'
                                     ])

        # Combine each band into a single image
        run_process("jedipaste", ['./executables/jedipaste',
                                  config['nx'],
                                  config['ny'],
                                  config['90_convolvedlist_file'],
                                  config['90_HST_convolved_image']
                                  ])

        # Scale the image down from HST to LSST scale and trim the edges.
        run_process("jedirescale", ['./executables/jedirescale',
                                    config['90_HST_convolved_image'],
                                    config['pix_scale'],
                                    config['final_pix_scale'],
                                    config['x_trim'],
                                    config['y_trim'],
                                    rescaled_lsst_outfile90[i]
                                    ])


def d90_average21_and_add_noise():
    config = update_config()
    run_process("jediaverage", ['./executables/jediaverage',
        config['rescaled_lsst_outfile90'],
        config['90_LSST_averaged_image']
        ])

    # Add noise to averaged file.
    run_process("jedinoise", ['./executables/jedinoise',
        config['90_LSST_averaged_image'],
        config['exp_time'],
        config['noise_mean'],
        config['90_LSST_averaged_noised_image']
        ])

    # Create monochromatic psf
    run_process("jedinoise", ['./executables/jedinoise',
        config["monochromatic_infits90"],                          
        config['exp_time'],
        config['noise_mean'],
        config["monochromatic_outfits90"]
        ])
                              

def main():
    """Run main function."""
    
    # Run 7 programs in the loop
    d90_run_7programs_loop()
    
    # Average 21 outputs and add noise to it.
    d90_average21_and_add_noise()

    

if __name__ == "__main__":
    # Beginning time
    program_begin_time = time.time()
    begin_ctime        = time.ctime()

    #  Run the main program
    main()

    # Print the time taken
    program_end_time = time.time()
    end_ctime        = time.ctime()
    seconds          = program_end_time - program_begin_time
    m, s             = divmod(seconds, 60)
    h, m             = divmod(m, 60)
    d, h             = divmod(h, 24)
    print("\nBegin time: ", begin_ctime)
    print("End   time: ", end_ctime, "\n")
    print("Time taken: {0: .0f} days, {1: .0f} hours, \
      {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))