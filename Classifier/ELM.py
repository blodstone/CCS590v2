'''
Created on Dec 29, 2010

@author: Blodstone
'''
from __future__ import division
from numpy import *
from IOPreprocessing.DBStore import DBStore
from numpy.ma.core import sin
import time
import pickle

def trainELM(numberOfHiddenNeuron,train=None):
    if type(train)==type(''):
        train_data = loadtxt(DBStore.trainingRoot+"/vector_"+ train +".txt")
    else:
        train_data = train
    t = train_data[:,0].T
    p = train_data[:,1:size(train_data,1)].T
    numberOfTrainingData = p.shape[1]
    numberOfInputNeuron = p.shape[0]
    start = time.time()
    inputWeight = random.random((numberOfHiddenNeuron,numberOfInputNeuron))*2-1
    biasOfHiddenNeuron = random.random((numberOfHiddenNeuron,1))
    
    tempH = dot(inputWeight,p)
    ind = zeros(numberOfTrainingData,dtype=int32)
    biasMatrix = biasOfHiddenNeuron[:,ind]
    tempH = tempH + biasMatrix
    
    H = tempH
#    H = 1 / (1 + exp(-1*tempH))
#    H = sin(tempH)
    
    outputWeight = dot(linalg.pinv(H.T),t.T)
    print 'Training time: ' + str(time.time()-start)
    y = dot(H.T, outputWeight).T
    missClassificationRateTraining = 0
    
    for i in range(0,t.shape[1]):
        labelIndexExpected = argmax(t[:,i])
        labelIndexActual = argmax(y[:,i])
        if labelIndexExpected!=labelIndexActual:
            missClassificationRateTraining = missClassificationRateTraining+1
    trainingAccuracy = 1-missClassificationRateTraining/size(t)
    
    return outputWeight,trainingAccuracy

def predictELM(numberOfHiddenNeuron,outputWeight,test=None):
    if type(test)==type(''):
        test_data = loadtxt(DBStore.testingRoot+"/vector_"+ test+".txt")
    else:
        test_data = test
    tv_t = test_data[:,0].T
    tv_p = test_data[:,1:size(test_data,1)].T
    numberOfInputNeuron = tv_p.shape[0]
    numberOfTestingData = tv_p.shape[1]
    inputWeight = random.random((numberOfHiddenNeuron,numberOfInputNeuron))*2-1
    biasOfHiddenNeuron = random.random((numberOfHiddenNeuron,1))
    tempH_test = dot(inputWeight,tv_p)
    ind = zeros(numberOfTestingData,dtype=int32)
    biasMatrix = biasOfHiddenNeuron[:,ind]
    tempH_test = tempH_test + biasMatrix
    tempH_test = tempH_test + biasMatrix
    H_test = tempH_test
    t_y = dot(H_test.T, outputWeight).T
    
    missClassificationRateTesting = 0
    
    for i in range(0,tv_t.shape[1]):
        labelIndexExpected = argmax(tv_t[:,i])
        labelIndexActual = argmax(t_y[:,i])
        if labelIndexExpected!=labelIndexActual:
            missClassificationRateTesting = missClassificationRateTesting+1
    testingAccuracy = 1-missClassificationRateTesting/tv_t.shape[1]
    return testingAccuracy
        
def ELMClassify(numberOfHiddenNeuron=None,p=None,t=None,
                tv_p=None,tv_t=None,
                train=None,test=None,
                inputWeight=None,biasOfHiddenNeuron=None):
    
    if numberOfHiddenNeuron is None:
        numberOfHiddenNeuron=inputWeight.shape[0]
    if train is None:
        pass
    elif type(train)==type(''):
        train_data = loadtxt(DBStore.trainingRoot+"/vector_"+ train +".txt")
    else:
        train_data = train
#    train_data = loadtxt('E:/Kuliah/Postgraduate/Assignment/CCS590/95098948ELM/diabetes_train')
    #===============================================================================
#    train_data = array([[5,-1,-1,1,1,-1,-1,-1,1,-1,-1,-1],
#                        [3,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1],
#                        [29,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1],
#                        [4,1,-1,-1,-1,-1,-1,1,-1,-1,-1,1]])
    #===============================================================================
    if t is None or p is None:
        t = train_data[:,0].T
        p = train_data[:,1:size(train_data,1)].T
    else:
        t = t.T
        p = p.T
        
    if test is None:
        pass
    elif type(test)==type(''):
        test_data = loadtxt(DBStore.testingRoot+"/vector_"+ test+".txt")
    else:
        test_data = test
