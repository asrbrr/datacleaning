'''
csv_helper  - convenience functions to work on csv data files
==========

Helps review and somewhat mungle CSV files. Typically, this would be done 
before a pd.read_csv(), as a conevenience tool to identify NA values, 
know data types etc

Functions
=========
 - csv_num_rows() :       returns number of rows in the CSV files
 - csv_delimiter() :    infer delimeter
 - csv_head() :         head, as in pd
 - csv_tail() :         tail, as in pd
 - csv_random_rows() :    show rows at random
 - csv_find_nans() :      not-numeric values
 - csv_remove_row() :     remove row
 - csv_col_subset () :    take subset of cols 
 - csv_read_files() :      read set of files into single df
'''


from datacleaning.file_helper import file_iterator
import pandas as pd


def csv_num_rows(filepath):
    '''
    Returns number of rows in the CSV files
    Arguments:
    ---------
     - f : file-like object
    Returns: 
    --------
     - lines : integer, number of rows in files (including empty rows!)
    '''

    lines = 0
    with open (filepath, 'r') as f:
        for line in f:
            lines += 1
    return lines


def csv_delimiter(filepath):
    '''
    Returns the infered delimiter of the CSV file.
    Arguments:
    ---------
     - filepath : file-like object
    Returns: 
    --------
     - delimiter : string
    '''
    import csv
    with open(filepath , 'r') as f:
        dialect = csv.Sniffer().sniff(f.read(9999))
    return(dialect.delimiter)


def csv_head(filepath, nrows=5, nchars=70):
    '''
    Prints the first N rows, and the first M characters of each row, for 
    visual inspection.
    Arguments
    ---------
     - filepath : file-like object
     - nrows : optional, integer, number of rows to show. Default=5
     - nchars : optinal, integer, number of characters of each row to show.
            Use None or -1 to show all the line
    Returns
    -------
     - list of nrows head  rows
     '''

    head = []
    with open(filepath , 'r') as f:           
        for i, line in enumerate(f):
            if i == nrows:
                break
            values = line[:nchars]
            head.append(values) 
    return head


def csv_tail(filepath, nrows=5, nchars=70):
    '''
    Prints the last N rows, and the first M characters of each row, for 
    visual inspection.
    Arguments
    ---------
     - filepath : file-like object
     - nrows : optional, integer, number of rows to show. Default=5
     - nchars : optinal, integer, number of characters of each row to show.
            Use None or -1 to show all the line
    Returns
    -------
     - list of nrows tail  rows
     '''

    tail = []
    totalrows = csv_num_rows(filepath)
    with open(filepath, 'r') as f:           
        for i, line in enumerate(f):
            if i < totalrows - nrows:
                continue
            values = line[:nchars]
            tail.append(values) 
    return tail


def csv_random_rows(filepath, nrows=5, nchars=70):
    '''
    Prints a bunch of random rows, in case head and tail contained misleading
    values.
    Arguments
    ---------
     - filepath : file-like object
     - nrows : optional, integer, number of rows to show. Default=5
     - nchars : optinal, integer, number of characters of each row to show.
            Use None or -1 to show all the line
    Returns
    -------
     - list of nrows random rows rows
     '''

    import random
    totalrows = csv_num_rows(filepath)
    randrows = [random.randint(1,totalrows) for _ in range(nrows)]
    values = []
    with open(filepath, 'r') as f:           
        for i,line in enumerate(f):
            if i in randrows:
                value = line[:nchars]
                values.append(value)
    return values


def csv_find_nans(filepath, hasheaders = True, hasindexcol=True):
    '''
    Passes through the columns 'the old way' (iterating)
    and enumerates non-numeric fields to be used as NaN identifiers
    
    Arguments:
    ----------
     - path : file object to be analysed. Assumes CSV format-
     - hasheaders : optional, default=True. Whether to skip first line
     - hasindexcol : optional, default=True. Whether to skip first col
    
    Returns: 
     - nan_list : set with nan values found
    '''
    import csv
    exceptions = set()

    with open(filepath) as f:
        csvr = csv.reader(f)
        for line in csvr:
            if hasheaders:
                hasheaders = False
                continue
            for item in line[hasindexcol:]:
                try:
                    float(item)
                except:
                    exceptions.add(item)
        return exceptions


def csv_remove_row(filepath, nrow):
    '''
    Removes the nrow-th row (starting at 0) of the CSV file.
    It does this by rewritting, so it's probably pretty little efficient.
    Arguments:
     - nrow : number of row to remove. If < 0, it will be understood 
              as standard list[:-1] syntax
    Returns:
     - modifies the file with removed row
     - show removed row
    '''

    import os
    lines = []
    with open(filepath, 'r') as f:
        for i,line in enumerate(f):
            if i != nrow:
                lines.append(line)
    os.remove(filepath)

    with open(filepath, 'x') as f: #this should create and write
        for line in lines:
            f.write(line)

            
def csv_col_subset(filename, pattern, outputfile, include_first=True):
    '''
    Creates a new csv with a subset of the columns of the given csv.
    Used pandas to do this for convenience
    
    Arguments
    ---------
     - filename : file path or object
     - pattern : currently, a substring to be located with the 'in' statement
                 Accepts list, so as to provide several patterns to include.
     - outputfile : file path or object
     - include_first : optional, default True. Whether to add the first col (typically, index)
     
    Returns
    --------
      - CSV file in the given directory
    '''
    
    import csv
    import pandas as pd
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        colnames = reader.fieldnames
    coltypes = {col:object for col in colnames}

    #Get the data into a DF, "as is" (objects)
    df = pd.read_csv(filename, engine='c', dtype=coltypes)

    #Prepare the columns that we will output
    if isinstance(pattern, str):
        pattern = list(pattern)
    
    subset_cols = []
    for patt in pattern:
        cols = [col for col in df.columns if patt in col]
        subset_cols.extend(cols)
        
    
    if include_first:
        subset_cols.insert(0, colnames[0])

    #Prepare the subset of the dataframe of interest
    subset_df = df[subset_cols]

    #Export
    subset_df.to_csv(outputfile, index=False, na_rep='NaN')

    
def csv_read_files(csv_path, **kwargs):    
    '''
    Reads all the csv files in the path, and constructs a single df.
    Assummes files have compatible row indexes, and different column names.
    
    Arguments
    ---------
     - csv_path : path to folder (allows glob expressions for the files)
     - kwargs : to be used in pd.read_csv
     
    Returns
    -------
     - df : dataframe
    '''
    
    df = pd.DataFrame()
    
    #Iterate each file and append to the collective dataframe
    for f in file_iterator(csv_path):
        df1 = pd.read_csv(f, **kwargs )
        df = df.join(df1, how='outer')
    return df