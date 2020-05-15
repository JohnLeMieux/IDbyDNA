import sys
import re
import time
from hashTable import HashTable

def count25mers(entry):
    i = firstValidIndex(entry)
    while i < len(entry) - 24:
        if ('A','T','C','G').count(entry[i + 24]) == 0:
            i += 25
        else:
            hashtable.insertAndUpdateCounts(entry[i:i + 25])
            i += 1

def firstValidIndex(entry):
    i = 0
    noise = re.search('[^ATCG]', entry[0:25])
    while noise != None and i < len(entry) - 24:
        i = noise.span()[1]
        noise = re.search('[^ATCG]', entry[i:i + 25])
    return i

def evaluateLine(line, entry):
    if line.startswith('>'):
        count25mers(entry)
        return ''
    else:
        return entry + line.replace('\n','')

try:
    hashtable = HashTable()
    filename = sys.argv[1]
    file = open(filename)
    entry = ''
    for line in file:
        entry = evaluateLine(line, entry)
    file.close()
    count25mers(entry)
except Exception as e:
    print(e)
finally:
    print('Distinct 25-mers: ' + str(hashtable.size))
    print('Total 25-mers: ' + str(hashtable.total))
    print('Highest count: ' + hashtable.mostCommon)