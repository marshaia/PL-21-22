from tokenizer import *
from lineProcessor import * 
from JSONconverter import *
import os
import sys

try:
    filenameCSV = sys.argv[1]
    if not filenameCSV.__contains__(".csv"):
        raise FileNotFoundError("Input File must be a CSV file")
    filenameJSON = filenameCSV.replace(".csv",".JSON")
    fileCSV = open(filenameCSV,'r')
    fileJSON = open(filenameJSON,'w+')
except FileNotFoundError as e:
    sys.exit("Initialization Failed: "+str(e))
except IndexError as e:
    sys.exit("Initialization Failed: No input file given")


fileJSON.write("[\n")
firstEntry = bool(True)

lexer = getCSVLexer()
keyList = []

for line in fileCSV:

    try:
        lexer.input(line)
        lexer.linha += 1
    except Exception as e:
        os.remove(filenameJSON)
        sys.exit("Tokenizer Malfunction :(\nCause of error: "+str(e))


    if lexer.current_state() == 'firstline':
        try:
            keyList = readFirstLine(lexer)
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
print("Conversion terminated successfully")
print("Output file: "+str(filenameJSON))
