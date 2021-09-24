# The-Daphnia-ruler manual
## Contents
1. Introduction\
	1a. Measured traits
2. Usage\
	2a. The help menu\
	2b. directory input\
	2c. The Eye method\
	2d. Don't write images with measurements\
	2e. Scale measurements from pixel to another unit of length
3. Output
4. Supported operating systems

## 1. Introduction
The Daphnia ruler is a command line program that allows the collection of 
morphometric data of zooplankton from still images. It was specifically
designed to collect accurate morphometric data of Daphnia using a
combination of edge detection methods and landmarking approaches. Although
the daphnia ruler was designed specifically for Daphnia it may also be
used to collect data for other zooplankton species.

### 1a. Measured traits
![](images/final_product_fin.jpg)

The following traits can be measured in all zooplankton species:
* body size: approximated by fitting an ellipse around the Daphnia body 
(green line)
* body area (area within red outline)
* body perimeter (length of red outline in image)
* body width (purple line in image)

For Daphnia additional features can be measured (for instructions see usage):
* body size: measured from the center of the eye to the base of the tail 
(red line)
* tail length (blue line)
* tail angle (angle between red and blue line)

## 2. Usage and arguments
The Daphnia ruler is simple to use and requires a maximum of four arguments.
Only one argument is mandatory which specifies the path to an input
directory (see 2b. Input). All other arguments are optional, can be combined as desired and will be
described in detail in the corresponding subsections. 

To use the daphnia ruler first install it and its dependencies
(instructions can be found in README.md). Once installed open your
command prompt and navigate into the cloned directory. Note that the
daphnia ruler only works when the working directory contains the following
files:
* daphnia_ruler.py
* measurement_methods.py
* helpers.py
* utils.py

### 2a. The help menu
The help menu very briefly describes the usage of the daphnia ruler and
can be accessed using the -h flag. Your input should look like
this:
```bash
python daphnia_ruler.py -h
```
This command will show all possible arguments the daphnia ruler accepts
plus a short description of each argument.

### 2b. directory input
The input path is specified using the -p flag.
Example:
Windows:
```powershell
python daphnia_ruler.py -p C:\Users\'Username'\input_directory
```
MacOS and Linux:
```bash
python daphnia_ruler.py -p ~/zooplankton_project/input_directory
```
This command specified 'input_directory' as the input for the daphnia ruler.

**The input directory:**
The input directory can either be a directory containing images or a
directory containing subdirectories which contain images. Thus the daphnia
ruler will analyze all images in both the input directory and all its 
subdirectories.

**Images in input directory:**

**What image formats are accepted:**

A variaty of image formats are accepted by the daphnia ruler including jpeg, png,
and tiff. 

**What should an image look like:**
The image should preferably only contain a single zooplankton individual.
However, the daphnia ruler will collect morphometric data of the largest object
in the image. Thus it is possible to have smaller objects in the image as well
which will be ignored by the daphnia ruler. Note however, that objects should
not touch each other.
The daphnia ruler relies on edge detection algorithms. Even though these can
handle a certain amount of noise in the the image it is important to have 
a clear separation of the zooplankton indivdual and the background. A good 
way to achieve this is to photograph individuals on clean microscope slides.
As mentioned in the introduction additional features can be measured for 
Daphnia. In order to do so it is crucial that images are taken by means
of bright field photography.

### 2c. The Eye method
Using the -e flag users can specify whether the localization of the eye should be included in the measurement process. 
When the -e flag is set the daphnia ruler will try to locate the eye in the image and measure the distance from the eye to the base of the tail,
the length of the tail and the angle between the tail (blue line in image) and the body length (red line in image).
Your input should look like this:
Windows:
```powershell
python daphnia_ruler.py -e -p C:\Users\'Username'\input_directory
```
MacOS and Linux:
```bash
python daphnia_ruler.py -e -p ~/zooplankton_project/input_directory
```
The eye method can be very usefull in measuring daphnia by potentially improving measurement accuracy since this method relies less on acurate masking of the daphnia body.
However it is only usefull in measuring daphnia with visible eyes. For all other zooplankton species this method is not of use.

### 2d. Don't write images with measurements
Using the -n flag disables the writing of images with measurements overploted. Having images with measurements overploted is useful for checking individual measurements for their accuracy. However with large samples or limited storage space one might prefer not to have this output. 
Writing images to disk can be disabled with the following code:\
Windows:
```powershell
python daphnia_ruler.py -n -p C:\Users\'Username'\input_directory
```
MacOS and Linux:
```bash
python daphnia_ruler.py -n -p ~/zooplankton_project/input_directory
```
### 2e. Scale measurements from pixel to another unit of length
The -s flag enables scaling of measurements. Note that this requires a file called Scale.txt in each directory containing images.\
A template for this file can be found in the github repository Github.com/nelstevens/The-Daphnia-ruler. Copy this file to each directory containing images and exchange NUM to the desired scaling factor. For instance if 100 pixels in an image corresponds to 1 cm of length exchange NUM with 100. If NUM is exchanged by a non valid entry (not a number) the daphnia ruler will throw an error. If a directory does not contain the Scale.txt file the user is asked wether this directory should be skipped or not.
The following code enables scaling:\
Windows:
```powershell
python daphnia_ruler.py -s -p C:\Users\'Username'\input_directory
```
MacOS and Linux:
```bash
python daphnia_ruler.py -s -p ~/zooplankton_project/input_directory
```

## 3. Output
The daphnia ruler will create a subfolder in each directory of the input 
that contains images. These subfolders will be named results and contain 
a copy of each image 
with results overplotted (unless argument -n is 
active; see 2d). This new subfolder will also include a single 
csv file containing all measurements for each image in the original
directory.

## 4. supported operating Systems
The Daphnia ruler is tested on Windows, macOS and Ubuntu (Linux). If errors occur please open an issue on Github preferably with a reproducable example.
