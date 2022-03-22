from tokenizer import *
from lineProcessor import * 
from JSONconverter import *
import os
import sys

#preciso deste pra funcionar no meu, ignorem
#filenameCSV ="/home/mirtilo/PL-21-22/TP1/CSV/agregacaoSUM.csv"
filenameCSV = "agregacaoSUM.csv"
#filenameCSV = sys.argv[1]
filenameJSON = filenameCSV.replace(".csv",".JSON")
fileCSV = open(filenameCSV,'r')
fileJSON = open(filenameJSON,'w+')


fileJSON.write("[\n")
firstEntry = bool(True)

lexer = getCSVLexer()
keyList = []

for line in fileCSV:
    lexer.input(line)
    lexer.linha += 1
    if lexer.current_state() == 'firstline':
        try:
            keyList = readFirstLine(lexer)
            print(keyList)
        except Exception as e:
            os.remove(filenameJSON)
            sys.exit("Header Malfunction :(\nCause of error: "+str(e))
        
    else:
        try:
            dic = processLine(keyList,lexer)
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
