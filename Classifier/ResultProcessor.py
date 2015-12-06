'''
Created on Apr 1, 2011

@author: Blodstone
'''
from __future__ import division
from IOPreprocessing.DBStore import DBStore


def parseResult(missClass,colName,rawName,classType):
    questions = DBStore.getDB()[colName].find()
    raw = DBStore.getDB()[rawName]
    mc = {}
    for c in missClass:
        mc[c[0]] = [c[1],c[2]]
    i = 0
    whTotal = {'whWord-who':0,'whWord-what':0,'whWord-how':0,'whWord-where':0,'whWord-rest':0,
               'whWord-when':0,'whWord-why':0,'whWord-which':0,'whWord-whom':0,'whWord-whose':0}
    whCorrect = {'whWord-who':0,'whWord-what':0,'whWord-how':0,'whWord-where':0,'whWord-rest':0,
               'whWord-when':0,'whWord-why':0,'whWord-which':0,'whWord-whom':0,'whWord-whose':0}
    if classType =='Fine':
        label = 'FineCode'
        index = ["ABBR:abb", "ABBR:exp",
             "DESC:def", "DESC:desc",
             "DESC:manner","DESC:reason",
             "ENTY:animal","ENTY:body", 
             "ENTY:color", "ENTY:cremat",
             "ENTY:currency", "ENTY:dismed",
             "ENTY:event", "ENTY:food",
             "ENTY:instru","ENTY:lang",
             "ENTY:letter", "ENTY:other",
             "ENTY:plant","ENTY:product",
             "ENTY:religion", "ENTY:sport",
             "ENTY:substance", "ENTY:symbol", 
             "ENTY:techmeth", "ENTY:veh",
             "ENTY:word", "ENTY:termeq",
             "HUM:ind", "HUM:title",
             "HUM:desc","HUM:gr",
             "LOC:country", "LOC:mount",
             "LOC:other", "LOC:state",
             "LOC:city", 
             "NUM:code", "NUM:count", 
             "NUM:date", "NUM:dist",
             "NUM:money", "NUM:ord",
             "NUM:other", "NUM:period",
             "NUM:perc", "NUM:speed",
             "NUM:temp", "NUM:volsize",
             "NUM:weight"]
    else:
        label = 'CoarseCode'
        index = ["ABBR","DESC", "ENTY", "HUM", "LOC",
                           "NUM"]
    confusionMat = [[0.0 for col in range(len(index))]for row in range(len(index))]
    resultMat = [[0.0 for col in range(3)]for row in range(len(index))]
    i = 0
    for question in questions:
        whWord = raw.find({'qID':question['qID']})[0]['whWord']
        whTotal[whWord] = whTotal[whWord] + 1 
        if i not in mc.keys():
            whCorrect[whWord] = whCorrect[whWord] + 1 
            predicted = actual = question[label]
            confusionMat[actual][predicted] = \
            confusionMat[actual][predicted] + 1 
        else:
            if question[label]!=mc[i][0]:
                print 'Error'
                break
            else:
                predicted = mc[i][1]
                actual = mc[i][0]
                confusionMat[actual][predicted] = \
                confusionMat[actual][predicted] + 1 
        i = i +1
    print confusionMat
    for i in range(len(index)):
        truePos = confusionMat[i][i]
        falsePos = 0.0
        for j in range(len(confusionMat)):
            if j == i: continue
            falsePos = falsePos + confusionMat[j][i] 
        trueNeg = 0.0
        for j in range(len(confusionMat)):
            for k in range(len(confusionMat)):
                if j == i or k == i: continue
                trueNeg = trueNeg + confusionMat[j][k]
        falseNeg = 0.0
        for j in range(len(confusionMat)):
            if j == i: continue
            falseNeg = falseNeg + confusionMat[i][j]
        print i,truePos,falseNeg,falsePos,trueNeg
        
        if truePos+falsePos == 0.0:
            precision = 0.0
        else:    
            precision = truePos/(truePos+falsePos)
        if trueNeg+falsePos == 0.0:
            specificity = 0.0
        else:
            specificity = trueNeg/(trueNeg+falsePos)
        if truePos+falseNeg == 0.0:
            sensitivity = 0.0
        else:
            sensitivity = truePos/(truePos+falseNeg)
        resultMat[i] = [i,(truePos+falseNeg),precision,sensitivity,specificity]
    file1 = DBStore.commonRoot+"\\result1_"+colName+".csv"
    file2 = DBStore.commonRoot+"\\result2_"+colName+".csv"
    f = open(file1,'w')
    f.write('Class,#,Precision,Sensitivity,Specificity\n')
    for result in resultMat:
        f.write(index[result[0]]+','+str(result[1])+','+str(result[2]) + ',' + str(result[3]) + ',' + str(result[4])+'\n')
    f.close
    f = open(file2,'w')
    f.write('Wh-Word,Accuracy,Total Question,Correctly Predicted\n')
    for k,v in whTotal.iteritems():
        if v == 0: continue
        percent = whCorrect[k]/v*100
        f.write(k+','+str(percent)+','+str(v)+','+str(whCorrect[k])+'\n')
    f.close