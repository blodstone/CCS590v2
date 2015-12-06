'''
Created on Feb 3, 2011

@author: Blodstone
'''
import re
import time
import pymongo
from IOPreprocessing.DBStore import DBStore
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from Feature.POS import POSTagger

class BagOfWords:
    
    def bagOfWords(self,words, stopfile='english'):
        badwords = stopwords.words(stopfile)
        cleanwords = set(words) - set(badwords)
        #return dict([(cleanwords, True) for word in words])
        return cleanwords
    
    def bagOfWordBuilder(self,questions,colName,insert):
        finalWords = []
        i = 0
        start = time.time()
        questions.rewind()
        p = re.compile('^[A-Za-z].*[A-Za-z]$')
        for question in questions:
            if insert['unigram']:
                lemma = [word for word in question['lemma'] if p.match(word)]
                finalWords.extend(lemma)
            if insert['hypernym']:
                for word in question['hypernym']:
                    finalWords.append(word)
            if insert['head']:
                for word in question['head']:
                    if word is not None:
                        finalWords.append(word)
            if insert['whWord']:
                finalWords.append(question['whWord'])
            print i
            i = i+1
        total = time.time()-start
        print 'Done '+ str(total)
        finalWords = sorted(self.bagOfWords(finalWords))
        outputFile = DBStore.commonRoot +'/' + colName+'.txt'
        output = open(outputFile,'w')
        print 'Total words: ' + str(len(finalWords))
        print 'Writing file'
        for word in finalWords:
            output.write(word+"\n")
        output.close()
        print 'Done'
        
    def vectorSpaceBuilder(self,questions,colName,featureName, common,insert):
        inputFile = DBStore.commonRoot+ '/words' +common+'.txt'
        input = open(inputFile,'r') 
        featureDB = DBStore.getDB()[featureName]
        raw = DBStore.getDB()['raw'+colName]
        words = dict([(word.rstrip(),-1) for word in input])
        i =0
        questions.rewind()
        print words
        print "Start building vector"
        start = time.time()
        for question in questions:
            print i
            r = raw.find_one({'qID':question['qID']})
            i=i+1
            bagOfWords = words.copy()
            if insert['head']:
                for word in r['head']:
                    if word is not None:
                        try:
                            bagOfWords[word]
                            bagOfWords[word]=1
                        except KeyError:
                            pass
            if insert['whWord']:
                try:
                    bagOfWords[question['whWord']]
                    bagOfWords[question['whWord']]=1
                except KeyError:
                    pass
            if insert['hypernym']:
                for word in r['hypernym']:
                    try:
                        bagOfWords[word]
                        bagOfWords[word]=1
                    except KeyError:
                        pass
            if insert['unigram']:
                tokenizeWords = question['lemma']
                for word in tokenizeWords:
                    try:
                        if word.lower() not in ['who','what','how','where',
                                            'when','why','who','which',
                                            'whom','whose']:
                            bagOfWords[word]
                            bagOfWords[word]=1
                    except KeyError:
                        pass
            featureDB.update({'qID':question['qID']},{"$set":bagOfWords},safe=False,multi=True)
        total = time.time() - start
        print "Finish building " + str(total)
