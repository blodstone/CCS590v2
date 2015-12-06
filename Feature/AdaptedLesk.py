'''
Created on Feb 27, 2011

@author: Blodstone
'''

from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
import string
import time
from operator import itemgetter
from IOPreprocessing.DataPreparation import DataRetrieval

class AdaptedLesk:
    
    def __init__(self,k):
        self.k = k
        self.pair = {}
        self.bestPair = {}
        self.english_stops = stopwords.words('english')
        
    def wsd(self,sent,target, tag=None):
        if tag is None:
            self.scoring(sent, target)
        else:
            self.scoring(sent, target,tag)
        sense = self.getGreedyBestSenses(10)
        print wordnet.synset(sense).definition
        return sense
    
    
    #definitely false but for testing sake
    def getGreedyBestSenses(self,ranking):
        
        def getBest(pairs,index,context):
            max = -1
            sortedPair = sorted(pairs.items(),key=itemgetter(1))
            sortedPair.reverse()
            if index<len(sortedPair)-1:
                if(sortedPair[index][1]==sortedPair[index+1][1]):
                    allSynsets = wordnet.synsets(context)
                    sense1 = wordnet.synset(sortedPair[index][0].split(" ")[0])
                    sense2 = wordnet.synset(sortedPair[index+1][0].split(" ")[0])
                    indexFirst = allSynsets.index(sense1)
                    indexSecond = allSynsets.index(sense2)
                    if indexFirst>indexSecond:
                        sortedPair[index] = sortedPair[index+1]
            pair = {sortedPair[index][0]:sortedPair[index][1]}
            return pair
        
        def extractPair(sense,allPair,context):
            max = -1
            optimumPairs={}
            
            for key,value in allPair.iteritems():
                tempSense = key.split(' ')[0]
                if tempSense == sense:
                    optimumPairs[key] = value
            
            return getBest(optimumPairs,0,context)
        
        self.maxSenses = {}
        if len(self.context)==1:
            selectPair = self.pair[self.context[0]+self.context[0]]
            
            return selectPair.keys()[0].split(" ")[0]
        maxValue = -1
        allPair = self.pair[self.context[0]+self.context[1]]
        if len(self.pair) == 1: 
            ranking = 1
        else:
            if len(allPair)<ranking:
                ranking = len(allPair)
        for rank in range(0,ranking):
            value = 0
            senses = {}
            for i in range(0,len(self.context)-1):
                if i>0:
                    allPair = self.pair[self.context[i]+self.context[i+1]]
                    sense = selectPair.keys()[0].split(' ')
                    selectPair = extractPair(sense[1],allPair,self.context[i]) 
                    value = value + selectPair.values()[0]
                    keyPair = selectPair.keys()[0].split(" ")
                    senses.update({self.context[i+1]:keyPair[1]})
                else:
                    allPair = self.pair[self.context[i]+self.context[i+1]]
                    selectPair =  getBest(allPair,rank,self.context[i])
                    value = value + selectPair.values()[0]
                    keyPair = selectPair.keys()[0].split(" ")
                    senses.update({self.context[i]:keyPair[0],self.context[i+1]:keyPair[1]})
            if value>maxValue:
                maxValue = value
                self.maxSenses = senses
        return self.maxSenses[self.target]
    
    def scoring(self, words, target,tag=None):
        
        def replaceTag(tag):
            pos = DataRetrieval.replace(tag)
            if pos=='a':
                pos = 'n'
            return pos
        
        self.target = target
        words = [word for word in words if len(wordnet.synsets(word)) != 0 and (word not in ['as','an','a'] or word==target)]
        targetIndex = words.index(target)
        leftNoWords= targetIndex if targetIndex < self.k/2 else self.k/2
        leftWords = [words[i] for i in range(targetIndex-leftNoWords,targetIndex)]
        rightNoWords = len(words)-targetIndex-1  if len(words)-targetIndex-1 < self.k/2 else self.k/2
        rightWords = [words[i] for i in range(targetIndex+1,rightNoWords+targetIndex+1)]
        leftWords.extend([target])
        leftWords.extend(rightWords)
        self.context = leftWords
        if tag is None:
            if len(self.context)==1:
                self.score(self.context[0],self.context[0])
            for i in range(0,len(self.context)-1):
                self.score(self.context[i], self.context[i+1])
        else:
            if len(self.context)==1:
                self.score(self.context[0],self.context[0],replaceTag(tag[self.context[0]]),replaceTag(tag[self.context[0]]))
            for i in range(0,len(self.context)-1):
                self.score(self.context[i], self.context[i+1],replaceTag(tag[self.context[i]]),replaceTag(tag[self.context[i+1]]))
            
            
    def score(self,word1,word2,tag1=None,tag2=None):
