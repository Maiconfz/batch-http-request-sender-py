'''
Created on Jan 28, 2018

@author: maiconfz
'''


class Request(object):
    '''
    classdocs
    '''

    def __init__(self, data=None, serviceUrl=None, response=None):
        '''
        Constructor
        '''
        self.data = data
        self.serviceUrl = serviceUrl
        self.response = response
        
