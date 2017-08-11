#!python3
# -*- coding: utf-8 -*-#
#
# Author      : Bhishan Poudel; Physics Graduate Student, Ohio University
# Date        : July 26, 2017
# Last update :
#
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


def replace_outfolder(outfolder):
    """Replace given directory."""
    if os.path.exists(outfolder):
        print('Replacing folder: ', outfolder)
        shutil.rmtree(outfolder)
        os.makedirs(outfolder)
    else:
        print('Making new folder: ', outfolder)
        os.makedirs(outfolder)

def run_process(name, args,):
    """Run a process.

    :Usage: 
    
    run_process("example ", ["./python ", 'example.py', 'arg1' ])
    
    The first argument "example" is optional.
    
    Also note the whitespace after the command python.
    
    .. note::
    
      This function needs python3 print_funtion.
      
    """
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
        print("\n\n", "#" * 129, end='\n')
        print("# Success! : %s " % name)
        print("\b", "#" * 129, "\n\n\n")
