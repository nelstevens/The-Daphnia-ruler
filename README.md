# The-Daphnia-ruler
Automatically collect morphometric traits of Daphnia.

![](images/final_product_fin.jpg)
## Overview
The Daphnia ruler is a command line program that can measure morphometric traits of Daphnia from images taken under a microscope. 
The Daphnia ruler works in both windows and linux and can measure the following traits:
* body size: measured from the center of the eye to the base of the tail (red line in image)
* body size: approximated by fitting an ellipse around the Daphnia body (green line in image)
* tail length (blue line in image)
* tail angle
* body area (area within red outline in image)
* body perimeter (length of red outline in image)
* body width (purple line in image)


## Installation
The fastest way to get your system setup is to make sure you've installed python 3 (https://www.python.org/) and clone this repository to your local drive.
Once complete use the package manager pip to install the necessary dependencies:
1. Open your command prompt and navigate to the cloned directory
2. Run this command: 
```bash
pip install -r requirements.txt
```
Users who wish to install dependencies manually run:
```bash
pip install opencv-python
pip install scikit-image
pip install pandas
pip install tqdm
```
## Usage
For detailed information on how to use the Daphnia ruler see Manual.md.

```bash
usage: python daphnia_ruler.py [-h] [-p PATH] [-n] [-e] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to your input directory. The program is able to
                        loop through subdirectories of the input.
  -n, --noImages        Don't write images with results overplotted.
  -e, --eyeMethod       Implement eye method on top of ellipse method.
  -s, --scaleMM         Scale measurement to mm. For more information see
                        Manual.md.
```

## Author
* Nelson Stevens
* Contact: nelson.stevens92@gmail.com
