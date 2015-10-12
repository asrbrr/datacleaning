'''
fleet_helper  module
====================
Convenience functions/classes to deal with machine fleet tags 

Classes:
=======
 - tag_subset : find substrings in the tag names. Returns list

Functions:
=========
 - tag_roots() : find tag roots (assuming xxx01.yyy format)
 - tag_prefixes()  : find tag prefixes(assuming xxx01.yyy format)
'''
 
import re

 
 
class fleet_tag_selector():
    '''
    This class generates a "tag-selector", according to substrins. An exclusion
    can also be stated.
    For convenience, allows square-bracket access, and returns list of tags
    (to be used in pandas for ex)
    
    For example, tag['Val01', 'Power']
    '''
    
    def __init__(self, df=None, colnames=None):
        '''
        df - reference to the df of interest
        colnames - or instead, provide explicit list of column names of df
        '''
        
        if not df is None:
            self._df = df 
            self._colnames = None
        elif not colnames is None:
            self._colnames = list(colnames)
            self._df = None
        else:
            pass

    
    def __getitem__(self, arg):
        '''
        Convenience square bracket accessor for the sub method
         '''
        return self.sub(arg)
        
        
    def sub(self, *substrings, exclude=None, ignorecase=True):
        '''
        Gets a subset of column names, based on substring(s)
        Arguments
        ---------
         - substring : one or more (tuple) susbstrins to search
         - exclude : (optional) substring(s) to exclude. Default=None
        '''
        #Minimum check
        if substrings is None:
            return None
        
        #Prepare the col names
        if not self._df is None:
            colnames = list(self._df.columns)
        else:
            colnames = self._colnames
        
        #Distinguis 1 or several arguments
        if isinstance(substrings, str):
            conditions = (substrings,)
        else:
            conditions = substrings
        
        #Do the subsettig
        subset = colnames
        for cond in conditions:
            if ignorecase:
                subset = [c for c in subset if cond.lower() in c.lower()]
            else:
                subset = [c for c in subset if cond in c]
        if exclude is None:
            return subset
        
        #Look for exclussions
        if isinstance(exclude, str):
            exclussions = (exclude,)
        else:   
            exclussions = exclude        
        for ex in exclussions:
            if ignorecase:
                subset = [c for c in subset if not ex.lower() in c.lower()]
            else:
                subset = [c for c in subset if not ex in c]
        return subset        
    
        
def fleet_tag_roots(df):
    '''
    Return tag roots within the df column names.
    Important: assumes xxx01.yyy format
    '''
            
    regexp = '.*\d\d\.(.*)'
    roottags = set()
    
    for tag in df.columns:
        match = re.match(regexp, tag)
        if match:
            tag = match.groups()[0]
            roottags.add(tag)
    
    return list(sorted(roottags))

    
def fleet_tag_prefixes(df):
    '''
    Return tag prefixes within the df column names.
    Important: assumes xxx01.yyy format
    '''
            
    regexp = '(.*)\d\d\..*'
    prefixes = set()
    
    for tag in df.columns:
        match = re.match(regexp, tag)
        if match:
            tag = match.groups()[0]
            prefixes.add(tag)
    
    return list(sorted(prefixes))
    
    
def fleet_cv_builder(df, func, args, colname):
    '''
    Create calculated variables (CV-s) at fleet level
    
    Arguments
     - df
     - func : to be applied to the df columns
     - args : should be everything after the 01 (ex: xxx01.yyy), including the dot (.)
    '''
    colnames = df.columns
    
    args = list(args)
    
    #Look at first argument
    roottag1 = args.pop()
    #Get all the tags that belong to this rrot_tag
    tags1 = [c for c in colnames if c.endswith(roottag1)]
    #Loop through each
    for tag1 in tags1:
        args1 = [df[tag1]]
        while args:
            roottag2 = args.pop()
            tag2 = tag1.replace(roottag1, roottag2)
            args1.append(df[tag2])
        colname1 = tag1.replace(roottag1, colname)
        df[colname1] = func(*args1)
    return df
    
    





