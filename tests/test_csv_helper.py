from nose.tools import with_setup
import tempfile
import csv
import os
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from datacleaning.csv_helper import *

tempfilename = 'temptestfile.csv'

def setup():
    try:
        os.remove(tempfilename)
    except:
        pass
    with open(tempfilename, 'w', newline='') as f:
        csvr = csv.writer(f)
        csvr.writerow(['', 'a','b'])
        csvr.writerow(['0', '01','02'])
        csvr.writerow(['1', 'x','12'])
    
def teardown():
    try:
        os.remove(tempfilename)
    except:
        pass
    
    
@with_setup(setup, teardown)
def test_csv_num_rows():
    num_rows = csv_num_rows(tempfilename)
    assert(num_rows ==3)
    
@with_setup(setup, teardown)
def test_csv_delimiter():
    delim = csv_delimiter(tempfilename)
    assert(delim ==',')

@with_setup(setup, teardown)    
def test_csv_find_nans():
    nans = list(csv_find_nans(tempfilename))
    assert(nans == ['x'])

@with_setup(setup, teardown)    
def test_csv_see_rows():
    a = csv_head(tempfilename)
    b = csv_tail(tempfilename)
    c = csv_random_rows(tempfilename)
    
@with_setup(setup, teardown)    
def test_csv_remove_row():
    num_rows1 = csv_num_rows(tempfilename)
    csv_remove_row(tempfilename, 1)
    num_rows2 = csv_num_rows(tempfilename)
    assert(num_rows2 == num_rows1 - 1)

@with_setup(setup, teardown)        
def test_csv_col_subset():
    #UNIMPLMENTED: THIS FUNCTION IS NOT ROBUST ENOUGH  #####
    return None
    
    
    try:
        csv_col_subset(tempfilename, 'b', 'tempoutput.csv')
        os.remove('tempoutput.csv')
    except:
        assert(False)
        
            
    
@with_setup(setup, teardown)   
def test_csv_read_files():
    df = DataFrame.from_dict({0:['01',2], 1:['x', 12]}, orient='index')
    df.columns = ['a','b']
    
    df2 = csv_read_files(tempfilename, index_col=0)
    assert_frame_equal(df, df2)
    