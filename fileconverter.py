import sys
import json
import re

def readFile(filename):
    try:
        file = open(filename)
        processFile = processorFactory(file)
        commonFormat = (processFile(file))
        print(commonFormat["Collection"])
        printReport(commonFormat)
        file.close()
    except Exception as e:
        print(e)

def processorFactory(file):
    firstChar = file.read(1)
    file.seek(0, 0)

    def processTypeA(file):
        collection = []
        error = False
        for line in file:
            part = ''
            number = 0
            for i in range(len(line)):
                currentChar = line[i]
                if not currentChar.isnumeric():
                    if currentChar == 'X':
                        error = True
                    part += currentChar
                else:
                    number = number * 10 + int(currentChar)
                    if i == len(line) - 1 or not line[i + 1].isnumeric():
                        collection.append(formatData(part, number))
                        part = ''
                        number = 0
        return {"Error": error, "Collection": collection}

    def processTypeB(file):
        collection = []
        error = False
        data = getJSONData(file)
        count = data["Count"]
        parts = data["Parts"]
        numbers = data["Numbers"]
        for i in range(count):
            if i < len(parts) and i < len(numbers):
                collection.append(formatData(parts[i], numbers[i]))
            if i >= len(parts) or i >= len(numbers) or parts[i].find('X') > -1:
                error = True
        return {"Error": error, "Collection": collection}

    if firstChar == '{':
        return processTypeB
    return processTypeA

def formatData(part, number):
    return {
        "Part": part,
        "Number": number,
        "PartLength": len(part)
    }

def getJSONData(file):
    string = ''
    for line in file:
        string += line
    string = formatJSONString(string)
    return json.loads(string)

def formatJSONString(string):
    return re.sub(r"(\W(?=[A-Za-z])|(?=:))", '"', string)

def printReport(commonFormat):
    error = commonFormat["Error"]
    collection = commonFormat["Collection"]
    output = ''
    for i in range(len(collection)):
        if len(output) > 0:
            output += ' '
        output += collection[i]["Part"] + ':' + str(collection[i]["Number"])
    if error:
        output += ', error found an X'
    print(output)

for i in range(1, len(sys.argv)):
    readFile(sys.argv[i])