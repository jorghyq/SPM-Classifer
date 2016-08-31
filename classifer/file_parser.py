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
import pandas as pd
from nanonisdatfile import NanonisDat
from nanonisfile import NanonisFile

type_dict = {'txt': 1, 'sxm': 2, 'dat': 3, '3ds': 4}
m2nm = 1e9


class FileParser:
    # parser for files

    def __init__(self):
        #self.param = {}
        #self.param['file_type'] = 0
        #self.param['file_format'] = 0
        #self.param['complete'] = True
        #self.param['square'] = True

    def load_file(self, path):
        self.full_path = path
        self.path, self.name= os.path.split(self.full_path)
        print self.full_path
        print self.path, self.name

    def parsing(self):
        self.param = {}
        self.param['path'] = self.path
        self.param['name'] = self.name
        self.param['file_type'] = 0
        self.param['file_format'] = 0
        self.param['complete'] = True
        self.param['square'] = True
        ending = self.name.split('.')[-1]
        print ending
        # determine the file_format
        if ending in type_dict.keys():
            self.param['file_type'] = type_dict[ending]
        # determine the format_type
        try:
            if ending == 'sxm':
                file_sxm = NanonisFile(self.full_path)
                header = file_sxm.header
                # check if the feedback on
                if header['z-controller>controller status'] == 'ON':
                    self.param['file_format'] = 0
                else:
                    self.param['file_format'] = 1
                # check the size and if square
                pixel = header['scan_pixels']
                size = header['scan_range']
                size[0] = size[0]*m2nm
                size[1] = size[1]*m2nm
                if pixel[0] == pixel[1]:
                    self.param['square'] = True
                else:
                    self.param['square'] = False
                self.param['pixel1'] = pixel[0]
                self.param['pixel2'] = pixel[1]
                self.param['size1'] = size[0]
                self.param['size2'] = size[1]
                self.param['ratio'] = pixel[0]*pixel[1]/(size[0]*size[1])
                # check if it complete, by calculating the acq time
                time_true = header['acq_time']
                scan_time = header['scan_time']
                time_full = pixel[0]*scan_time[0] + pixel[1]*scan_time[1]
                if abs(time_true - time_full) < 1:
                    self.param['complete'] = True
                else:
                    self.param['complete'] = False
            elif ending == 'dat':
                file_dat = NanonisDat(self.full_path)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            pass
        #return self.param['file_type']

    def print_results(self):
        for k, v in self.param.iteritems():
            print k, v

    def write_to_csv(self,f):
        pass
    def write_to_db(self):
        pass

class Controller():
    # manage all the files

    def __init__(self):
       self.parser = FileParser()
       self.columns = ['filename','filetype','fileformat','pixel1','pixel2',\
                      'size1','size2','ratio','finished','quality','type']
       self.count = 0

    def init_table(self):
        # initialize with
        self.table = pd.DataFrame(columns=self.columns)

    def load_table(self):
        pass

    def update_entry(self,row,column):
        pass

    def update_row(self,row):
        pass



if __name__ == "__main__":
    fdir = '/home/jorghyq/Data/201511/'
    files = os.listdir(fdir)
    parser = FileParser()
    for item in files:
        #print item
        parser.load_file(fdir+item)
        parser.parsing()
        parser.print_results()

