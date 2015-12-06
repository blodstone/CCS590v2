'''
Created on Mar 10, 2011

@author: Blodstone
'''

from scikits.learn.cross_val import StratifiedKFold
from scikits.learn.cross_val import KFold
from scikits.learn.grid_search import GridSearchCV
from numpy import *
from Classifier import ELM
from IOPreprocessing.DBStore import DBStore
from numpy.random import shuffle

#train_data = array([[0,-1,-1,1,1,-1,-1,-1,1,-1,-1,-1],
#                    [1,1,-1,-1,-1,1,-1,-1,-1,1,-1,-1],
#                    [2,-1,1,-1,-1,-1,1,-1,-1,-1,1,-1],
#                    [3,1,-1,-1,-1,-1,-1,1,-1,-1,-1,1]])
train = '5500'
test = '10'

bestAcc = 0
inputNeuron = None
biasOfHiddenNeuron = None
i = 1
totalAcc = []
def rata2(acc):
    sum = 0
    for n in acc:
        sum = sum + n
    return sum/len(acc)
    
train_data = loadtxt(DBStore.trainingRoot+"/vector_"+ train +".txt")
test_data = loadtxt(DBStore.testingRoot+"/vector_"+ test+".txt")
for i in range(500,1001,100):
    p = train_data[:,1:size(train_data,1)].T
    inputWeight = random.random((i,p.shape[0]))*2-1
    biasOfHiddenNeuron = random.random((i,1))
    print 'i: ' + str(i)
    for j in range(0,5):
        X = train_data[:,1:size(train_data,1)]
        Y = train_data[:,0]
        data = KFold(len(Y), k=2)
        for train, test in data:
    #        print X[train],Y[train]
            acc, missClass = ELM.ELMClassify(numberOfHiddenNeuron=i,
                                             p=X[train], t=Y[train],
                                             tv_t=Y[test],tv_p=X[test],
                                             inputWeight=inputWeight,
                                             biasOfHiddenNeuron=biasOfHiddenNeuron)
            totalAcc.append(acc)
        shuffle(train_data)
    print str(totalAcc)
    print "average: " + str(rata2(totalAcc))
    totalAcc = []
    print 'No Hidden Neuron: ' + str(i)
    