#!/usr/local/bin/env python3
# -*- coding: utf-8 -*-
# Author         : Bhishan Poudel, Physics PhD Student, Ohio University
# Date           : Sep 06, 2016
# Last modified  : Jun 01, 2017
#
# Jedimaster  : BEFORE : a.jedicolor    b.jedicatalog
#               loop   : 1.jedicolor    2.jeditransform 3.jedidistort 4.jedipaste
#                        5.jediconvolve 6.jedipaste     7.jedirescale
#               AFTER  : a.jediaverage  b.jedinoise     c.jedinoise_10
#               Same happens for 90 degree rotated case.
#
# Inputs      : 1. executables/*
#                      1.jedicolor   2.jedicatalog  3.jedicolor    4.jeditransform
#                      5.jedidistort 6.jedipaste    7.jediconvolve 8.jedipaste
#                      9.jedirescale 10.jediaverage 11.jedinoise   12.jedinoise
#
#               2. physics_settings/*
#                   config1.conf psf.txt lens.txt color.txt
#                   rescaled_convolved_lsst_out.txt rescaled_convolved_lsst_out90.txt
#                   psf.txt lens.txt
#
#               3. psf/*
#                   psf0.fits ... psf20.fits
#
#               4. simdatabase/*
#                   a) galaxies/f606w_gal0.fits f814w_gal0.fits (302 fitsfiles with four headers)
#                   b) bulge_disk_f8/   (empty folder, jedicolor will create fitsfiles)
#                   c) radius_db/*.dat   20.dat to 29.dat
#                   d) red_db/*.dat     19.dat to 33.dat and 99.dat and -99.dat
#
#
# Outputs     : 1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_0_to_20.fits    
#             : 2. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst90_0_to_20.fits
#             : 3. jedisim_out/out1/*      folders, txt, fits     # from various programs
#             : 4. jedisim_out/90_out1/*   folders, txt, fits     # from various programs
#
# Final output: jedisim_out/out1/LSST_convolved_noise.fits
#               jedisim_out/out1/90_LSST_convolved_noise.fits
#
#
# Info:
# A. jedicolor
#    This prgoram takes in 302 f814 filter bulge galaxies
#    ( simdatabase/bulge_f8/f814w_bulge*.fits)
#
#    302 f814 filter disk  galaxies
#    ( simdatabase/disk_f8/f814w_disk*.fits)
#
#     applies algorithm pix3[ii] = ((1-m)*pix1[ii])+(m*pix2[ii]); with m = 1.
#
#     And finally create 302 galaxies inside simdatabase/bulge_disk_f8/bulge_disk_f8_*.fits
#     according to input text file physics_settings/color.txt.
#
# B. jedicatalog
# This program takes in : config.sh,lens.txt,psf.txt, config_ouptput_folder,
#                         simdatabase/radius_db, simdatabase/red_db,
#                         files_created_by_jedicolor
#                         (simdatabase/bulge_disk_f8/*.fits)
#
#    And, creates       : config_output_folder/catalog.txt
#                         config_output_folder/convolvedlist.txt
#                         config_output_folder/distortedlist.txt
#    Note: jedisim_out/out1/dislist.txt is created by jeditransform.
#    Note: jeditransform will read these catalogs and read input galaxies
#          from simdatabase/bulge_disk_f8/f8_bulge_disk*.fits and
#          transforms as zipped files to jesisim_out/out1/stamp_0/stamp_0_to_999.fits.gz
#
# jedicatalog output1:
# jedisim_out/out1/catalog.txt looks like this:
# simdatabase/bulge_disk_f8/f8_bulge_disk14.fits	7611.209473	8073.551270
# name                                              x           y
#
# 220.772644	1.500000	0.030000	22.127100	0.380010
# angle         redshift    pixscale    old_mag     old_rad
#
# 27.040001	0.166800	jedisim_out/out1/stamp_0/stamp_0.fits.gz	
# new_mag   new_rad     stamp_name                      
#
# jedisim_out/out1/distorted_0/distorted_0.fits
# dis_name
#
# jedicatalog output2:
# jedisim_out/out1/convolvedlist.txt has 6 lines and first line is:
# jedisim_out/out1/convolved/convolved_band_0.fits
#
# jedicatalog output3:
# jedisim_out/out1/distortedlist.txt looks like this:
# jedisim_out/out1/distorted_0/distorted_0.fits
# jedisim_out/out1/distorted_12/distorted_12419.fits
# (it has 12420 entries)
#
# Jedicatalog does not create fitsfiles, it creates three catalog files.
#
# LOOP STARTS HERE
# 1. jedicolor
#    jedicolor scales bulge and disk galaxies into new files.
#    e.g. reads simdatabase/bulge_f8/f814w_bulge0.fits and
#               simdatabase/disk_f8/f606w_disk0.fits
#    writes     simdatabase/bulge_disk_f8/bulge_disk_f8_0.fits
#    There is no red shift information in these input/output fitsfiles.
#
#    Inside the loop this program does:
#       'jedicolor',  "physics_settings/color.txt",str(i/20.0)]
#
# 2. jeditransform
#       'jeditransform', config['catalog_file'],config['dislist_file']])
#
#  This program takes in the catalog list created by jedicatalog:
#  (e.g. jedisim_out/out1/trial1_catalog.txt)
#
#  reads the galaxy names which are to be transformed
#  (e.g. simdatabase/bulge_disk_f8/bdf8_14.fits)
#
#  and also read other parameters needed to transform that galaxy
#  (e.g. x y angle redshift pixscale old_mag old_r50 new_mag new_r50 stamp1 stamp2)
#
#  Then, it creates 12420 zipped fitsfiles inside
#  jedisim_out/out1/stamp_0/stamp_0_to_999.fits.gz  (for stamps 0 to 12 )
#
#  It also creates dislist for the jedidistort,viz.,
#  jedisim_out/out1/trial1_dislist.txt
#
## WARNING : The input fitsfile (i.e. output of jedicolor) should not be NULL.
#
#  3. jedidistort
#  Run         : ./jedidistort 12288 12288 dislist.txt lens.txt 0.03 0.3
#                 executable   nx    ny    dislist     lens     pix  redshift
#
#
#
#  Depends     : 1. jedisim_out/out1/dislist.txt   or, dislist.txt
#                2. physics_settings/lens.txt or, lens.txt
#                3. jedisim_out/out1/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input galaxies)
#                4. jedisim_out/out1/distorted_0_to_12/  ( 13 empty folder to write distorted galaxies)
#
#
#  Outputs     : 1. jedisim_out/out1/distorted_0/distorted_0.fits 1000*12+ 420 fitsfiles.
#
#  Info        : This program distorts the 12420 galaxies from jedisim_out/out1/stamp_/
#               according to dislist.txt and lens.txt and write distorted
#               galaxies inside 13 folders jedisim_out/out1/distorted_/
#
# WARNING : (Jun 01, 2017)
#            While distorting galaxy 0 and all the rest of galaxies I see 
#            following print outs on the terminal:
#            !jedisim_out/out1/distorted_0/distorted_0.fits 0 -?ˆ? 
#
# 4. jedipaste
#  Run         : ./jedipaste 12288 12288 jedisim_out/out1/distortedlist.txt jedisim_out/out1/HST.fits
#               executable  nx    ny    input_distortedlist                       output_embedded_large_fitsfile
#
# Depends     : 1. config file for nx,ny,distortedlist,HST
#               2. jedisim_out/out1/distortedlist.txt
#               3. jedisim_out/out1/distorted_0_to12/distorted_0_to_12419.fits
#
#
# Output      : 1. jedisim_out/out1/HST.fits
#
#
# Info: This program combines 12,420 distorted fits files inside the jedisim_out/out1/distorted_/distorted_fits/
#       into a single large embedded image: jedisim_out/out1/HST.fits.
#
# 5. jediconvolve
#   Run         : ./jediconvolve fitsfile_to_convolve psf_name_to_convolve_with output_convolved_path
#
#                ./jediconvolve jedisim_out/out1/HST.fits psf/psf0.fits jedisim_out/out1/convolved/
#
#  Depends     : 1. fitsfile_to_convolve : jedisim_out/out1/HST.fits
#                2. psf_to_convolve_with : psf/psf0.fits
#                3. output_path_to_write_6_bands: jedisim_out/out1/convolved/
#
#
#  Output      : 1. convolved_band_0.fits  upto convolved_band_5.fits
#
#  Info: This program convolves the HST fitsfile with given psf and
#        writes the convolved images into 6 bands to save disk space.
#
# 6.jedipaste
#   Run         : ./jedipaste 12288 12288 jedisim_out/out1/distortedlist.txt jedisim_out/out1/HST.fits
#                 executable  nx    ny    input_distortedlist                output_embedded_large_fitsfile
#
#  Needs       : 1. config file for nx,ny,distortedlist,HST
#                2. jedisim_out/out1/distortedlist.txt
#                3. jedisim_out/out1/distorted_0_to_12/distorted_0_to_12419.fits
#
#
#  Output      : 1. jedisim_out/out1/HST.fits           (after jedidistort)
#  Output      : 1. jedisim_out/out1/HST_convolved.fits (after jediconvolve)
#
#
#  Info: This program combines 12,420 distorted fits files inside the folder
#        jedisim_out/out1/distorted_/distorted_fits/
#        into a single large embedded image: jedisim_out/out1/HST.fits.

