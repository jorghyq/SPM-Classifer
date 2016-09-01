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
        pass
        self.columns = ['filename','filetype','fileformat','pixel1','pixel2',\
                      'size1','size2','ratio','complete','quality','type']
        #self.param = {}
        #self.param['file_type'] = 0
        #self.param['file_format'] = 0
        #self.param['complete'] = True
        #self.param['square'] = True

    def load_file(self, path):
        self.full_path = path
        self.path, self.name= os.path.split(self.full_path)
        #print self.full_path
        #print self.path, self.name

    def parsing(self):
        self.param = {}
        #self.param['path'] = self.path
        self.param['filename'] = self.name
        self.param['filetype'] = 0
        self.param['fileformat'] = 0
        self.param['complete'] = True
        self.param['square'] = True
        self.param['quality'] = 0
        self.param['type'] = 0
        self.ending = self.name.split('.')[-1]
        #print self.ending
        # determine the file_format
        if self.ending in type_dict.keys():
            self.param['filetype'] = type_dict[self.ending]
        # determine the format_type
        try:
            if self.ending == 'sxm':
                file_sxm = NanonisFile(self.full_path)
                header = file_sxm.header
                # check if the feedback on
                if header['z-controller>controller status'] == 'ON':
                    self.param['fileformat'] = 0
                else:
                    self.param['fileformat'] = 1
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
                self.param['size1'] = round(size[0],1)
                self.param['size2'] = round(size[1],1)
                self.param['ratio'] = round((pixel[0]*pixel[1]/(size[0]*size[1])),1)
                # check if it complete, by calculating the acq time
                time_true = header['acq_time']
                scan_time = header['scan_time']
                time_full = pixel[0]*scan_time[0] + pixel[1]*scan_time[1]
                if abs(time_true - time_full) < 1:
                    self.param['complete'] = True
                else:
                    self.param['complete'] = False
            elif self.ending == 'dat':
                file_dat = NanonisDat(self.full_path)
            else:
                pass
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

    def output_to_csv(self):
        # prepare the format as list
        output = []
        if self.ending == 'sxm':
            for item in self.columns:
                output.append(self.param[item])
            print output
        return output


class Controller():
    # manage all the files

    def __init__(self, list_path):
       self.parser = FileParser()
       self.columns = self.parser.columns
       self.count = 0
       self.list_path = list_path

    def init_table(self):
        # initialize with
        self.table = pd.DataFrame(columns=self.columns)
        with open(self.list_path,'r') as f:
            lines = f.readlines()
        for line in lines:
            self.parser.load_file(line)
            self.parser.parsing()
            self.parser.output_to_csv()
            if self.parser.param['filetype'] == 2:
                print line
                self.table.loc[self.count] = self.parser.output_to_csv()
                self.count = self.count + 1
                print "saved to entry %d", self.count

    def load_table(self):
        pass

    def update_entry(self,row,column):
        pass

    def update_row(self,row):
        pass

    def write_table(self):
        pass



if __name__ == "__main__":
    fdir = '/home/jorghyq/Data/201511/'
    files = os.listdir(fdir)
    parser = FileParser()
    #for item in files:
        #print item
        #parser.load_file(fdir+item)
        #parser.parsing()
        #parser.print_results()
        #parser.output_to_csv()
    cl = Controller('../scripts/file_names.txt')
    cl.init_table()
