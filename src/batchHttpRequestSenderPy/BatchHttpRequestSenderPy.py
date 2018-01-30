'''
Created on Jan 28, 2018

@author: maiconfz
'''

import csv

from batchHttpRequestSenderPy.Request import Request
from batchHttpRequestSenderPy.RequestFileConfig import RequestFileConfig
from batchHttpRequestSenderPy.RequestSenderThread import RequestSenderThread
from queue import Queue


class BatchHttpRequestSenderPy(object):
    '''
    classdocs
    '''

    def __init__(self, appConfig):
        '''
        Constructor
        '''
        self.appConfig = appConfig
        
        self.requestFileConfig = RequestFileConfig()
        self.pendingProcessIndexes = Queue()
        self.requests = []

    def run(self):
        '''
        Executes the app
        '''
        if self.appConfig.verbose:
            self.printConfig()
        
        self.createRequestsFromFile()
        self.sendRequests()
    
    def createRequestsFromFile(self):
        '''
        '''
        csvFile = open(self.appConfig.requestsCsvFilePath, 'r')
        reader = csv.reader(csvFile)
        pendingProcessIndex = 0
        
        headerRow = next(reader)
        self.discoverColumnsPositions(headerRow)
        
        for row in reader:
            self.pendingProcessIndexes.put(pendingProcessIndex)
            pendingProcessIndex += 1
            
            data = ''
            serviceUrl = self.appConfig.defaultServiceUrl
            
            if self.requestFileConfig.dataColumnIndex >= 0 and len(row[self.requestFileConfig.dataColumnIndex]) > 0:
                data = row[self.requestFileConfig.dataColumnIndex]
            
            if self.requestFileConfig.serviceUrlColumnIndex >= 0 and len(row[self.requestFileConfig.serviceUrlColumnIndex]) > 0:
                serviceUrl = row[self.requestFileConfig.serviceUrlColumnIndex]
                
            self.requests.append(Request(data, serviceUrl))
                
        csvFile.close()
    
    def discoverColumnsPositions(self, headerRow):
        
        if 'data' in headerRow:
            self.requestFileConfig.dataColumnIndex = headerRow.index('data')
        else:
            self.requestFileConfig.dataColumnIndex = -1
        
        if 'serviceUrl' in headerRow:
            self.requestFileConfig.serviceUrlColumnIndex = headerRow.index('serviceUrl')
        else:
            self.requestFileConfig.serviceUrlColumnIndex = -1
    
    def sendRequests(self):
        for i in range(1, self.appConfig.threadsNumber + 1):
            thread = RequestSenderThread(str(i), self.appConfig, self.pendingProcessIndexes, self.requests)
            thread.start()            
    
    def printConfig(self):
        '''
        '''
        print('defaultServiceUrl:', self.appConfig.defaultServiceUrl)
        print('requestCsvFilePath:', self.appConfig.requestsCsvFilePath)
        print('threadsNumber:', self.appConfig.threadsNumber)
