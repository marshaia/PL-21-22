from fileinput import filename
from tokenizer import *
from lineProcessor import * 
import sys
import os
#preciso deste pra funcionar no meu, ignorem
filenameCSV ="/home/mirtilo/PL-21-22/TP1/listasInterTam.csv"
#filenameCSV = "agregacaoSUM.csv"
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
    if lexer.current_state() == 'firstline':
        keyList = readFirstLine(lexer)
    else:
        try:
            dic = processLine(keyList,lexer)
        except Exception as e:
            os.remove(filenameJSON)
            print(e)
            break
        jsonObj = convertDicToJSONLine(dic)
        if not firstEntry:
            fileJSON.write(",\n")
        fileJSON.write(jsonObj)
        firstEntry = bool(False)

fileJSON.write("\n]")
fileJSON.close()
fileCSV.close()
print("DONE! :D")
