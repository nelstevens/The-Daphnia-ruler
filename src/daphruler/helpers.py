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
import filetype
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

# define measurement approach by implementing different exceptions
def measure_except_eye(path):
    """This method deals with the appropriate exceptions that need to be
    handled when measuring several daphnia

    Parameters
    ----------
    path : str
        path to image

    Returns
    -------
    List of measurements and image with results plotted
        

    
    """
    try:
        res = measurement_methods.eye_method_2(path)
        return(res)

    except IndexError as a:
        try:
            res2 = measurement_methods.head_method(path)
            return(res2)

        except IndexError as e:
            pass
    except ValueError as a:
        try:
            res2 = measurement_methods.head_method(path)
            return(res2)

        except IndexError as e:
            pass

    except ZeroDivisionError as z:
        res2 = measurement_methods.head_method(path)
        return(res2)
    
# define measurement approach by implementing different exceptions
def measure_except(path):
    """This method deals with the appropriate exceptions that need to be
    handled when measuring several daphnia

    Parameters
    ----------
    path : str
        path to image

    Returns
    -------
    List of measurements and image with results plotted
        

    
    """
    try:
        res2 = measurement_methods.head_method(path)
        return(res2)

    except IndexError as e:
        pass
# define argparse function to check whether input directory is valid
def is_dir(path):
    """This function checks whether a path is a directory. If so it returns the path to this
    directory

    Parameters
    ----------
    path : str
        path to check if it's a directory

    Returns
    -------
    path if check has passed. Otherwise an error is raised
        

    
    """
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError('input directory: %s is not a valid path' % path)
    else:
        return os.path.abspath(path)

# define function that checks directories for images and scaling files
def check_scale(path):
    """This functions checks the directory tree for the presence and correctness of scaling files in image directories.
    If missing the user is asked if he wants to continue.

    Parameters
    ----------
    path : str
        Path to directory or parent directory where scale.txt file should be.

    Returns
    -------
    nothing
        

    
    """
    # set counter for missing scaling files
    missing_dir = []
    # set list for wrong scaling files
    nt_nr = []
    # first check input directory
    files = os.listdir(path)
    filtered_files = []
    for f in files:
        file_path = os.path.join(path,f)
        if os.path.isfile(file_path) and filetype.image_match(file_path) is not None and '_processed' not in file_path:
            filtered_files.append(file_path)
        else:
            pass
    # if scaling is active check if Scale.txt is in directory. if not exit
    if len(filtered_files)>0:
        if 'Scale.txt' not in files:
            missing_dir.append(path)
    # if file is present check if it's a number
        else:
            json_file = open(os.path.join(path, 'Scale.txt'), 'r', encoding ='utf-8')
            try:
                Scale = json.load(json_file)
                json_file.close()
                sc_factor = Scale['PixelperMM']
            except json.decoder.JSONDecodeError:
                raise ValueError("\n %s cannot be read properly. Please make sure you enter a number or float!" % os.path.join(path, 'Scale.txt'))

            # check if scaling factor is accepted data type
            if not isinstance(sc_factor, (int, float)):
                nt_nr.append(os.path.join(path, 'Scale.txt'))

    # now check subdirectories
    for root, dirs, files in os.walk(path):
        for d in dirs:
            dir_path = os.path.join(root, d)
            files = os.listdir(dir_path)
            filtered_files = []
            for f in files:
                file_path = os.path.join(dir_path,f)
                if  os.path.isfile(file_path) and filetype.image_match(file_path) is not None and '_processed' not in file_path:
                    filtered_files.append(file_path)
                else:
                    pass
            # if scaling is active check if Scale.txt is in directory. if not exit
            if len(filtered_files)>0:
                if 'Scale.txt' not in files:
                    missing_dir.append(dir_path)
            # if scaling file is in directory check if it's an integer or float
                else:
                    json_file = open(os.path.join(dir_path, 'Scale.txt'), 'r', encoding ='utf-8')
                    try:
                        Scale = json.load(json_file)
                        json_file.close()
                        sc_factor = Scale['PixelperMM']
                    except json.decoder.JSONDecodeError:
                        raise ValueError("\n %s cannot be read properly. Please make sure you enter a number or float!" % os.path.join(dir_path, 'Scale.txt'))

                    # check if scaling factor is accepted data type
                    if not isinstance(sc_factor, (int, float)):
                        nt_nr.append(os.path.join(dir_path, 'Scale.txt'))

    #if scaling files are missing ask if user wants to continue
    if len(missing_dir) > 0:
        print("You didn't provide scaling files in the following directories: \n")
        for i in missing_dir: print(i + '\n')
        while True:
            answer = input('These directories will be skipped. continue? (y/n)').lower()
            #define accepted answers
            acc_n_answers = ('n', 'no')
            acc_y_answers = ('y','yes')
            if answer in acc_n_answers:
                sys.exit(0)
            elif answer in acc_y_answers:
                break
            else:
                print('Please enter y or n')
    #if scaling factor is not a number ask user to continue
    if len(nt_nr) > 0:
        print("The following scaling files don't provide numbers!")
        for j in nt_nr: print(j + '\n')
        while True:
            answer = input('These directories will be skipped. continue? (y/n)').lower()
            #define accepted answers
            acc_n_answers = ('n', 'no')
            acc_y_answers = ('y','yes')
            if answer in acc_n_answers:
                sys.exit(0)
            elif answer in acc_y_answers:
                return
            else:
                print('Please enter y or n')