#        if word1==word2:
#            if tag1 == None:
#                synCol1 = wordnet.synsets(word1)
#            else:
#                synCol1 = wordnet.synsets(word1,tag1)
#            self.pair.update({word1+word2:{synCol1[0].name+" "+synCol1[0].name:100}})
#            return 
        wordComb = word1+word2
        if tag1 == None: synCol1 = wordnet.synsets(word1)
        else: synCol1 = wordnet.synsets(word1,tag1)
        if tag2 == None: synCol2 = wordnet.synsets(word2)
        else: synCol2 = wordnet.synsets(word2,tag2)
#        optimumScore = -1
        if len(synCol1)==0:
            print word1 + " " + tag1
            synCol1 = wordnet.synsets(word1)
        if len(synCol2)==0:
            print word2 + " " + tag2
            synCol2 = wordnet.synsets(word2)
        synPair = {}
        for i in range(0,len(synCol1)):
            for j in range(0,len(synCol2)):
                syn1 = synCol1[i]
                syn2 = synCol2[j]
                synName = syn1.name + " " + syn2.name
                synHyper1 = string.join([hypernim.definition for hypernim in syn1.hypernyms()])
                synHyper2 = string.join([hypernim.definition for hypernim in syn2.hypernyms()])
                synInsHyper1 = string.join([hypernim.definition for hypernim in syn1.instance_hypernyms()])
                synInsHyper2 = string.join([hypernim.definition for hypernim in syn2.instance_hypernyms()])
                synExample1 = string.join([example for example in syn1.examples])
                synExample2 = string.join([example for example in syn2.examples])
                
                score = self.oSL(syn1.definition,syn2.definition) + self.oSL(synHyper1, synHyper2) \
                + self.oSL(syn1.definition, synHyper2) \
                +self.oSL(synHyper1, syn2.definition) \
                +self.oSL(synExample1, syn2.definition) \
                +self.oSL(synExample2, syn1.definition) +  self.oSL(synExample1, synExample2) \
                + self.oSL(synInsHyper1, syn2.definition) \
                +self.oSL(synInsHyper2, syn1.definition) +  self.oSL(synInsHyper1, synInsHyper2) \
                +self.oSL(synInsHyper2, synExample1) +  self.oSL(synInsHyper1, synExample2) 
                synPair.update({synName:score})
#                if score>optimumScore: 
#                    optimumScore = score
#                    self.bestPair.update({wordComb:{synName:score}})
        self.pair.update({wordComb:synPair})
        
    def oSL(self, sent1, sent2):
        sent1Token = word_tokenize(sent1)
        sent2Token = word_tokenize(sent2)
        final1Token = [word for word in sent1Token if word not in string.punctuation]
        final2Token = [word for word in sent2Token if word not in string.punctuation]
        len1 = len(final1Token)
        len2 = len(final2Token)
        i = 0
        j = 0
        commonToken = []
        seq = []
        start = False
        while i<len1:
            j = 0
            key = i
            seq = []
            while j<len2:
                if(i<len1 and j<len2) and (final1Token[i]==final2Token[j]) :
                    start = True
                    seq.append(final1Token[i])
                    i = i + 1
                    j = j + 1
                else:
                    if start:
                        #if len(commonToken)<len(seq):
                        commonToken.extend(seq)
                        seq = []
                        start = False
                    i = key
                    j = j + 1
            #if len(commonToken)<len(seq):
            commonToken.extend(seq)
            seq = []
            i = i + 1
        length = 0
        for word in commonToken:
            length = length + len(word)**2
        return length
    
if __name__ == "__main__":
    lesk = AdaptedLesk(6)
    start = time.time()
    tokenized =  [ "What", "is", "the", "scientific", "name", "for", "elephant" ]
    target= 'elephant'
    tagged =  { "What" : "WP", "name" : "NN", "for" : "IN", "is" : "VBZ", "elephant" : "NN", "the" : "DT", "scientific" : "JJ" }
    a = wordnet.synset(lesk.wsd(tokenized,target,tagged))
    print a.definition, str(a)
    finish = time.time()- start 
    print str(finish)
    #print str(lesk.oSL("the youngest member of a group (not necessarily young)", "(physics) a manifestation of energy; the transfer of energy from one physical system to another expressed as the product of a force and the distance through which it moves a body in the direction of that force"))