#  Info: This program combines 6 convolved bands inside the folder
#        jedisim_out/out1/convolved/
#        into a single large embedded image: jedisim_out/out1/HST_convolved.fits.
#
# 7. jedirescale
# #   Run         :
#   ./jedirescale HST_convolved.fits 0.03 0.2 480 480 LSST_convolved.fits
#    executable   input                     from to  trimx_y output
#
#
#
#   Depends     : 1. input fitsfile to rescale
#                    e.g. jedisim_out/out1/HST_convolved.fits
#                 2. pixscale_from, pixscale_to, trim_x, trim_y
#                    e.g input config file = physics_settings/config.sh
#                    pix_scale=0.03      # arseconds per pixel
#
#   Output      : 1. rescaled_fitsfile (as from physics_settings/rescaled_lsst_out.txt)
#                    e.g. jedisim_out/rescaled_convolved_lsst_out/rescaled_lsst_0.fits
#
#   Info: This program scales down HST image to LSST image.
#
#   1.A. jediaverage
#   Run         : ./jediaverage psf.txt avg20.fits
#
#   Inputs      : psf.txt (21 psf files names, e.g. psf/psf0.fits)
#   Outputs     : avg20.fits
#
#   Info: This program averages out 21 psf files from the given input
#         textfile and writes one output average fitsfile.
#
#   1.B. jedinoise
#  Run         : ./jedinoise LSST_convolved.fits 6000 10 LSST_convolved_noise.fits
#                executable  input_file             exp_time noise_mean output_file
#
#  Depends     : 1. jedisim_out/out1/LSST_convolved.fits
#
#  Output      : 1. jedisim_out/out1/LSST_convolved_noise.fits
#
#  Info        : This program adds Poisson noise to a given input fitsfile.
#                e.g. with exposure time 6000 seconds and noise mean 10,
#                we can add noise to fitsfile "LSST_convolved.fits"
#                to get "LSST_convolved_noise.fits"
#
#   1.C. jedinoise
#   In this case we add the poisson noise to aout/aout10.fits and
#   create aout/aout10_noise.fits and choose this as monochromatic psf.
#
# Estimated time: 6 hr 17 min (Jun 08, 2017 Thu, 377 mins)
# Estimated time: 7 hr 1 min (Jun 09, 2017 Fri, 421 mins)
#
# Imports
import os
import sys
import subprocess
import math
import re
import shutil
import copy
import time
import numpy as np