# define function that scales results to mm
def scale_measurements(res, img_dir, sc_factor, args):
    """This function uses the scaling factor from Scale.txt to convert
    measurements from pixels to mm.

    Parameters
    ----------
    res : list
        list with original measurements without scaling
    img_dir : str
        path to image directory
    sc_factor : float
        scaling factor
    args : arguments from cli
        

    Returns
    -------
    List with measurements scaled to mm
        

    
    """
    # scale measurements
    for inst in res:
        # if eye method is activate scale all variables
        if args.eyeMethod:
            try:
                inst['eye.Length'] = round(inst['eye.Length'] / sc_factor, 4)
                inst['tail.Length'] = round(inst['tail.Length'] / sc_factor, 4)
                inst['perimeter'] = round(inst['perimeter'] / sc_factor, 4)
                inst['area'] = round(inst['area'] / sc_factor**2, 4)
                inst['minor'] = round(inst['minor'] / sc_factor, 4)
                inst['full.Length'] = round(inst['full.Length'] / sc_factor, 4)
            # if eye method failed scale left over measurements
            except KeyError:
                inst['perimeter'] = round(inst['perimeter'] / sc_factor, 4)
                inst['area'] = round(inst['area'] / sc_factor**2, 4)
                inst['minor'] = round(inst['minor'] / sc_factor, 4)
                inst['full.Length'] = round(inst['full.Length'] / sc_factor, 4)
            except TypeError:
                    pass
        # if eye method is deactivated scale necessary measurements only.
        else:
            try:
                inst['perimeter'] = round(inst['perimeter'] / sc_factor, 4)
                inst['area'] = round(inst['area'] / sc_factor**2, 4)
                inst['minor'] = round(inst['minor'] / sc_factor, 4)
                inst['full.Length'] = round(inst['full.Length'] / sc_factor, 4)
            except TypeError:
                    pass

    return(res)
