'''
Created on Mar 13, 2011

@author: Blodstone
'''

import pymongo

conn = pymongo.Connection()
col = conn['QAnlp_hypernym_head_whWord']['feature10_Fine']
result = col.find()
for test in result:
    printout =''
    for document in test:
        if document=='question':
            printout = printout + ' question: ' +test[document] + ' '
        elif document == 'FineCode':
            printout = printout + 'Fine: ' + str(test[document]) + ' '
        elif test[document]==1 and document!='CoarseCode':
            printout = printout + document + " "
    printout = printout + '\n'
    print printout

if __name__ == '__main__':
    pass