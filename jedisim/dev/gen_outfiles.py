#!python
# -*- coding: utf-8 -*-
#
# Author      : Bhishan Poudel, Physics PhD Student, Ohio University
# Last update : Jun 10, 2017 Sat
#
# Info: This program will create four output text files, viz.
#       config.sh, color.txt, rescaled_lsst_outfile.txt,
#       and rescaled_lsst_outfile90.txt inside ../physics_settings directory.
#
# Imports
import time

# Global variable
NUM_GALS = 201

def gen_config():
    """ This needs template_config.sh input text file. """
    # data
    data = open('template_config.sh').readlines()
    config_path = '../physics_settings/config.sh'
    print('Creating : %s'%(config_path))
    with open(config_path, 'w') as fo:
        for line in data:
            fo.write(line)
    ## add image names
    with open(config_path, 'a') as fo:
        for i in range(NUM_GALS):
            line = r'image="simdatabase/bulge_disk_f8/bdf8_{:d}.fits"'.format(i) + '\n'
            fo.write(line)


def gen_color_txt():
    """ Create color.txt    
    This has three columns which looks like: 
 simdatabase/bulge_f8/f814w_bulge0.fits
 simdatabase/disk_f8/f814w_disk0.fits
 simdatabase/bulge_disk_f8/bulge_disk_f8_0.fits 
 jedicolor will scale first two fits files and writes the last one. 
 bulge and disk are obtained from two component fitting of galfit. 
 The galfit takes in input galaxy provided by collaboraters, 
 and gets bulge and disk part from each galaxy. 
 Not all the galaxies have two components. 
 The one which does not have bulge part, we take the original galaxy as bulge one. 
 The one which does not have disk part, we take the nullfits as the disk one.
    """
    sim          = 'simdatabase/'
    outfile      = "../physics_settings/color.txt"
    print('Creating : %s'%(outfile))  
    with open(outfile, 'w') as fout:
        for i in range(NUM_GALS):
            in1  = sim + 'bulge_f8/f814w_bulge'         + str(i) + '.fits'
            in2  = sim + 'disk_f8/f814w_disk'           + str(i) + '.fits'
            #out  = sim + 'bulge_disk_f8/bulge_disk_f8_' + str(i) + '.fits'
            out  = sim + 'bulge_disk_f8/bdf8_' + str(i) + '.fits'
            line = '  '.join([in1, in2, out])
            print(line, file=fout)



def gen_rescaled_lsst_ofile():
    """ Create rescaled_lsst_outfile.txt.    
    This is used by jediaverage.
    """
    outfile0  = "../physics_settings/rescaled_lsst_outfile.txt"
    outfile90 = "../physics_settings/rescaled_lsst_outfile90.txt"
    print('Creating : %s'%(outfile0))    
    print('Creating : %s'%(outfile90))    
    with open(outfile0, 'w')  as fout0, \
         open(outfile90, 'w') as fout90:
        for i in range(21):
            fout0.write('jedisim_out/rescaled_lsst/rescaled_lsst_%d.fits\n' % i)
            fout90.write('jedisim_out/rescaled_lsst90/rescaled_lsst90_%d.fits\n' % i)

##==============================================================================
## Main program
##==============================================================================
if __name__ == '__main__':
    # beginning time
    begin_time,begin_ctime = time.time(), time.ctime()

    # run main program
    gen_config()
    gen_color_txt()
    gen_rescaled_lsst_ofile()

    # print the time taken
    end_time,end_ctime  = time.time(), time.ctime()
    seconds             = end_time - begin_time
    m, s                = divmod(seconds, 60)
    h, m                = divmod(m, 60)
    d, h                = divmod(h, 24)
    print('\nBegin time: ', begin_ctime,'\nEnd   time: ', end_ctime,'\n' )
    print("Time taken: {0:.0f} days, {1:.0f} hours, \
          {2:.0f} minutes, {3:f} seconds.".format(d, h, m, s))
