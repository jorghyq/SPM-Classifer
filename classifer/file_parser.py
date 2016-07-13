# This file pre parses the file and extract the important information
############################################
# file_type:    0     others               #
#               1     txt                  #
#               2     sxm                  #
#               3     dat                  #
#               4     3ds                  #
############################################
# file_format:  0     STM
#               1     AFM
#               2     dI/dV map
#               3     dI/dV
#               4     Force curve
###########################################


import numpy as np
import os
import csv
from nanonisdatfile import NanonisDat
from nanonisfile import NanonisFile

pre_dir = '.'

def preparser(file_name):
    path, name = os.path.split(file_name)
    ending = name.split('.')[-1]
    print path, name, ending
    if ending == 'sxm':
        file_type = 2
        try:
            file_sxm = NanonisFile(file_name)
            # check if the feedback on
            # check if it complete
            # check the size and if square
            #





    return file_type,file_format,file_finished,file_pixel



if __name__ == "__main__":
    files = os.listdir('../test/')
    for item in files:
        print item
        preparser(item)

