from tokenizer import *
from lineProcessor import * 
from JSONconverter import *
import os
import sys

#preciso deste pra funcionar no meu, ignorem
filenameCSV ="agregacaoSUM.csv"
#filenameCSV = "agregacaoSUM.csv"
#filenameCSV = sys.argv[1]
filenameJSON = filenameCSV.replace(".csv",".JSON")
fileCSV = open(filenameCSV,'r')
fileJSON = open(filenameJSON,'w+')


fileJSON.write("[\n")
firstEntry = bool(True)

lexer = getCSVLexer()
keyList = []
numLine = 0

for line in fileCSV:
    lexer.input(line)
    numLine += 1
    if lexer.current_state() == 'firstline':
        keyList = readFirstLine(lexer)
    else:
        try:
            dic = processLine(keyList,lexer,numLine)
        except Exception as e:
            os.remove(filenameJSON)
            sys.exit("Conversion Failed :(\nCause of error: "+str(e))
        jsonObj = convertDicToJSONLine(dic)
        if not firstEntry:
            fileJSON.write(",\n")
        fileJSON.write(jsonObj)
        firstEntry = bool(False)

fileJSON.write("\n]")
fileJSON.close()
fileCSV.close()
print("DONE! :D")
