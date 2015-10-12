'''
Various utilities to deal with sets of files
'''

import csv
import os
import glob
from os import listdir
    
def file_iterator(path):
    if os.path.isfile(path):
        #this means it's a path to a unique file
        data_files = [os.path.abspath(path)]
        
    if os.path.isdir(path):
        #this means it's a path to dir
        abspath = os.path.abspath(path)
        data_files = [ os.path.join(abspath,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
        
    elif '*' in path or '?' in path or '[' in path:
        #this means it must be a glob route or a folder
        data_files = glob.glob(path)
        
    else:
        #assume it's a file-like object
        data_files = [path]
    
    for file in data_files:
        yield file
    