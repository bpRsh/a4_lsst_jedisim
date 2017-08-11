#!python
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : Jan 4, 2017
# Update      : Aug 7, 2017 Mon
# 
# Imports
import os
import subprocess
import glob
import re
import natsort
from astropy.io.fits import getdata
import numpy as np


def find_nan_in_fits():
    """Check if a fitsfile has nan values in it."""
    # get nan values
    mynans = []
    negs=[]
    for i in range(1000):
        dat = getdata('out0/distorted_0/distorted_{}.fits'.format(i))
        mysum = np.sum(dat)
        if np.isnan(mysum):
            mynans.append(i)
            # print('simdatabase/bulge_disk_f8/bdf8_{}.fits'.format(i) , 'has sum = ', mysum)
        print('out0/distorted_0/distorted_{}.fits'.format(i) , 'has sum = ', mysum)
        
        # extra
        if float(mysum) < 0.0:
            negs.append(i)
                
        
    return mynans,negs


if __name__ == "__main__":
    mynans,negs     = find_nan_in_fits()
    print(mynans)
    # print(negs)

