#!python
# -*- coding: utf-8 -*-
"""This program takes in HST images and simulates LSST images.

:Before Running:

  Before running this program we have created required output folders and 
  required 3 catalog files (catalog, convolvedlist and distortedlist)
  using jedicolor and jedicatalog programs.

:Order:

  color transform distort convolve rescale average21 noise 

.. note::

  - jedicolor reads bulge and disk images and create bulge-disk image with weights.
  - jeditransform transforms bulge-disk fitsfiles with our needs and creates 12420 zipped stamps and also create dislist.txt.
  - jedidistort distort the zipped stamps accordint to the dislist.txt and writes 12420 unzipped distorted fitsfiles.
  - jedipaste will combine these 12420 distorted images into one large HST.fits according to distortedlist.txt.
  - jediconvolve will convolve HST.fits with psf[i].fits inside the 21 loop and creates 6 convolved bands.
  - jedipaste will combine these 6 convolved bands and create HST_convolved_image.
  - jedirescale scales down from HST_convolved image to rescaled_lsst image according to rescaled_lsst_outfile.txt.
  - jediaverage will average 21 rescaled_lsst0_to20 images and writes LSST_averaged.fits according to config.sh.
  - jedinoise will add noise to this image and creates LSST_averaged_noised.fits according to config.sh
  
:Runtime:

  10 minutes for only one of 21 loops. (July 27, 2017)

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
    """Update the config dictionary keys and values.
    
    Changes::
    
      From: HST_image = HST.fits
      To:   HST_image = jedisim_out/out0/trial1_HST.fits
      Also: 90_HST_image = jedisim_out/out90/90_trial1_HST.fits
       
    """
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


def psf_rescaled_lsst_outfile_lst():
    psf =  ['psf/psf%d.fits' % i for i in range(21)]
    rescaled_lsst_outfile = ['jedisim_out/rescaled_lsst/rescaled_lsst_%d.fits'
                              % i for i in range(21) ]
    return psf, rescaled_lsst_outfile



def get_bulge_disk_weights():
    config = update_config()
    infile = config['jedicolor_args_infile']
    b,d = np.genfromtxt(infile,delimiter=None,usecols=(0,1),dtype=float,unpack=True)
    
    return b,d


def run_7programs_loop():
    """Run 7 programs in the loop."""
    config = update_config()
    b, d = get_bulge_disk_weights()
    psf, rescaled_lsst_outfile = psf_rescaled_lsst_outfile_lst()
    for i in range(0, 21):

        # Create bulge-disk images with appropriate weights to bulge and disk.
        run_process("jedicolor", ['./executables/jedicolor',
                                  config['color_infile'],
                                  str(b[i]), str(d[i])  
                                  ])

        # Transform bulge-disk images with our settings.
        run_process("jeditransform", ['./executables/jeditransform',
                                      config['catalog_file'],
                                      config['dislist_file']
                                      ])

        # Lens 12420 galaxies and get unzipped distorted images.
        run_process("jedidistort", ['./executables/jedidistort',
                                    config['nx'],
                                    config['ny'],
                                    config['dislist_file'],
                                    config['lenses_file'],
                                    config['pix_scale'],
                                    config['lens_z']
                                    ])

        # Combine the lensed galaxies onto one large image
        run_process("jedipaste", ['./executables/jedipaste',
                                  config['nx'],
                                  config['ny'],
                                  config['distortedlist_file'],
                                  config['HST_image']
                                  ])

        # Create 6 convolved bands by combinining input images with psf[i].
        run_process("jediconvolve", ['./executables/jediconvolve',
                                     config['HST_image'],
                                     psf[i],
                                     config['output_folder'] + 'convolved/'
                                     ])

        # Combine 6 convolved bands into HST_convolved image.
        run_process("jedipaste", ['./executables/jedipaste',
                                  config['nx'],
                                  config['ny'],
                                  config['convolvedlist_file'],
                                  config['HST_convolved_image']
                                  ])

        # Scale the image down from HST to LSST scale and trim the edgescolor
        run_process("jedirescale", ['./executables/jedirescale',
                                    config['HST_convolved_image'],
                                    config['pix_scale'],
                                    config['final_pix_scale'],
                                    config['x_trim'],
                                    config['y_trim'],
                                    rescaled_lsst_outfile[i]
                                    ])


def average21_and_add_noise():
    """Average 21 rescaled lsst images and add noise to them.
    
    :Runtime:
    
        15 seconds.
    
    """
    # Average the 21 fits files from jedisim_out/rescaled_lsst/*.fits
    # And write to jedisim_out/out0/LSST_averaged.fits
    config = update_config()
    run_process("jediaverage", ['./executables/jediaverage',
                                config['rescaled_lsst_outfile'],
                                config['LSST_averaged_image']
                                ])

    # Simulate exposure time and add Poisson noise
    # jedisim_out/out0/LSST_averaged.fits ==> jedisim_out/out1/LSST_averaged_noised.fits
    run_process("jedinoise", ['./executables/jedinoise',
                              config['LSST_averaged_image'],
                              config['exp_time'],
                              config['noise_mean'],
                              config['LSST_averaged_noised_image']
                              ])


    # Add noise to rescaled file and  choose as monochromatic image
    run_process("jedinoise", ['./executables/jedinoise',
                              config["monochromatic_infits"],                          
                              config['exp_time'],
                              config['noise_mean'],
                              config["monochromatic_outfits"] 
                              ])


def main():
    """Run main function."""
    
    # Run 7 programs in the loop
    run_7programs_loop()
    
    # Average 21 outputs and add noise to it.
    average21_and_add_noise()

    

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
    # print("\nBegin time: ", begin_ctime)
    # print("End   time: ", end_ctime, "\n")
    # print("Time taken: {0: .0f} days, {1: .0f} hours, \
    #   {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))

