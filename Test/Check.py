'''
Created on Feb 8, 2011

@author: Blodstone
'''

import pymongo

conn = pymongo.Connection()
col = conn['QAnlp_head_whWord']['feature10_Fine']
result = col.find()
count = 0 
question = []
for tes in result:
    print len(tes)-5
#    break
#    if len(tes) != 7979:
#        count = count + 1
#        question.append(tes['Question'])

print count
print question
