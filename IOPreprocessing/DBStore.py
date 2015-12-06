'''
Created on Jan 31, 2011

@author: Blodstone
'''
import re
import pymongo
import time

class DBStore:
    '''
    Wrapping class of pymongo database
    '''
    
    testingRoot = 'E:/Kuliah/Postgraduate/Assignment/CCS590/Experiment/Output/Testing'
    trainingRoot= 'E:/Kuliah/Postgraduate/Assignment/CCS590/Experiment/Output/Training'
    commonRoot = 'E:/Kuliah/Postgraduate/Assignment/CCS590/Experiment/Output/Common'
    
    connection = None
    db = None
    
    @classmethod
    def init(cls, dbName='QAnlp'):
        cls.connection = pymongo.Connection()
        cls.db = cls.connection[dbName]
    
    @classmethod
    def dropColl(cls,collName):
        print 'Dropping collection '+ collName
        cls.db.drop_collection(collName)
    
    @classmethod
    def queryDB(cls,collName):
        return cls.db[collName].find(timeout=False)
    
    @classmethod
    def getDB(cls):
        return cls.db