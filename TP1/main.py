from tokenizer import *
from lineProcessor import * 
from JSONconverter import *
import os
import sys


#Verificação de argumentos e ficheiro
try:
    filenameCSV = sys.argv[1] # Capta o nome do ficheiro

    if not filenameCSV.__contains__(".csv"): # Verifica se o ficheiro tem a extensão ".csv"
        raise FileNotFoundError("Input File must be a CSV file")

    filenameJSON = filenameCSV.replace(".csv",".JSON") # Contrói o nome do ficheiro de output com a extensão ".JSON"
    fileCSV = open(filenameCSV,'r') # Abre o ficheiro de input para leitura
    fileJSON = open(filenameJSON,'w+') # Abre o ficheiro de output para escrita
except FileNotFoundError as e:
    sys.exit("Initialization Failed: "+str(e))
except IndexError as e:
    sys.exit("Initialization Failed: No input file given")


# Escrita Inicial JSON
fileJSON.write("[\n")
firstEntry = bool(True)

# Montar o Lexer
lexer = getCSVLexer()
keyList = []

for line in fileCSV:

    #Tokenizar a linha
    try:
        lexer.input(line)
        lexer.linha += 1
    except Exception as e:
        os.remove(filenameJSON)
        sys.exit("Tokenizer Malfunction :(\nCause of error: "+str(e))

    # Se é a primeira linha, gera a lista de atributos
    if lexer.current_state() == 'firstline':
        try:
            keyList = readFirstLine(lexer)
        except Exception as e:
            os.remove(filenameJSON)
            sys.exit("Header Malfunction :(\nCause of error: "+str(e))
        
    # Senão, processa com a linha com a lista de atributos
    else:
        try:
            dic = processLine(keyList,lexer)
        except Exception as e:
            os.remove(filenameJSON)
            sys.exit("Conversion Failed :(\nCause of error: "+str(e))
            
        #Conversão e escrita no ficheiro JSON
        jsonObj = convertDicToJSONLine(dic)
        if not firstEntry:
            fileJSON.write(",\n")
        fileJSON.write(jsonObj)
        firstEntry = bool(False)

#Escrita Final e Finalização
fileJSON.write("\n]")
fileJSON.close()
fileCSV.close()
print("Conversion terminated successfully")
print("Output file: "+str(filenameJSON))