# start time
program_start_time = time.time()
program_begin_time = time.ctime()
config_path = "physics_settings/config.sh"



# ==============================================================================
#            Part 1A   Define some functions at the beginning.
#                      replace_outfolder, config_dict, run_process
# ==============================================================================
def replace_outfolder(outfolder):
    """Replace given directory."""
    # Imports
    import shutil
    import os

    if os.path.exists(outfolder):
        print('Replacing folder: ', outfolder)
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)
    else:
        print('Making new folder: ', outfolder)
        os.makedirs(outfolder)


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


def run_process(name, args,):
    """Run a process.

    Usage: run_process("example ", ["python ", 'example.py', 'arg1' ]) .
    The first argument "example" is optional.
    Also note that whitespace after the command python.
    """
    # Imports
    import subprocess
    import sys

    print("\n\n\n", "#" * 130)
    print("# Program  : %s\n# Commands :" % name, end=' ')
    for arg in args:
        print(arg, end=' ')

    print("\n", "#" * 130, end='\n\n')

    process = subprocess.Popen(args)

    process.communicate()
    if process.returncode != 0:
        print("Error: %s did not terminate correctly. \
              Return code: %i." % (name, process.returncode))
        sys.exit(1)
    else:
        till_now = (time.time() - program_start_time) / 60
        print("\n\n", "#" * 129, end='\n')
        print("# Time taken till now = %.0f minutes" % till_now)
        print("# Success! : %s " % name)
        print("\b", "#" * 129, "\n\n\n")

