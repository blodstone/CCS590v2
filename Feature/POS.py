'''
Created on Feb 7, 2011

@author: Blodstone
'''

from nltk.tag import tnt
from nltk.tag import brill
from nltk.tag import pos_tag
from nltk.corpus import conll2000,treebank
import pickle
import time
import itertools
from nltk.tag.sequential import UnigramTagger, BigramTagger, TrigramTagger,\
    DefaultTagger
import nltk

class POSTagger:
    
    def __init__(self):
        self.filePath = 'E:/Kuliah/Postgraduate/Assignment/CCS590/Experiment/tagger.tag' 
    
    def backoff_tagger(self,train_sents, tagger_classes, backoff=None):
        for cls in tagger_classes:
            backoff = cls(train_sents, backoff=backoff)
        return backoff

    def train(self):
        start = time.time()
        templates = [
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
            brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
            brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
            brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1))
        ]
        self.train_sents = conll2000.tagged_sents('train.txt')
        word_patterns = [
            (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
            (r'.*ould$', 'MD'),
            (r'.*ing$', 'VBG'),
            (r'.*ed$', 'VBD'),
            (r'.*ness$', 'NN'),
            (r'.*ment$', 'NN'),
            (r'.*ful$', 'JJ'),
            (r'.*ious$', 'JJ'),
            (r'.*ble$', 'JJ'),
            (r'.*ic$', 'JJ'),
            (r'.*ive$', 'JJ'),
            (r'.*ic$', 'JJ'),
            (r'.*est$', 'JJ'),
            (r'^a$', 'PREP'),
        ]
        raubt_tagger = self.backoff_tagger(self.train_sents, [nltk.tag.AffixTagger,
                                                              nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],
                                                              backoff=nltk.tag.RegexpTagger(word_patterns))
        trainer = brill.FastBrillTaggerTrainer(raubt_tagger, templates,deterministic=True)
        self.tagger = trainer.train(self.train_sents,max_rules=100, min_score=3)
        self.save2Pickle(self.tagger)
        print 'Time: ' + str(time.time()-start)
        
    def save2Pickle(self,tagger):
        f = open(self.filePath,'w')
        pickle.dump(self.tagger,f)
        f.close()
    
    def loadTagger(self):
        f = open(self.filePath,'r')
        self.tagger = pickle.load(f)
        
    def getTagger(self):
        return self.tagger

if __name__ == "__main__": 
    pos = POSTagger()
#    print 'training'
#    pos.train()
    print 'loading'
    pos.loadTagger()
    tagger = pos.getTagger()
    print 'tagging'
    token = [u'What', u'are', u'liver', u'enzymes']
    result = tagger.tag(token)
    print result
    result = pos_tag(token)
    print result