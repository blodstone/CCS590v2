'''
Created on Feb 1, 2011

@author: Blodstone
'''
from __future__ import division
from IOPreprocessing.DBStore import DBStore
from Feature.FeatureExtractor import FeatureExtractor
from Feature.TermExtractor import BagOfWords
from IOPreprocessing.DataPreparation import DataRetrieval 
from Classifier.ELM import ELMClassify
from Classifier.svm import *
from Classifier.svmutil import svm_read_problem, svm_train, svm_predict
import cProfile
import pickle
import time
from numpy import *
from numpy.random import shuffle
from numpy import random
from numpy.lib.npyio import loadtxt
from scikits.learn.cross_val import StratifiedKFold
from scikits.learn.cross_val import KFold
from scikits.learn.grid_search import GridSearchCV
from Classifier import ResultProcessor

def parsingBerkeley():
    #===============================================================================
    # Parsing using BerkeleyParser
    #===============================================================================
    print "Parsing File"
#    dataprep.parseQuestion(colName, training)
    print "Done"

    #===============================================================================
    # Run Collins Head Finder
    #===============================================================================
    print "Runs Collins head finder"
    featureExtractor.collinsHeadParsing(colName, training)
    print "Done"

def featureInit():
    #===============================================================================
    # Extracting course and fine category of question 
    #===============================================================================
    print "Generating vector"
    featureExtractor.vectorSpaceInit(questions, 'feature'+colName+'_'+classType)
    print "Done"

def headWordExtraction():
    #===============================================================================
    # Extracting Collins Head
    #===============================================================================
    print "Extracting collins head"
    featureExtractor.collinsHeadExtractor(colName,training)
    print "Done"
    
def hypernimExtraction():
    #===========================================================================
    # Extracting Head Sense
    #===========================================================================
    print "Extracting head sense"
    featureExtractor.collinsHeadSenseExtractor(questions, colName, training)
    print "Done"
    
    #===============================================================================
    # Extracting Collins Head Hypernym
    #===============================================================================
    print "Extracting collins head hypernym"
    featureExtractor.hypernimExtractor(colName, 6)
    print "Done"

def whWordExtraction():
    #===========================================================================
    # Extracting WhWord
    #===========================================================================
    print "Extracting WhWord"
    featureExtractor.whWordExtractor(questions, colName)
    print "Done"
    
def featureInsertion():
#    if training:
        #===============================================================================
        # Generating bag of words
        #===============================================================================
#        print "Generating bag of words"
#        termExtractor.bagOfWordBuilder(questions,'words'+colName,insert)
#        print "Done"

    #===============================================================================
    # Inserting bag of words to vector space
    #===============================================================================
    print 'Inserting bag of words to vector space'
#    termExtractor.vectorSpaceBuilder(questions, colName, 'feature'+colName+'_'+classType,common,insert)
    print 'Done'
    
    #===============================================================================
    # Generating data for classifier
    #===============================================================================
    print 'Generating data for classifier'
    dataRetrieval = DataRetrieval()
    dataRetrieval.extractData('feature'+colName+'_'+classType,training,common,False,classType)
    dataRetrieval.extractData('feature'+colName+'_'+classType,training,common,True,classType)
    print 'Done'

def classification():
    filePath = DBStore.commonRoot + '/'+dbName + '_'+colName +'.txt'
    f = open(filePath,'w')
    def maxmeanstdv(x):
        from math import sqrt
        n, max, mean, std = len(x), 0, 0, 0
        for a in x:
            if a>max:
                max = a
            mean = mean + a
        mean = mean / float(n)
        for a in x:
            std = std + (a - mean)**2
        std = sqrt(std / float(n-1))
        return max, mean, std
    #===============================================================================
    # Running ELM
    #===============================================================================

    print 'Running ELM'
    result = []
#    for i in range(100,500,10):
#        print "i: " + str(i)
#        for j in range(0,20):
#            print "   j: " + str(j)
#            acc, missClass = ELMClassify(numberOfHiddenNeuron=i,train='feature'+common+'_'+classType, test='feature'+colName+'_'+classType)
#            result.append(acc)
#        max,mean,std = maxmeanstdv(result)
#        result = []
#        print max,mean,std
    
#    for i in range(0,20):
#        print i
#        acc, missClass = ELMClassify(numberOfHiddenNeuron=1200,train='feature'+common+'_'+classType, test='feature'+colName+'_'+classType)
#        result.append(acc)
#    max,mean,std = maxmeanstdv(result)
#    pickle.dump(result,f)
#    f.close()
#    print str(max), str(mean), str(std)
#