# ==============================================================================
#            Part 1B   Before Loop create outfolders and run color,catalog
# ==============================================================================
# Create config dictionary
#config_path = "physics_settings/config.sh"
config = config_dict(config_path)

# Print config dictionary
#for key, value in config.items():
    #print (key, " = ", value)

# Make copy
config_record = copy.deepcopy(config)


# Make the filenames from the config parameters
# e.g HST.fits ==> jedisim_out/out1/HST.fits from config file
#print(config['HST_image'])  # HST.fits
prefix = config['output_folder'] + config['prefix']  #


keys = ['HST_image',            'HST_convolved_image',
        'LSST_averaged_image',  'LSST_averaged_noised_image',
        'catalog_file',         'dislist_file',
        'distortedlist_file',   'convolvedlist_file']


for key in keys:
    config[key] = prefix + config[key]

#print(config['HST_image'])  # jedisim_out/out1/HST.fits

# List of psf and rescaled_lsst_outfile
psf =  ['psf/psf%d.fits' % i for i in range(21)]
rescaled_lsst_outfile = ['jedisim_out/rescaled_lsst/rescaled_lsst_%d.fits'
                          % i for i in range(21) ]

# Replace old output folders before running new simulation
# e.g. delete jedisim_out/out1/ ==> jedisim_out/out1
outfolders = [config["output_folder"][0:-1],
              config["rescaled_outfolder"],
              config["color_outfolder"]
              ]
for outfolder in outfolders:
    replace_outfolder(outfolder)


# Create output folders for jedidistort and jediconvolve
# Make folder for convolved images
# e.g. jedisim_out/out1/convolved
convolved_path = "%sconvolved/" % config['output_folder']
if not os.path.exists(convolved_path):
    os.makedirs(convolved_path)

# Make stamps and distorted folders
# e.g. 90_jedisim_out/out1/stamp_0 to stamp_12
# e.g. 90_jedisim_out/out1/distorted_0 to stamp_12
for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
    postage_path = "%sstamp_%i" % (config['output_folder'], x)
    distorted_path = "%sdistorted_%i" % (config['output_folder'], x)
    if not os.path.exists(postage_path):
        os.makedirs(postage_path)
    if not os.path.exists(distorted_path):
        os.makedirs(distorted_path)




# Now we run the Auxiliary C programs.
# We have changed jedicolor program.
# Modified : Jun 10, 2017 Sat
# First row of the file (first is b and second is d)
# 6.9565099e-04 4.9318209e-02
infile = config['jedicolor_args_infile']
b,d = np.genfromtxt(infile,delimiter=None,usecols=(0,1),dtype=float,unpack=True)

# Create sample galaxies from original galaxies.
run_process("jedicolor", ['./executables/jedicolor',
                          config['color_infile'],
                          str(b[0]), str(d[0])  ])

# Make the catalog of galaxies (three text files)
run_process("jedicatalog", ["./executables/jedicatalog",
                            config_path])


# ==============================================================================
#            Part 1C   Loop of 7 programs
#                      color,trans,distort,paste,convolve,paste,rescale
# ==============================================================================
for i in range(0, 21):

    # The jedicolor creates 302 fitsfiles inside config['color_outfolder']
    run_process("jedicolor", ['./executables/jedicolor',
                              config['color_infile'],
                              str(b[i]), str(d[i])  ])

    # Run jeditransform
    run_process("jeditransform", ['./executables/jeditransform',
                                  config['catalog_file'],
                                  config['dislist_file']])

    # Lens the galaxies one at a time
    run_process("jedidistort", ['./executables/jedidistort',
                                config['nx'],
                                config['ny'],
                                config['dislist_file'],
                                config['lenses_file'],
                                config['pix_scale'],
                                config['lens_z']])

    # Combine the lensed galaxies onto one large image
    run_process("jedipaste", ['./executables/jedipaste',
                              config['nx'],
                              config['ny'],
                              config['distortedlist_file'],
                              config['HST_image']])

    # Convonlve the large image with the PSF
    # This creates one image for each band of the image
    run_process("jediconvolve", ['./executables/jediconvolve',
                                 config['HST_image'],
                                 psf[i],
                                 convolved_path])

    # Combine each band into a single image
    run_process("jedipaste", ['./executables/jedipaste',
                              config['nx'],
                              config['ny'],
                              config['convolvedlist_file'],
                              config['HST_convolved_image']])

    # Scale the image down from HST to LSST scale and trim the edgescolor
    # outputfile[0] = jedisim_out/rescaled_lsst/rescaled_lsst_0.fits
    run_process("jedirescale", ['./executables/jedirescale',
                                config['HST_convolved_image'],
                                config['pix_scale'],
                                config['final_pix_scale'],
                                config['x_trim'],
                                config['y_trim'],
                                rescaled_lsst_outfile[i]])
