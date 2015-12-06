'''
Created on Mar 24, 2011

@author: Blodstone
'''
from nltk.corpus import wordnet, stopwords
import string
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
class Lesk:
    
    def wsd(self,sent ,target):
        self.target = target 
        sent = word_tokenize(sent)
#        words = [pair for pair in tagged if len(wordnet.synsets(pair[0])) != 0]
        words = [word for word in sent if len(wordnet.synsets(word)) != 0]
        synTarget = wordnet.synsets(target)
        maxCount = -1
        optimum = None
        for syn in synTarget:
            count = 0 
            definition = syn.definition
            for word in words:
                if word == target: continue
                wordSyns = wordnet.synsets(word)
                glossBag = ''
                for wordSyn in wordSyns:
                    glossBag = glossBag + ' ' + string.join([hypernim.definition for hypernim in wordSyn.hypernyms()])
                    glossBag = glossBag + ' ' +  string.join([hyponim.definition for hyponim in wordSyn.hyponyms()])
                    glossBag = glossBag + ' ' +  wordSyn.definition
                    glossBag = glossBag + ' ' +  string.join([example for example in wordSyn.examples])
                    glossBag = glossBag + ' ' +  string.join([holonym.definition for holonym in wordSyn.part_holonyms()])
                    glossBag = glossBag + ' ' +  string.join([meronym.definition for meronym in wordSyn.part_holonyms()])
                subMax = self.oSL(glossBag,definition)
                count = count + subMax
            if maxCount<count:
                maxCount = count
                optimum = syn
        return optimum
    
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

if __name__ == '__main__':
    lesk = Lesk()
    sense = lesk.wsd('What is the average speed of the horses at the Kentucky Derby ?','speed')
    print str(sense.name),sense.definition