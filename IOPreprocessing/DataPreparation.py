'''
Created on Feb 8, 2011

@author: Blodstone
'''
import pymongo
import time
import re
import string
import os
from IOPreprocessing.DBStore import DBStore
from Feature.POS import POSTagger
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from subprocess import Popen
from subprocess import call
import shlex


class DataRetrieval:
    
    @classmethod
    def replace(cls,str):
        if str == None:
            return "n"
        elif str[0]=='J':
            return "a"
        elif str[0] in 'VBDHM':
            return "v"
        elif str[0] in 'RI':
            return "r"
        else: 
            return "n"
    
    def parseQuestion(self,colName,training):
        raw = DBStore.getDB()['raw'+colName].find()
        if training:
            final = DBStore.trainingRoot + '/parsed_'+colName+'.txt'
            outputFile = DBStore.trainingRoot +'/raw_'+colName+'.txt'
        else:
            final = DBStore.testingRoot + '/parsed_'+colName+'.txt'
            outputFile = DBStore.testingRoot +'/raw_'+colName+'.txt'
        f = open(outputFile,'w')
        for question in raw:
            f.write(question['question']+'\n')
        f.close
        startDir = os.getcwd()
        print 'Parsing'
#        command = "java  -Xms512m -Xmx512m -jar berkeleyParser.jar -gr eng_sm6.gr -inputFile "+outputFile+" -outputFile "+final
        command = "execute.bat " + outputFile + " " + final
#        os.system(command)
        args = shlex.split(command)
#        call(args)
        p = Popen(args,bufsize=-1,shell=True)
#        sts = os.waitpid(p.pid, 0)[1]
        #os.chdir(startDir)
    
    def extractData(self,name,training,common,svmFormat=False,classType='Coarse'):
        helperFile =  DBStore.commonRoot + '/words'+common+'.txt'
        if training:
            if not svmFormat:
                outputFile = DBStore.trainingRoot + '/vector_'+name+'.txt'
            else:
                outputFile = DBStore.trainingRoot + '/vector_SVM_'+name+'.txt'
        else:
            if not svmFormat:
                outputFile = DBStore.testingRoot + '/vector_'+name+'.txt'
            else:
                outputFile = DBStore.testingRoot + '/vector_SVM_'+name+'.txt'
                
        output = open(outputFile,'w')
        helper = open(helperFile,'r')
        helperWord = [word for word in helper]
        query = DBStore.queryDB(name)
        i = 0
        for question in query:
            print i
            i=i+1
            output.write(str(question[classType+'Code']) +" ")
            j = 1
            if svmFormat:
                for word in helperWord:
                    output.write(str(j)+":" +str(question[word.rstrip()]) + " ") 
                    j=j+1
            else:
                for word in helperWord:
                    output.write(str(question[word.rstrip()]) + " ") 
            helper.seek(0)
            output.write("\n")
        output.close()
    
    def insertFile2Database(self,colName='',training=True,parse=False):
#        posTagger = POSTagger()
#        posTagger.loadTagger()
#        tagger = posTagger.getTagger()
        lemmatizer = WordNetLemmatizer()
        DBStore.dropColl('raw'+colName)
        collection = DBStore.getDB()['raw'+colName]
        if training:
            readFileName = DBStore.trainingRoot + "\\raw_" + colName + ".txt"
        else:
            readFileName = DBStore.testingRoot + "\\raw_" + colName + ".txt"
        outputFileName = DBStore.commonRoot + "\\parsed_" + colName + ".txt"
        readFile = open(readFileName,'w')
        if colName=='':
            print 'Filename is needed'
        else:
            print 'Beginning insertion of ' +'raw' + colName
            start = time.time()
            if training:
                file = DBStore.trainingRoot+'/train_'+colName+'.label'
            else:
                file = DBStore.testingRoot+'/TREC_'+colName+'.label'
            input = open(file,'r')
            pattern = re.compile(r"(?P<coarse>\w+):(?P<fine>\w+) (?P<question>.+)");
            i = 0
            for line in input:
                print i
                i = i + 1
                match = pattern.match(line)
                tokenizeWords = word_tokenize(match.group('question'))
                print match.group('question')
                p = re.compile('\.') #pattern for eliminating .
                p2 = re.compile('(1|2)\d\d\d') #pattern for grouping year
                tokenizeWords = [p.sub('',word) for word in tokenizeWords if word not in string.punctuation]
                taggedWords = dict(pos_tag(tokenizeWords))
                lemmatizedQuestion = [lemmatizer.lemmatize(word,pos=self.replace(taggedWords[word])) for word in tokenizeWords]
#                print taggedWords
#                print match.group('question')
                pairQuestion = dict(zip(tokenizeWords,lemmatizedQuestion))
                readFile.write(match.group('question')+'\n')
                collection.insert({"qID":i,
                                   "question": match.group('question'),
                                   "coarse":match.group("coarse"),
                                   "fine":match.group("coarse")+":"+match.group("fine"),
                                   "lemma":lemmatizedQuestion,
                                   "tagged":taggedWords,
                                   "tokenized":tokenizeWords,
                                   "pair":pairQuestion
                                        })
            readFile.close()
            if parse:
                self.parseQuestion(readFileName, outputFileName)
            total = time.time()-start
            print 'End of insertion with total time '+ str(total)      
            
if __name__ == '__main__':
    dataprep = DataRetrieval()
    dataprep.parseQuestion()