# ==============================================================================
#            Part 1D   After the loop run avg,noise,noise
#                      replace_outfolder, config_dict, run_process
# ==============================================================================


# Average the 21 fits files from jedisim_out/rescaled_lsst/*.fits
# And write to jedisim_out/out0/LSST_averaged.fits
run_process("jediaverage", ['./executables/jediaverage',
                            config['rescaled_lsst_outfile'],
                            config['LSST_averaged_image']])

# Simulate exposure time and add Poisson noise
# jedisim_out/out0/LSST_averaged.fits ==> jedisim_out/out1/LSST_averaged_noised.fits
run_process("jedinoise", ['./executables/jedinoise',
                          config['LSST_averaged_image'],
                          config['exp_time'],
                          config['noise_mean'],
                          config['LSST_averaged_noised_image']])


# Add noise to rescaled file and  choose as monochromatic image
run_process("jedinoise", ['./executables/jedinoise',
                          config["monochromatic_infits"],                          
                          config['exp_time'],
                          config['noise_mean'],
                          config["monochromatic_outfits"] ])


# ==============================================================================
#            Part 2A   Part 2 is 90 degree rotated case
#                      Part before loop
# ==============================================================================
# Add 90_ keys to our dictionary config
# Modified: Jun 03, 2017
keys = ['HST_image',            'HST_convolved_image',
        'LSST_averaged_image',  'LSST_averaged_noised_image',
        'catalog_file',         'dislist_file',
        'distortedlist_file',   'convolvedlist_file' ]
        
pre = '90_' + config_record['prefix']
for key in keys:
    key90 = '90_' + key
    config[key90] = config['90_output_folder'] + pre + config_record[key]

# Replace output folders for 90 degree rotated case.
# e.g. jedisim_out/out90
replace_outfolder(config['90_output_folder'])
  
# Replace rescaled_lsst_90 folder
# e.g. jedisim_out/rescaled_lsst90
replace_outfolder(config['rescaled_outfolder90'])


# Make folder for convolved images
# e.g. 90_jedisim_out/out1/convolved
convolved_path = "%sconvolved/" % (config['90_output_folder'])
if not os.path.exists(convolved_path):
    os.makedirs(convolved_path)


# Make distroted folders
# e.g. jedisim_out/out90/stamp_0 to stamp_12
# e.g. jedisim_out/out90/distorted_0 to stamp_12
for x in range(0, int(math.ceil(float(config['num_galaxies']) / 1000))):
    postage_path = "%sstamp_%i" % (config['90_output_folder'], x)
    distorted_path = "%sdistorted_%i" % (config['90_output_folder'], x)
    if not os.path.exists(postage_path):
        os.makedirs(postage_path)
    if not os.path.exists(distorted_path):
        os.makedirs(distorted_path)


# Rotate old catalog file by 90 degree
# e.g. jedisim_out/out90/trial1_catalog.txt
old_catalog_file = open(config['catalog_file'], 'r')
catalog_file = open(config['90_catalog_file'], 'w')
for old_line in old_catalog_file:
    l = old_line.split("\t")
    angle = float(l[3]) + 90
    angle -= 360 * (int(angle) / 360)
    l[3] = str(angle)
    l[-1] = l[-1].replace(config['output_folder'], config['90_output_folder'])
    l[-2] = l[-2].replace(config['output_folder'], config['90_output_folder'])
    line = "\t".join(l)
    catalog_file.write(line)
old_catalog_file.close()
catalog_file.close()


