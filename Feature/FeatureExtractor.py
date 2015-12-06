'''
Created on Feb 3, 2011

@author: Blodstone
'''
import pymongo
import re
from IOPreprocessing.DBStore import DBStore
from AdaptedLesk import AdaptedLesk
from nltk.corpus import wordnet
import os
import shlex
from subprocess import Popen
from IOPreprocessing.DataPreparation import DataRetrieval

class FeatureExtractor:
    coarseClassCode = {"ABBR" : 0,"DESC":1, "ENTY":2, "HUM":3, "LOC":4,
                           "NUM":5}
    fineClassCode = {"ABBR:abb" : 0,
             "ABBR:exp": 1,
             "DESC:def" : 2,
             "DESC:desc" : 3, 
             "DESC:manner" : 4,  
             "DESC:reason" : 5,
             "ENTY:animal" : 6, 
             "ENTY:body" : 7, 
             "ENTY:color" : 8, 
             "ENTY:cremat" : 9,
             "ENTY:currency" : 10, 
             "ENTY:dismed" : 11,
             "ENTY:event" : 12, 
             "ENTY:food" : 13, 
             "ENTY:instru" : 14,
             "ENTY:lang" : 15, 
             "ENTY:letter" : 16, 
             "ENTY:other" : 17,
             "ENTY:plant" : 18,
             "ENTY:product" : 19, 
             "ENTY:religion" : 20, 
             "ENTY:sport" : 21, 
             "ENTY:substance" : 22,  
             "ENTY:symbol" : 23, 
             "ENTY:techmeth" : 24, 
             "ENTY:veh" : 25,
             "ENTY:word" : 26, 
             "ENTY:termeq" : 27, 
             "HUM:ind" : 28, 
             "HUM:title" : 29, 
             "HUM:desc" : 30, 
             "HUM:gr" : 31, 
             "LOC:country" : 32, 
             "LOC:mount" : 33, 
             "LOC:other" : 34, 
             "LOC:state" : 35, 
             "LOC:city" : 36, 
             "NUM:code" : 37, 
             "NUM:count" : 38, 
             "NUM:date" : 39, 
             "NUM:dist" : 40, 
             "NUM:money" : 41, 
             "NUM:ord" : 42,
             "NUM:other" : 43, 
             "NUM:period" : 44, 
             "NUM:perc" : 45, 
             "NUM:speed" : 46, 
             "NUM:temp" : 47, 
             "NUM:volsize" : 48, 
             "NUM:weight" : 49  }
    
    def __init__(self):
        pass
    
    
    def whWordExtractor(self,questions,colName):
        rawQuestions = DBStore.getDB()['raw'+colName]
        p = re.compile('.*(?P<whword>who|what|how|where|when|why|which|whom|whose) .*', re.IGNORECASE)
        questions.rewind()
        for question in questions:
            match = p.match(question['question'])
            try:
                whWord = 'whWord-'+match.group('whword').lower()
            except AttributeError:
                whWord = 'whWord-rest'
            print question['question'] + whWord
            rawQuestions.update({'qID':question['qID']},{"$set":{"whWord":whWord}},safe=True,multi=True)
    
    def vectorSpaceInit(self,questions,colName):
        questions.rewind()
        DBStore.dropColl(colName)
        print 'Creating vector space'
        for question in questions:
            DBStore.getDB()[colName].insert({'qID':question['qID'],'question':question['question'],'CoarseCode':self.__class__.coarseClassCode[question['coarse']],'FineCode':self.__class__.fineClassCode[question['fine']]})
        print 'Done'
    
    def hypernimExtractor(self,colName,max):
        rawQuestions = DBStore.getDB()['raw'+colName]
        l = 0 
        for question in rawQuestions.find():
            print question['headSense']
            if question['headSense']=='null':
                selectedHypernyms = []
            else:
#                sense = wordnet.synset(question['headSense'])
#                instances = sense.instance_hypernyms()
#                hypernyms = sense.hypernym_paths()
#                if len(instances) != 0:
#                    j = 0
#                    for instance in instances:
#                        j = j + 1
#                        if j>1: break;
#                        insPath = instance.hypernym_paths()
#                        k = 0
#                        for ins in insPath:
#                            k = k + 1
#                            if k>1: break;
#                            if len(ins)>max+1:
#                                index = max+1
#                            else:
#                                index = len(ins)
#                            ins.reverse()
#                            selected = [ins[k].lemma_names[0] for k in range(1,index)]
#                        selectedHypernyms.extend(selected)
#                else:
#                    j = 0
#                    for hypernym in hypernyms:
#                        j = j + 1
#                        if j>1: break
#                        if len(hypernym)>max+1:
#                            index = max+1
#                        else:
#                            index = len(hypernym)
#                        hypernym.reverse()
#                        selected = [hypernym[k].lemma_names[0] for k in range(1,index)]
#                    selectedHypernyms.extend(selected)
                sense = wordnet.synset(question['headSense'])
                instance = sense.instance_hypernyms()
                hypernym = sense.hypernym_paths()[0]
                if len(instance) != 0:
                    hypernym = instance[0].hypernym_paths()[0]
                if len(hypernym)>max+1:
                    index = max+1
                else:
                    index = len(hypernym)
                hypernym.reverse()
                selectedHypernyms = [hypernym[k].lemma_names[0] for k in range(1,index)]
            print l
            l = l + 1
            print question['question']
            rawQuestions.update({'question':question['question']},{"$set":{"hypernym":selectedHypernyms}},safe=True,multi=True)
    
    def collinsHeadParsing(self,colName,training):
        if training:
            inputFile = DBStore.trainingRoot + '/parsed_'+colName+'.txt'
            questionFile = DBStore.trainingRoot + '/raw_'+colName+'.txt'
            outputFile = DBStore.trainingRoot + '/headword_question'+colName+'.txt'
        else:
            inputFile = DBStore.testingRoot + '/parsed_'+colName+'.txt'
            questionFile = DBStore.testingRoot+ '/raw_'+colName+'.txt'
            outputFile = DBStore.testingRoot + '/headword_question'+colName+'.txt'
        startDir = os.getcwd()
        print startDir
        print 'Parsing'
        command = "execute2.bat "+inputFile+" "+questionFile+" " +outputFile
        args = shlex.split(command)
        p = Popen(args,bufsize=-1,shell=True)
    
    def collinsHeadExtractor(self,colName,training):
        def whatPattern(question):
            p3 = re.compile("^[w|W]hat (is|are|was|were)( [A-Za-z]*)*( composed of| made of| made out of)( [A-Za-z]*)* \?$")
            if p3.match(question):
                return "ENTY:subs"
            p7 = re.compile("^[w|W]hat (is|are|was|were)( [A-Za-z]*)* used for \?$")
            if p7.match(question):
                return "DESC:reason_2"
            p1 = re.compile("^[w|W]hat (is|are|was|were|\'s)( a| an| the)*( \`\`)*( [A-Za-z]+[a-z\-]*[A-Za-z]+){1,2}( \'\')* \?$")
            if p1.match(question):
                return "DESC:def_1"
            p2 = re.compile("^[w|W]hat (do|does|did)( [A-Za-z]*)*( \`\`)*( [A-Za-z]*)*( \'\')*( means?)( [A-Za-z]*)* \?$")
            if p2.match(question):
                return "DESC:def_2"
            p4 = re.compile("^[w|W]hat (do|does|did) .* (do|does|did) \?$")
            if p4.match(question):
                return "DESC:desc"
            p5 = re.compile("^[w|W]hat do you (call|called) .*")
            p9 = re.compile("^[w|W]hat (is|\'s) the term .*")
            p10 = re.compile("^[w|W]hat (was|is|\'s) another name .*")
            if p5.match(question) or p9.match(question) or p10.match(question):
                return "ENTY:termeq"
            p6 = re.compile("^[w|W]hat (causes|cause|caused) .*")
            if p6.match(question):
                return "DESC:reason_1"
            p8 = re.compile("^[w|W]hat (do|does|did).* stand for \?$")
            if p8.match(question):
                return "ABBR:exp"
            p11 = re.compile('[w|W]hat (do|did|does) .* eat \?')
            if p11.match(question):
                return "ENTY:food"

        def whoPattern(question):
            p1 = re.compile("^[w|W]ho (is|are|was|were)( the)*( \`\`)*( [A-Z][a-z]+)+( \'\')* \?$")
            if p1.match(question):
                return "HUM:desc"
            p2 = re.compile("^[w|W]ho (is|was) .*")
            if p2.match(question):
                return "Hum:ind"
        if training:
            file = DBStore.trainingRoot+"\\headword_question"+colName+".txt"
        else:
            file = DBStore.testingRoot+"\\headword_question"+colName+".txt"
        f = open(file,'r')
        p = re.compile(r"(?P<head>.+)::(?P<question>.+)")
        i = 0
        rawQuestions = DBStore.getDB()['raw'+colName]
        p2 = re.compile('\.')
        headWord = []
        for line in f:
#        line = "was:What was archy , and mehitabel ?"
            print i
            i = i + 1
            match = p.match(line)
            print match.group('question')
            head = p2.sub('',match.group('head'))
            question = match.group('question')
            raw = rawQuestions.find_one({'question':question})
            if raw['whWord']=='whWord-what':
                pattern = whatPattern(question)
            elif raw['whWord']=='whWord-who':
                pattern = whoPattern(question)
            else:
                pattern = None
            if head.isupper() and (pattern == "DESC:def_1" or pattern == 'DESC:def_2'):
                pattern = "ABBR:exp"
            if head == 'null':
                headWord = [None,pattern]
            elif pattern is None:
                headWord = [head,pattern]
            else:
                headWord = [None,pattern]
            rawQuestions.update({'question':question},{"$set":{"head":headWord}},safe=True,multi=True)
    
    def collinsHeadSenseExtractor(self,questions, colName,training):
        rawQuestions = DBStore.getDB()['raw'+colName]
        adaptedLesk = AdaptedLesk(6)
        i = 1
        questions.rewind()
        p = re.compile('(?P<head1>.+)--(?P<head2>.+)')
        for question in questions:
#        line = "was:What was archy , and mehitabel ?"
            print i
            i = i + 1
            headWord = question['head']
            try:
                match = p.match(headWord[0])
                if match:
                    headWord[0] = match.group('head1')
            except StandardError:
                    pass
            if headWord[0] is None \
                or len(wordnet.synsets(headWord[0]))==0 \
                or headWord[0] == 'null':
                headSense = "null"
            else:
                pos = DataRetrieval.replace(question['tagged'][headWord[0]])
                if question['whWord'] ==  'whWord-how':
                    headSense = 'null'
                else:
                    print question['tokenized'],headWord[0],question['tagged']
                    headSense = adaptedLesk.wsd(question['tokenized'],headWord[0],question['tagged'])
            rawQuestions.update({'qID':question['qID']},{"$set":{"headSense":headSense}},safe=True,multi=True)
    
