'''
Created on Mar 8, 2011

@author: Blodstone
'''
from IOPreprocessing.DBStore import DBStore

lines = DBStore.commonRoot + '\\words5500.txt'
i=0
f = open(lines,'r')
for line in f:
    print i
    i = i+1