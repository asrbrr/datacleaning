'''
plots module
============

'''

import matplotlib.pyplot as plt

class interactive_plot():
    '''
    
    '''
    
    def __init__(self, i):
        #TO-DO: work the i argument
        plt.interactive(True)
        self._figure = plt.figure()
        
        ax = f.add_subplot()   #<- TO-DO: depending on intended axes and geometries
        
        '''
        ax_scatt
        ax_ts
        ax_hist
        ax.box
        '''
        
        
    def close(self):
        f = self._figure
        f.close()
    
    def fleet(self):
        pass
        
    
    