def create_df(res, img_dir, args, scaling=None):
    """This function creates a dataframe based on the multiprocessing output (list of dictionaries).

    Parameters
    ----------
    res : list
        List with measurement results
    img_dir : str
        path to image directory
    args : args from cli
        
    scaling : float
        Scaling factor
        (Default value = None)

    Returns
    -------
    Dataframe with measurement results
    """
      # define scale
    scale = scaling
    # remove image to save time
    res = [{k: v for k, v in d.items() if k != "image"} for d in res]
    # if scaling is activated. overwrite results with scaled measurements
    if args.scaleMM:
        res = scale_measurements(res, img_dir, scale, args)
    # define column defs
    if args.eyeMethod:
        nam_mp = {
            'ID': "ID",
            'full.Length': "body.Length.h",
            'eye.Length': "body.Length.e",
            'tail.Length': "tail.Length",
            'perimeter': "body.Perimeter",
            'area': "body.Area",
            'minor': "body.Width",
            'solidity': "solidity",
            'tail.angle': "tail.Angle"
        }
    else:
        nam_mp = {
            'ID': "ID",
            'full.Length': "body.Length.h",
            'perimeter': "body.Perimeter",
            'area': "body.Area",
            'minor': "body.Width",
            'solidity': "solidity"
        }
    df = pd.DataFrame.from_records(res).rename(columns=nam_mp).fillna("NA")
    # reorder columns
    df = df[list(nam_mp.values())]
    return(df)

#define a function that analyses a directory
def process_directory(d, args):
    """This functionen measured all images in a directory if it is not an output directory

    Parameters
    ----------
    d : str
        path to directory
    args : args from cli
        

    Returns
    -------
    nothing
        

    
    """
    if not d.endswith('results'):
        # create list of image files
        files = os.listdir(d)

        # filter files for images
        filtered_files = []
        for k in files:
            file_path = os.path.join(d, k)
            if os.path.isfile(file_path) and filetype.image_match(file_path) is not None and '_processed' not in file_path:
                filtered_files.append(file_path)
            else:
                pass
        # if scaling is active check if Scale.txt is in directory. if not exit
        if len(filtered_files)>0 and args.scaleMM:
            if 'Scale.txt' not in files:
                print(
                    'You did not provide a scaling file in directory: %s ... skipping directory!' % d
                )
                return
            else:
                json_file = open(os.path.join(d, 'Scale.txt'), 'r', encoding ='utf-8')

                Scale = json.load(json_file)
                json_file.close()
                sc_factor = Scale['PixelperMM']

                # check if Scaling.txt provides a number
                if not isinstance(sc_factor, (int, float)):
                    print('%s/Scaling.txt did not provide a number... skipping' % d)
                    return

        # overwrite files with only images
        files = filtered_files

        if len(files) > 0:

            # set start time and print where program is
            start = time.time()
            print('\n Processing ' + d)

            # make directory for results
            if not os.path.exists(os.path.join(d, 'results')):
                os.makedirs(os.path.join(d, 'results'))
            destination = os.path.join(d, 'results')

            # Create a pool of workers (multiprocessing)
            p = Pool(processes = cpu_count() - 1)

            # split work on workers and implement progress bar
            if args.eyeMethod:
                result = list(tqdm(p.imap(measure_except_eye, files), total = len(files)))
            else:
                result = list(tqdm(p.imap(measure_except, files), total = len(files)))
            p.close()
            p.join()

            # Create Dataframe
            print('Writing dataframe')
            if args.scaleMM:
                df = create_df(
                    res = result,
                    img_dir = d,
                    args = args,
                    scaling = sc_factor
                )
            else:
                df = create_df(
                    res = result,
                    img_dir =  d, 
                    args = args
                )

            # write data frame to csv
            df.to_csv(os.path.join(destination,'measurement_results_')+str(os.path.basename(d))+'.csv', index = False)

            # if no -n flag is set write images with measurement overplotted
            if not args.noImages:
                print('writing processed images')
                # loop over results and implement progress bar
                for di in tqdm(result):
                    ID = os.path.basename(di['ID'])+'_processed.png'
                    cv2.imwrite(os.path.join(destination, ID), di['image'])
            # print total elapsed time for directory d
            print('total elapsed time (s): ' + str(time.time()-start))

def process_recursive(source, args):
    """Process input directory and children

    Parameters
    ----------
    source : str
        source directory
        
    args : args from argparser
        

    Returns
    -------
    nothing
    """
    #if source directory contains images, prcess them
    process_directory(source, args = args)

    # loop through subdirectories and process the appropriate ones
    for root, dirs, filenames in os.walk(source):
        for d in dirs:
            directory_in = os.path.join(root,d)
            process_directory(directory_in, args = args)