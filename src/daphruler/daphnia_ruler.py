#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 19:28:26 2018

@author: Nelson
"""


#load libraries
import time
import os
import json
import cv2
import sys
from daphruler import measurement_methods
import imghdr
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse
from pathlib import Path
from daphruler import helpers

def parse_args(args):
    """parse arguments properly

    Parameters
    ----------
    args : Arguments from cli
        

    Returns
    -------

    """
    # use argparse to create optional arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to your input directory. The program is able to loop through subdirectories of the input.', type=helpers.is_dir)
    parser.add_argument('-n', '--noImages', help="Don't write images with results overplotted.", action='store_true')
    parser.add_argument('-e', '--eyeMethod', help="Implement eye method on top of ellipse method.", action='store_true')
    parser.add_argument('-s', '--scaleMM', help="Scale measurement to mm. For more information see README.md", action='store_true')

    #if no arguments are provided go to help menu
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    #parse arguments
    args = parser.parse_args()
    return(args)

# define main
def main():
    """run whole daphnia ruler."""
    # parse arguments
    args = parse_args(sys.argv)
    # set source to directory input if it's a valid directory
    source = helpers.is_dir(args.path)

    #if scaling is active check for scaling files. If missing user is asked if he wants to continue
    if args.scaleMM:
        helpers.check_scale(source)

    #if source directory contains images, prcess them
    helpers.process_directory(source, args = args)

    # loop through subdirectories and process the appropriate ones
    for root, dirs, filenames in os.walk(source):
        for d in dirs:
            directory_in = os.path.join(root,d)
            helpers.process_directory(directory_in, args = args)

if __name__ == '__main__':
    # run main
    main()
