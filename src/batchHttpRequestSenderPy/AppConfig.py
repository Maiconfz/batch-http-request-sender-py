'''
Created on Jan 28, 2018

@author: maiconfz
'''


class AppConfig(object):
    '''
    classdocs
    '''

    def __init__(self, defaultServiceUrl, requestsCsvFilePath, threadsNumber=1, verbose=True):
        '''
        Constructor
        '''
        self.defaultServiceUrl = defaultServiceUrl
        self.requestsCsvFilePath = requestsCsvFilePath
        self.threadsNumber = threadsNumber if threadsNumber is not None else 1
        self.verbose = verbose if verbose is not None else True
        
