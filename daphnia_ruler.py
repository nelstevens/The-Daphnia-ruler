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
import measurement_methods
import imghdr
import pandas as pd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse
from pathlib import Path

# define measurement approach by implementing different exceptions
def measure_except(path):
    '''
    This method deals with the appropriate exceptions that need to be
    handled when measuring several daphnia
    '''
    if args.eyeMethod:
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
    else:
         try:
            res2 = measurement_methods.head_method(path)
            return(res2)

         except IndexError as e:
                pass

# define argparse function to check whether input directory is valid
def is_dir(path):
    '''
    This function checks whether a path is a directory. If so it returns the path to this
    directory
    '''
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError('input directory: %s is not a valid path' % path)
    else:
        return os.path.abspath(path)

# define function that checks directories for images and scaling files
def check_scale(path):
    '''
    This functions checks the directory tree for the presence and correctness of scaling files in image directories.
    If missing the user is asked if he wants to continue.
    '''
    # set counter for missing scaling files
    missing_dir = []
    # set list for wrong scaling files
    nt_nr = []
    # first check input directory
    files = os.listdir(path)
    filtered_files = []
    for f in files:
        file_path = os.path.join(path,f)
        if os.path.isfile(file_path) and imghdr.what(file_path) is not None and '_processed' not in file_path:
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
                print("\n %s cannot be read properly. Please make sure you enter a number or float!" % os.path.join(path, 'Scale.txt'))
                sys.exit(0)

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
                if  os.path.isfile(file_path) and imghdr.what(file_path) is not None and '_processed' not in file_path:
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
                        print("\n %s cannot be read properly. Please make sure you enter a number or float!" % os.path.join(dir_path, 'Scale.txt'))
                        sys.exit(0)

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
def scale_measurements(res, img_dir, sc_factor):
    '''
    This function uses the scaling factor from Scale.txt to convert 
    measurements from pixels to mm.
    '''
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

# define function that creates a datframe based on result dictionaries
def create_df(res, img_dir, scaling=None):
    '''
    This function creates a dataframe based on the multiprocessing output (list of dictionaries).
    '''
    # define scale
    scale = scaling
    # if scaling is activated. overwrite results with scaled measurements
    if args.scaleMM:
        res = scale_measurements(res, img_dir, scale)


    # if eye method is activated provide column for it
    if args.eyeMethod:
            df = pd.DataFrame(columns = ['ID', 'body.Length.h','body.Length.e', 'tail.Length',
            'body.Perimeter', 'body.Area', 'body.Width', 'solidity', 'tail.Angle'])
            # loop through results and append to dataframe
            for di in tqdm(res):
                try:
                    df = df.append({'ID': di['ID'], 'body.Length.h': di['full.Length'],
                    'body.Length.e': di['eye.Length'],
                    'tail.Length': di['tail.Length'], 'body.Perimeter': di['perimeter'],
                    'body.Area': di['area'], 'body.Width': di['minor'],
                    'solidity': di['solidity'], 'tail.Angle': di['tail.angle']}, ignore_index=True)
                # if Landmark method failed
                except KeyError:
                        df = df.append({'ID': di['ID'], 'body.Length.h': di['full.Length'],
                        'body.Perimeter': di['perimeter'],
                        'body.Area': di['area'], 'body.Width': di['minor'],
                        'solidity': di['solidity']}, ignore_index=True).fillna('NA')
                # if everything failed
                except TypeError:
                    pass
    else:
        df = pd.DataFrame(columns = ['ID', 'body.Length.h', 'body.Perimeter',
        'body.Area', 'body.Width', 'solidity'])
        for di in tqdm(res):
                try:
                        df = df.append({'ID': di['ID'], 'body.Length.h': di['full.Length'],
                        'body.Perimeter': di['perimeter'],
                        'body.Area': di['area'], 'body.Width': di['minor'],
                        'solidity': di['solidity']}, ignore_index=True).fillna('NA')
                # if everything failed
                except TypeError:
                    pass
    return(df)

#define a function that analyses a directory
def process_directory(d):
    '''
    This functionen measured all images in a directory if it is not an output directory
    '''
    if not d.endswith('results'):
        # create list of image files
        files = os.listdir(d)

        #filter files for images
        filtered_files = []
        for k in files:
            file_path = os.path.join(d,k)
            if  os.path.isfile(file_path) and imghdr.what(file_path) is not None and '_processed' not in file_path:
                filtered_files.append(file_path)
            else:
                pass
        # if scaling is active check if Scale.txt is in directory. if not exit
        if len(filtered_files)>0 and args.scaleMM:
            if 'Scale.txt' not in files:
                print('You did not provide a scaling file in directory: %s ... skipping directory!' % d)
                return

            else:
                json_file = open(os.path.join(d, 'Scale.txt'), 'r', encoding ='utf-8')

                Scale = json.load(json_file)
                json_file.close()
                sc_factor = Scale['PixelperMM']

                #check if Scaling.txt provides a number
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
            if not os.path.exists(os.path.join(d,'results')):
                os.makedirs(os.path.join(d,'results'))
            destination = os.path.join(d,'results')


            # Create a pool of workers (multiprocessing)
            p = Pool(processes = cpu_count() - 1)

            # split work on workers and implement progress bar
            result = list(tqdm(p.imap(measure_except, files), total = len(files)))
            p.close()
            p.join()

            # Create Dataframe
            print('Writing dataframe')
            if args.scaleMM:
                df = create_df(result, d, scaling=sc_factor)
            else:
                df = create_df(result, d)

            # write data frame to csv
            df.to_csv(os.path.join(destination,'measurement_results.')+str(os.path.basename(d))+'.csv', index = False)

            # if no -n flag is set write images with measurement overplotted
            if not args.noImages:
                print('writing processed images')
                # loop over results and implement progress bar
                for di in tqdm(result):
                    ID = os.path.basename(di['ID'])+'_processed.png'
                    cv2.imwrite(os.path.join(destination, ID), di['image'])
            # print total elapsed time for directory d
            print('total elapsed time (s): ' + str(time.time()-start))

# use argparse to create optional arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help='Path to your input directory. The program is able to loop through subdirectories of the input.', type=is_dir)
parser.add_argument('-n', '--noImages', help="Don't write images with results overplotted.", action='store_true')
parser.add_argument('-e', '--eyeMethod', help="Implement eye method on top of ellipse method.", action='store_true')
parser.add_argument('-s', '--scaleMM', help="Scale measurement to mm. For more information see README.md", action='store_true')

#if no arguments are provided go to help menu
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

#parse arguments
args = parser.parse_args()



if __name__ == '__main__':

    # set source to directory input if it's a valid directory
    source = is_dir(args.path)

    #if scaling is active check for scaling files. If missing user is asked if he wants to continue
    if args.scaleMM:
        check_scale(source)

    #if source directory contains images, prcess them
    process_directory(source)

    # loop through subdirectories and process the appropriate ones
    for root, dirs, filenames in os.walk(source):
        for d in dirs:
            directory_in = os.path.join(root,d)
            process_directory(directory_in)
