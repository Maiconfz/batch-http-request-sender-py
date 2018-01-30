'''
Created on Jan 28, 2018

@author: maiconfz
'''
from threading import Thread
import urllib.request


class RequestSenderThread(Thread):
    '''
    classdocs
    '''

    def __init__(self, name, appConfig, pendingProcessIndexes, requests):
        '''
        Constructor
        '''
        super(RequestSenderThread, self).__init__(name=name)
        self.appConfig = appConfig
        self.pendingProcessIndexes = pendingProcessIndexes
        self.requests = requests
    
    def run(self):
        while not self.pendingProcessIndexes.empty():
            try:
                i = self.pendingProcessIndexes.get()
                print('Thread', self.name, ' sending request', i)
                request = self.requests[i-1]
                
                response = urllib.request.urlopen(request.serviceUrl, request.data.encode())
                request.response = response
            except Exception as e:
                print(str(e))