#    test_data = loadtxt('E:/Kuliah/Postgraduate/Assignment/CCS590/95098948ELM/diabetes_test')
    #===============================================================================
#    test_data = array([[5,-1,-1,1,1,1,-1,-1,1,-1,-1,-1]])
    #===============================================================================
    if tv_t is None or tv_p is None:
        tv_t = test_data[:,0].T
        tv_p = test_data[:,1:size(test_data,1)].T
        del train_data
        del test_data
    else:
        tv_t = tv_t.T
        tv_p = tv_p.T
    
    numberOfTrainingData = p.shape[1]
    numberOfTestingData = tv_p.shape[1]
    numberOfInputNeuron = p.shape[0]
    
    sortedTarget = sort(concatenate((t,tv_t),1),axis=0)
    label = zeros(1,dtype=int32)
    label[0] = sortedTarget[0]
    j = 0
    for i in range(0,numberOfTrainingData+numberOfTestingData):
        if sortedTarget[i]!=label[j]:
            j = j + 1
            label = append(label,sortedTarget[i])
            
    numberClass = j+1
    numberOfOutputNeuron = numberClass
    
    tempT = zeros((numberOfOutputNeuron,numberOfTrainingData),dtype=int32)
    for i in range(0,numberOfTrainingData):
        for j in range(0,numberClass):
            if label[j] == t[i]:
                break
        tempT[j,i]=1
    t = tempT*2-1
    
    tempTV_T = zeros((numberOfOutputNeuron,numberOfTestingData),dtype=int32)
    for i in range(0,numberOfTestingData):
        for j in range(0,numberClass):
            if label[j] == tv_t[i]:
                break
        tempTV_T[j,i]=1
    tv_t = tempTV_T*2-1
    
    del label
    del tempTV_T
    del tempT
    
    start = time.time()
    if inputWeight is None or biasOfHiddenNeuron is None:
        inputWeight = random.random((numberOfHiddenNeuron,numberOfInputNeuron))*2-1
        biasOfHiddenNeuron = random.random((numberOfHiddenNeuron,1))
    
    tempH = dot(inputWeight,p)
    ind = zeros(numberOfTrainingData,dtype=int32)
    biasMatrix = biasOfHiddenNeuron[:,ind]
    tempH = tempH + biasMatrix
    
    H = tempH
#    H = 1 / (1 + exp(-1*tempH))
#    H = sin(tempH)

    outputWeight = dot(linalg.pinv(H.T),t.T)
    
    print 'Training time: ' + str(time.time()-start)
    
    y = dot(H.T, outputWeight).T
    
    start = time.time()
    
    tempH_test = dot(inputWeight,tv_p)
    ind = zeros(numberOfTestingData,dtype=int32)
    biasMatrix = biasOfHiddenNeuron[:,ind]
    tempH_test = tempH_test + biasMatrix
    
#    H_test = 1 / (1 + exp(-1*tempH_test))
    H_test = tempH_test
    
    del tempH_test
    t_y = dot(H_test.T, outputWeight).T
    
    print 'Testing time: '+ str(time.time()-start)
    
    missClassificationRateTraining = 0
    missClassificationRateTesting = 0
    
    for i in range(0,t.shape[1]):
        labelIndexExpected = argmax(t[:,i])
        labelIndexActual = argmax(y[:,i])
        if labelIndexExpected!=labelIndexActual:
            missClassificationRateTraining = missClassificationRateTraining+1
    trainingAccuracy = 1-missClassificationRateTraining/size(t)
    
    missClass = []
    
    for i in range(0,tv_t.shape[1]):
        labelIndexExpected = argmax(tv_t[:,i])
        labelIndexActual = argmax(t_y[:,i])
        if labelIndexExpected!=labelIndexActual:
            missClassificationRateTesting = missClassificationRateTesting+1
            missClass.append([i,labelIndexExpected,labelIndexActual])
    testingAccuracy = 1-missClassificationRateTesting/tv_t.shape[1]
    
    
#    print 'Testing Accuracy ' + str(testingAccuracy*100)
#    
#    print 'Training Accuracy ' + str(trainingAccuracy*100)
    return testingAccuracy*100.0, missClass

if __name__ == "__main__":
    ELMClassify()
