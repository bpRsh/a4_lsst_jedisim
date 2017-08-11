#!python
# -*- coding: utf-8 -*-
"""
:Author:

  Bhishan Poudel; Physics Graduate Student, Ohio University

:Date:

  Aug 01, 2016

:Last update: |today|

:Inputs:

  1. jedimaster.py, especially the final outputs
  2. out1/trial0_LSST_convolved_noise.fits
  3. out1/90_trial0_LSST_convolved_noise.fits

:Outputs:
  1. jedisim_output/lsst*.fits
  2. jedisim_output/90_lsst*.fits
  3. jedisim_output/aout10_noise*.fits
  4. jedisim_output/90_aout10_noise*.fits

:Info:
  1. This is a wrapper script to jedimaster.py.
  2. Basically it copies the final outputs of jedimaster to a different
     directory in each loop.

:Runtime:

  - one loop takes 4 hours 20 min(mac)
  - six loop takes 25 hours (mac)
  - one loop takes 6 hour 20 minutes (linux)
  - five loop took  (simplici, July 29 2017)

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
from util import run_process

# start time
start_time = time.time()
start_ctime = time.ctime()

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

def run_jedimaster(start, end):

    # Get redshift
    config = config_dict(config_path)
    z = config['fixed_redshift']

    # create outfolder names
    outfolder = 'jedisim_output/jout_z{}_2017'.format(z) + time.strftime("_%b_%d_%H_%M/")
    print(outfolder)

    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    # run jedimaster in a loop
    for i in range(start, end+1):
        print('{} {} {}'.format('Running jedimaster loop :', i, ''))

        run_process("jedimaster.py", ['python', "jedimaster.py"])

        # copy final output files
        infile1 = r'jedisim_out/out0/trial1_LSST_averaged_noised.fits'
        outfile1 = outfolder + 'lsst_{:d}.fits'.format(i)

        infile2 = r'jedisim_out/out90/90_trial1_LSST_averaged_noised.fits'
        outfile2 = outfolder + 'lsst_90_{:d}.fits'.format(i)

        infile3 = r'jedisim_out/rescaled_lsst/rescaled_noised_lsst_10.fits'
        outfile3 = outfolder + 'monochromatic_{:d}.fits'.format(i)

        infile4 = r'jedisim_out/rescaled_lsst90/rescaled_noised_lsst90_10.fits'
        outfile4 = outfolder + 'monochromatic_90_{:d}.fits'.format(i)

        shutil.copyfile(infile1, outfile1)
        shutil.copyfile(infile2, outfile2)
        shutil.copyfile(infile3, outfile3)
        shutil.copyfile(infile4, outfile4)

        # print('{} {} {}'.format('!' * 80, '', ''))
        # print('{} {} {} {}'.format('!' * 35, ' End of jedimaster loop :', i, '!' * 35))
        # print('{} {} {}'.format('!' * 80, '\n', ''))


def main():
    """Run main function."""
    # start, end inclusive
    # no. of loop = end - start + 1
    start, end = 0,2
    run_jedimaster(start, end)


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
    print("Begin time: ", begin_ctime)
    print("End   time: ", end_ctime, "\n")
    print("Time taken: {0: .0f} days, {1: .0f} hours, \
      {2: .0f} minutes, {3: f} seconds.".format(d, h, m, s))
