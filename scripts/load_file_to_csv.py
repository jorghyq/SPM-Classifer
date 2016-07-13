# load file to csv file

import os
import csv

start_dir = '/home/jorghyq/Data'

files = []
dir_to_complete = [start_dir]

#for root, dirs, files in os.walk('/home/jorghyq/Downloads'):
#    for name in files:
#        print name
    #for name in dirs:
    #    print os.path.join(root, name)

while (len(dir_to_complete) > 0):
    search_dir = dir_to_complete.pop()
    print search_dir
    if search_dir == start_dir:
        for item in os.listdir(search_dir):
            if os.path.isdir(os.path.join(search_dir,item)):
                dir_to_complete.append(item)
            else:
                files.append(item)
    else:
        search_dir_full = os.path.join(start_dir,search_dir)
        for item in os.listdir(search_dir_full):
            if os.path.isdir(os.path.join(search_dir_full,item)):
                dir_to_complete.append(os.path.join(search_dir,item))
            else:
                files.append(os.path.join(search_dir,item))
#print files
with open('file_names.txt','w') as f:
    writer = csv.writer(f)
    for row in files:
        writer.writerow([row])