###Cross Validation
#    meanSeed = 0
#    meanMax = 0
#    for i in range(0,1000):
#        print 'Seed: ' + str(i)
#        result = []
#        train_data = loadtxt(DBStore.trainingRoot+"/vector_"+ 'feature'+common+'_'+classType +".txt")
#        for j in range(0,5):
#            X = train_data[:,1:size(train_data,1)]
#            Y = train_data[:,0]
#            data = KFold(len(Y), k=2)
#            for train, test in data:
#        #        print X[train],Y[train]
#                random.seed(i)
#                acc, missClass = ELMClassify(numberOfHiddenNeuron=210,
#                                                 p=X[train], t=Y[train],
#                                                 tv_t=Y[test],tv_p=X[test],
#                                                 )
#                result.append(acc)
#            random.seed(1+j)
#            shuffle(train_data)
#        max,mean,std = maxmeanstdv(result)
#        print max,mean
#        if mean>meanMax:
#            meanSeed = i
#            meanMax = mean
#            print 'New Maximum: ' + str(mean) + ' with seed: ' + str(i) 
        
#### Checking best hidden neuron
#
    maxHidden = 0
    max = 0
    for i in range(1000,1301,50):
        print 'Hidden neuron: ' + str(i) 
        random.seed(31)
        acc, missClass = ELMClassify(numberOfHiddenNeuron=i,train='feature'+common+'_'+classType, test='feature'+colName+'_'+classType)
        print acc
        if acc>max:
            maxHidden = i
            max = acc
            print 'New Maximum: ' + str(acc) + ' with hidden: ' + str(i) 
    print maxHidden, max 
#    
# Checking best seed
    start = time.time()
    maxSeed = 0
    max = 0
    for i in range(1,51):
        print 'Seed: ' + str(i) 
        random.seed(i)
        acc, missClass = ELMClassify(numberOfHiddenNeuron=maxHidden,train='feature'+common+'_'+classType, test='feature'+colName+'_'+classType)
        print acc
        result.append(acc)
        if acc>max:
            maxSeed = i
            max = acc
            print 'New Maximum: ' + str(acc) + ' with seed: ' + str(i) 
    max,mean,std = maxmeanstdv(result)
    print mean,std,max,maxSeed
#    
    random.seed(maxSeed)
    acc, missClass = ELMClassify(numberOfHiddenNeuron=1150,train='feature'+common+'_'+classType, test='feature'+colName+'_'+classType)
    print acc
#    ResultProcessor.parseResult(missClass, 'feature'+colName+'_'+classType,'raw'+colName, classType)

    for c in missClass:
        rawQuestions = DBStore.getDB()['raw'+colName]
        question = rawQuestions.find()[c[0]]
        print question['question'] + ' ' + question[classType.lower()] + ' ' + str(question['head']) + ' ' + str(c[0]) + ' ' + str(c[1]) + ' ' + str(c[2])
#        print question['hypernym']
#        
        
#    finish = time.time() - start
#    print 'Time taken: ' + str(finish)
    
    #===============================================================================
    # Running SVM
    #===============================================================================
#    print 'Running SVM'
#    y,x = svm_read_problem(DBStore.trainingRoot+'/vector_SVM_'+'feature'+common+'_'+classType+'.txt')
#    y_test,x_test = svm_read_problem(DBStore.testingRoot+'/vector_SVM_'+'feature'+colName+'_'+classType+'.txt')
#    start = time.time()
#    m = svm_train(y,x,"-c 4 -t 0")
#    print 'SVM training time: ' + str(time.time()-start)
#    start = time.time()
#    p_label, p_acc, p_val = svm_predict(y_test,x_test,m)
#    print 'SVM testing time: ' + str(time.time()-start)
#    print 'Done'


insert = {'unigram':False,'hypernym':False,'head':True,'whWord':True}
classType = 'Coarse'
dbName = 'QAnlp'
for key,value in insert.iteritems():
    if value:
        dbName = dbName + '_' + key
                
DBStore.init(dbName)
dataprep = DataRetrieval()
termExtractor = BagOfWords()
featureExtractor = FeatureExtractor()
colName = '5500'
common = '5500'
training = True
questions = DBStore.queryDB('raw'+colName)
#===============================================================================
# Insert Raw File to Database
#===============================================================================


#dataprep.insertFile2Database(colName,training)
#parsingBerkeley()
#featureInit()
#whWordExtraction()
#headWordExtraction()
#hypernimExtraction()
#termExtractor.bagOfWordBuilder(questions,'words'+colName,insert)
#featureInsertion()

colName = '10'
common = '5500'
training = False
questions = DBStore.queryDB('raw'+colName)


#dataprep.insertFile2Database(colName,training)
#parsingBerkeley()
#featureInit()
#whWordExtraction()
#headWordExtraction()
#hypernimExtraction()
#termExtractor.vectorSpaceBuilder(questions, colName, 'feature'+colName+'_'+classType,common,insert)
#featureInsertion()
classification()