# Update output folder in convolvedlist file
# e.g. jedisim_out/out90/trial1_convolvedlist.txt
old_convolvedlist_file = open(config['convolvedlist_file'], 'r')
convolvedlist_file = open(config['90_convolvedlist_file'], 'w')
for old_line in old_convolvedlist_file:
    line = old_line.replace(config['output_folder'],
                            config['90_output_folder'])
    convolvedlist_file.write(line)
old_convolvedlist_file.close()
convolvedlist_file.close()



# Update output folder in distortedlist file
# e.g. jedisim_out/out90/trial1_distortedlist.txt
old_distortedlist_file = open(config['distortedlist_file'], 'r')
distortedlist_file = open(config['90_distortedlist_file'], 'w')
for old_line in old_distortedlist_file:
    line = old_line.replace(config['output_folder'],
                            config['90_output_folder'])
    distortedlist_file.write(line)
old_distortedlist_file.close()
distortedlist_file.close()


# Create list of psf90, rescaled_lsst_outfile90
psf90 =  ['psf/psf%d.fits' % i for i in range(21)]
rescaled_lsst_outfile90 = ['jedisim_out/rescaled_lsst90/rescaled_lsst90_%d.fits'
                          % i for i in range(21) ]

# ==============================================================================
#            Part 2B  Part before for loop is not needed
#            Part 2C  Part of loop of 7 programs
# ==============================================================================
for j in range(0, 21):

    # The jedicolor creates 302 fitsfiles inside config['output_folder_bulge']
    run_process("jedicolor", ['./executables/jedicolor',
                              config['color_infile'],
                              str(b[j]), str(d[j])  ])

    # Make postage stamp images that fit the catalog parameters
    run_process("jeditransform", ['./executables/jeditransform',
                                  config['90_catalog_file'],
                                  config['90_dislist_file']])

    # Lens the galaxies one at a time
    run_process("jedidistort", ['./executables/jedidistort',
                                config['nx'],
                                config['ny'],
                                config['90_dislist_file'],
                                config['lenses_file'],
                                config['pix_scale'],
                                config['lens_z']])

    # Combine the lensed galaxies onto one large image
    run_process("jedipaste", ['./executables/jedipaste',
                              config['nx'],
                              config['ny'],
                              config['90_distortedlist_file'],
                              config['90_HST_image']])

    # Convonlve the large image with the PSF.
    # This creates one image for each band of the image.
    run_process("jediconvolve", ['./executables/jediconvolve',
                                 config['90_HST_image'],
                                 psf90[j],
                                 convolved_path])

    # Combine each band into a single image
    run_process("jedipaste", ['./executables/jedipaste',
                              config['nx'],
                              config['ny'],
                              config['90_convolvedlist_file'],
                              config['90_HST_convolved_image']])

    # Scale the image down from HST to LSST scale and trim the edges.
    run_process("jedirescale", ['./executables/jedirescale',
                                config['90_HST_convolved_image'],
                                config['pix_scale'],
                                config['final_pix_scale'],
                                config['x_trim'],
                                config['y_trim'],
                                rescaled_lsst_outfile90[j]])
# ==============================================================================
#            Part 2D  Part after the loop
# ==============================================================================
# Average the lsst files.
run_process("jediaverage", ['./executables/jediaverage',
                            config['rescaled_lsst_outfile90'],
                            config['90_LSST_averaged_image']])

# Add noise to averaged file.
run_process("jedinoise", ['./executables/jedinoise',
                          config['90_LSST_averaged_image'],
                          config['exp_time'],
                          config['noise_mean'],
                          config['90_LSST_averaged_noised_image']])


# Modified aug 3, 2016
# Create monochromatic psf
run_process("jedinoise", ['./executables/jedinoise',
                          config["monochromatic_infits90"],                          
                          config['exp_time'],
                          config['noise_mean'],
                          config["monochromatic_outfits90"] ])

# ==============================================================================
#            Part 3  Last part printing Success and time taken
# ==============================================================================
# Print success
print("jedisim successful! Exiting.")


# Print the time taken
program_end_time = time.time()
seconds = program_end_time - program_start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
print('\nProgram started at : ', program_begin_time)
print('\nProgram ended at   : ', time.ctime())
print("\nTime taken to run whole program ==> {:2.0f} days, {:2.0f} hours,\
        {:2.0f} minutes, {:f} seconds.".format(d, h, m, s))
# ==============================================================================
#            The End !!
# ==============================================================================
#
