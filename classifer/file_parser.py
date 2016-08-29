# This file pre parses the file and extract the important information
############################################
# file_type:    0     others               #
#               1     txt                  #
#               2     sxm                  #
#               3     dat                  #
#               4     3ds                  #
############################################
# file_format:  0     STM                  #
#               1     AFM                  #
#               2     dI/dV map            #
#               3     dI/dV                #
#               4     Force curve          #
############################################


import numpy as np
import os
import csv
from nanonisdatfile import NanonisDat
from nanonisfile import NanonisFile

type_dict = {'txt': 1, 'sxm': 2, 'dat': 3, '3ds': 4}

class FileParser:
    # parser for files

    def __init__(self):
        self.file_type = 0
        self.format_type = 0
        self.complete = True
        self.square = True

    def load_file(self, path):
        self.full_path = path
        self.path, self.name= os.path.split(self.full_path)
        print self.full_path
        print self.path, self.name

    def parsing(self):
        ending = self.name.split('.')[-1]
        # determine the file_format
        if ending in type_dict.keys():
            self.file_type = type_dict[ending]
        # determine the format_type
        try:
            if ending == 'sxm':
                file_sxm = NanonisFile(self.full_path)
                header = file_sxm.header
                # check if the feedback on
                if header['z-controller>controller status'] == 'ON':
                    self.file_format = 0
                else:
                    self.file_format = 1
                # check the size and if square
                pixel = header['scan_pixels']
                size = header['scan_range']
                if pixel[0] == pixel[1]:
                    self.square = True
                else:
                    self.square = False
                # check if it complete, by calculating the acq time
                time_true = header['acq_time']
                scan_time = header['scan_time']
                time_full = pixel[0]*scan_time[0] + pixel[1]*scan_time[1]
                if abs(time_true - time_full) < 1:
                    self.complete = True
                else:
                    self.complete = False
            elif ending == 'dat':
                file_dat = NanonisDat(self.full_path)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            pass
        return self.file_type #,file_format,file_finished,file_pixel

if __name__ == "__main__":
    fdir = '/home/jorghyq/Data/201511/'
    files = os.listdir(fdir)
    parser = FileParser()
    for item in files:
        #print item
        parser.load_file(fdir+item)
        print parser.parsing()

