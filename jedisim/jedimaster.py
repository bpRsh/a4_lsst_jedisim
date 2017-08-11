#!python
#-*- coding: utf-8 -*-
"""
:Author:
 
  Bhishan Poudel, Physics PhD Student, Ohio University

:Date: 

  Sep 06, 2016

:Last modified: 

  |today|


:Jedimaster: 

  + BEFORE
  
    * a.jedicolor, b.jedicatalog
    
  + LOOP
  
    * 1.jedicolor    2.jeditransform 3.jedidistort 4.jedipaste 5.jediconvolve 6.jedipaste     7.jedirescale
    
  + AFTER
  
    * a.jediaverage  b.jedinoise     c.jedinoise_10
    

:Inputs:

  1. executables/*
  
    - jedicolor,   jedicatalog, jedicolor,    jeditransform
    - jedidistort, jedipaste,   jediconvolve, jedipaste
    - jedirescale, jediaverage, jedinoise,    jedinoise

  2. physics_settings/*
  
    - config1.conf psf.txt lens.txt color.txt
    - rescaled_convolved_lsst_out.txt rescaled_convolved_lsst_out90.txt
    - psf.txt lens.txt

  3. psf/*
  
      - psf0.fits ... psf20.fits

  4. simdatabase/*
  
    - galaxies/f606w_gal0.fits f814w_gal0.fits (302 fitsfiles with four headers)
    - bulge_disk_f8/   (empty folder, jedicolor will create fitsfiles)
    - radius_db/*.dat   20.dat to 29.dat
    - red_db/*.dat     19.dat to 33.dat and 99.dat and -99.dat


:Outputs: 

  1. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst_0_to_20.fits    
  2. jedisim_out/rescaled_convolved_lsst_out/rescaled_convolved_lsst90_0_to_20.fits
  3. jedisim_out/out0/*      folders, txt, fits      from various programs
  4. jedisim_out/out90/*   folders, txt, fits      from various programs

:Final output: 

  1. jedisim_out/out/LSST_convolved_noise.fits
  2. jedisim_out/out/90_LSST_convolved_noise.fits

:Runtime:

   1. 6 hr 17 min (Jun 08, 2017 Thu, 377 mins)
   2. 7 hr 1 min (Jun 09, 2017 Fri, 421 mins)

.. note::

  + BEFORE_LOOP

    - jedicolor
  
      * This prgoram takes in 302 f814 filter bulge galaxies
      * ( simdatabase/bulge_f8/f814w_bulge*.fits)

      * 302 f814 filter disk  galaxies
      * ( simdatabase/disk_f8/f814w_disk*.fits)
      
      * According to the input file physics_settings/color.txt.
      * simdatabase/bulge_f8/f814w_bulge0.fits  simdatabase/disk_f8/f814w_disk0.fits  simdatabase/bulge_disk_f8/bdf8_0.fits

      * applies algorithm pix3[ii] = ((1-m)*pix1[ii])+(m*pix2[ii]);

      * And finally creates 302 galaxies inside simdatabase/bulge_disk_f8/bulge_disk_f8_*.fits
      * according to input text file physics_settings/color.txt.

    - jedicatalog
    
        * This program takes in : config.sh,lens.txt,psf.txt, config_ouptput_folder,
        * simdatabase/radius_db, simdatabase/red_db,
        * files_created_by_jedicolor
        * (simdatabase/bulge_disk_f8/*.fits)

        * And, creates       : config_output_folder/catalog.txt
        * config_output_folder/trial1_convolvedlist.txt
        * config_output_folder/trail1_distortedlist.txt
        * Note: jedisim_out/out0/trial1_dislist.txt is created by jeditransform.
        * Note: jeditransform will read these catalogs and read input galaxies
        * from simdatabase/bulge_disk_f8/f8_bulge_disk*.fits and
        * transforms as zipped files to jesisim_out/out0/stamp_0/stamp_0_to_999.fits.gz

      :jedicatalog output1:
    
        - jedisim_out/out0/catalog.txt looks like this:
        - simdatabase/bulge_disk_f8/f8_bulge_disk14.fits	7611.209473	8073.551270
        - name                                              x           y

        - 220.772644	1.500000	0.030000	22.127100	0.380010
        - angle         redshift    pixscale    old_mag     old_rad

        - 27.040001	0.166800	jedisim_out/out0/stamp_0/stamp_0.fits.gz	
        - new_mag   new_rad     stamp_name                      

        - jedisim_out/out0/distorted_0/distorted_0.fits
        - dis_name

      :jedicatalog output2:
    
        - jedisim_out/out0/convolvedlist.txt has 6 lines and first line is:
        - jedisim_out/out0/convolved/convolved_band_0.fits

      :jedicatalog output3:
   
        - jedisim_out/out0/distortedlist.txt looks like this:
        - jedisim_out/out0/distorted_0/distorted_0.fits
        - jedisim_out/out0/distorted_12/distorted_12419.fits
        - (it has 12420 entries)

      Jedicatalog does not create fitsfiles, it creates three catalog files.

.. note::

  + IN_THE_LOOP
  
    1. jedicolor
    
        jedicolor scales bulge and disk galaxies into new files.
        e.g. reads simdatabase/bulge_f8/f814w_bulge0.fits and
               simdatabase/disk_f8/f606w_disk0.fits
        writes     simdatabase/bulge_disk_f8/bulge_disk_f8_0.fits
        There is no red shift information in these input/output fitsfiles.

        Inside the loop this program does::
        
          run_process('jedicolor',  "physics_settings/color.txt",str(i/20.0)])

    2. jeditransform
    
      The code is::
    
        run_process('jeditransform', config['catalog_file'],config['dislist_file']])

      This program takes in the catalog list created by jedicatalog:
      (e.g. jedisim_out/out0/trial1_catalog.txt)

      reads the galaxy names which are to be transformed
      (e.g. simdatabase/bulge_disk_f8/bdf8_14.fits)

      and also read other parameters needed to transform that galaxy
      (e.g. x y angle redshift pixscale old_mag old_r50 new_mag new_r50 stamp1 stamp2)

      Then, it creates 12420 zipped fitsfiles inside
      jedisim_out/out0/stamp_0/stamp_0_to_999.fits.gz  (for stamps 0 to 12 )

      It also creates dislist for the jedidistort,viz.,
      jedisim_out/out0/trial1_dislist.txt

      .. warning::
        
          The input fitsfile (i.e. output of jedicolor) should not be NULL.

    3. jedidistort
    
        :Run: 
       
          :code:  `./jedidistort 12288 12288 dislist.txt lens.txt 0.03 0.3`
          :code: `executable   nx    ny    dislist     lens     pix  redshift`


        :Depends: 
        
          1. jedisim_out/out0/dislist.txt   or, dislist.txt
          2. physics_settings/lens.txt or, lens.txt
          3. jedisim_out/out0/stamp_0_to_12/stamp_0_to_999.fits.gz ( 12420 input galaxies)
          4. jedisim_out/out0/distorted_0_to_12/  ( 13 empty folder to write distorted galaxies)


        :Outputs: 
        
          1. jedisim_out/out0/distorted_0/distorted_0.fits 1000*12+ 420 fitsfiles.

        :Info: 
        
          This program distorts the 12420 galaxies from jedisim_out/out0/stamp_/
               according to dislist.txt and lens.txt and write distorted
               galaxies inside 13 folders jedisim_out/out0/distorted_/

        .. warning:: (Jun 01, 2017)
        
            While distorting galaxy 0 and all the rest of galaxies I see 
            following print outs on the terminal::
            
            !jedisim_out/out0/distorted_0/distorted_0.fits 0 -?ˆ? 

    4. jedipaste
    
        :Run: 
        
          :code: `./jedipaste 12288 12288 jedisim_out/out0/distortedlist.txt jedisim_out/out0/HST.fits`
          :code: `executable  nx    ny    input_distortedlist           output_embedded_large_fitsfile`

        :Depends: 
        
          1. config file for nx,ny,distortedlist,HST
          2. jedisim_out/out0/distortedlist.txt
          3. jedisim_out/out0/distorted_0_to12/distorted_0_to_12419.fits


        :Output: 
        
          1. jedisim_out/out0/HST.fits


        :Info: 
        
          This program combines 12,420 distorted fits files inside the jedisim_out/out0/distorted_/distorted_fits/
          into a single large embedded image: jedisim_out/out0/HST.fits.

    5. jediconvolve
        :Run: 
        
          :code: `./jediconvolve fitsfile_to_convolve psf_name_to_convolve_with output_convolved_path`

          :code: `./jediconvolve jedisim_out/out0/HST.fits psf/psf0.fits jedisim_out/out0/convolved/`

        :Depends: 
        
          1. fitsfile_to_convolve : jedisim_out/out0/HST.fits
          2. psf_to_convolve_with : psf/psf0.fits
          3. output_path_to_write_6_bands: jedisim_out/out0/convolved/


        :Output: 
        
          1. convolved_band_0.fits  upto convolved_band_5.fits

        :Info: 
        
          This program convolves the HST fitsfile with given psf and
          writes the convolved images into 6 bands to save disk space.

    6. jedipaste
    
        :Run: 
        
          :code: `./jedipaste 12288 12288 jedisim_out/out0/distortedlist.txt jedisim_out/out0/HST.fits`
          :code: `executable  nx    ny    input_distortedlist                output_embedded_large_fitsfile`

        :Needs: 
        
          1. config file for nx,ny,distortedlist,HST
          2. jedisim_out/out0/distortedlist.txt
          3. jedisim_out/out0/distorted_0_to_12/distorted_0_to_12419.fits


        :Output: 
        
          1. jedisim_out/out0/HST.fits           (after jedidistort)
      
        :Output: 
        
          1. jedisim_out/out0/HST_convolved.fits (after jediconvolve)


        :Info: 
        
          This program combines 12,420 distorted fits files inside the folder
          jedisim_out/out0/distorted_/distorted_fits/
          into a single large embedded image: jedisim_out/out0/HST.fits.

        :Info: 
        
          This program combines 6 convolved bands inside the folder
          jedisim_out/out0/convolved/
          into a single large embedded image: jedisim_out/out0/HST_convolved.fits.

    7. jedirescale
    
        :Run:
        
          :code: `./jedirescale HST_convolved.fits 0.03 0.2 480 480 LSST_convolved.fits`
          :code: `executable   input                     from to  trimx_y output`



        :Depends: 
        
          1. input fitsfile to rescale
            - e.g. jedisim_out/out0/HST_convolved.fits
                 
          2. pixscale_from, pixscale_to, trim_x, trim_y
            - e.g input config file = physics_settings/config.sh
            - pix_scale=0.03       arseconds per pixel

        :Output: 
        
          1. rescaled_fitsfile (as from physics_settings/rescaled_lsst_out.txt)
            - e.g. jedisim_out/rescaled_convolved_lsst_out/rescaled_lsst_0.fits

        :Info: 
        
          This program scales down HST image to LSST image.

.. note::

  + AFTER_LOOP
  
    1. jediaverage
    
      :Run: 
      
        :code: `./jediaverage psf.txt avg20.fits`

      :Inputs:
       
        psf.txt (21 psf files names, e.g. psf/psf0.fits)
        
      :Outputs: avg20.fits

      :Info: 
      
        This program averages out 21 psf files from the given input
        textfile and writes one output average fitsfile.

    2. jedinoise
    
      :Run: 
      
        :code: `./jedinoise LSST_convolved.fits 6000 10 LSST_convolved_noise.fits`
        :code: `executable  input_file             exp_time noise_mean output_file`

      :Depends: 
      
        1. jedisim_out/out0/LSST_convolved.fits

      :Output: 
      
        1. jedisim_out/out0/LSST_convolved_noise.fits

      :Info: 
      
        This program adds Poisson noise to a given input fitsfile.
        e.g. with exposure time 6000 seconds and noise mean 10,
        we can add noise to fitsfile "LSST_convolved.fits"
        to get "LSST_convolved_noise.fits"

    3.jedinoise
    
      In this case we add the poisson noise to aout/aout10.fits and
      create aout/aout10_noise.fits and choose this as monochromatic psf.

   
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
from util import run_process

def jedimaster():
    # Using run_process
    run_process("Replace output dirs.", ['python', "a1_create_odirs.py"])
    run_process("Create 3 catalogs.", ['python', "a2_create_3catalogs.py"])
    run_process("Run the simulation for normal case.", ['python', "a3_jedisimulate.py"])
    run_process("Run the simulation for rotated case.", ['python', "a4_jedisimulate90.py"])
    
def main():
    """Run main function."""
    jedimaster()

if __name__ == "__main__":
    main()


