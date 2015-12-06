'''
Created on Mar 24, 2011

@author: Blodstone
'''

from nltk import ne_chunk as nc
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize as wt

tokenizeWords = wt('Who is Samuel Pickering ?')
pos = pos_tag(tokenizeWords)
n = nc(pos)
print n

