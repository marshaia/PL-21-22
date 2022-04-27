import sys
from parser import getParser
from lexer import getLexer
from writer import strFinalFile
import json


#   [fileINPUT]   [OPTIONS]     [fileOUTPUT]
#     argv[1]      argv[2]        argv[3]

# Verificação de argumentos e ficheiro

# dois = bool(False)
# try:
#     filenameInput = sys.argv[1] # Capta o nome do ficheiro

#     fileOPTION = sys.argv[2] # Capta a opção de output dos ficheiros

#     if fileOPTION.__eq__("1"):
#         filenameOutput = sys.argv[3] + ".py"

#     elif fileOPTION.__eq__("2"):
#         dois = bool(True)
#         filenameOutputLex = sys.argv[3] + "_Lex.py"
#         filenameOutputYacc = sys.argv[3] + "_Yacc.py"
        

# except FileNotFoundError as e:
#     sys.exit("Initialization Failed: "+str(e))
# except IndexError as e:
#     sys.exit("Initialization Failed :(((( ")


def readArguments(argv):
    flagList = ["-i","-input","-o","-output","-help","-divide","-debug","-wall"]
    arguments = {}
    arguments["input"] = ""
    arguments["output"] = ""
    arguments["help"] = False
    arguments["divide"] = False
    arguments["debug"] = False
    arguments["wall"] = False
    argv.pop(0)
    argslen = len(argv)
    skip = False
    for i in range (0,argslen):

        if skip:
            skip = False

        elif argv[i][0] == '-':

            if argv[i] not in flagList:
                raise Exception("Opção desconhecida "+str(argv[i]))

            if argv[i] == "-input" or argv[i] == "-i":
                if i+1 >= argslen or argv[i+1][0] == "-":
                    raise Exception("Ficheiro de Entrada em falta")
                if arguments["input"] != "":
                    raise Exception("Ficheiro de Entrada repetido")
                arguments["input"] = argv[i+1]
                skip = True
            elif argv[i] == "-output" or argv[i] == "-o":
                if i+1 >= argslen or argv[i+1][0] == "-":
                    raise Exception("Ficheiro de Saída em falta")
                if arguments["output"] != "":
                    raise Exception("Ficheiro de Saída repetido")
                arguments["output"] = argv[i+1]
                skip = True
            else:
                arguments[argv[i]] = True
                
        else:
            if arguments["input"] != "":
                    raise Exception("Ficheiro de Entrada repetido")
            arguments["input"] = argv[i]

    return arguments


print(readArguments(sys.argv))

#-------------JSON
# finput = open("Exemplo.txt","r")
# rinput = finput.read()

# parser = getParser()
# parser.parse(rinput)

# out = open("Exemplo.JSON","w+")
# json.dump(parser.mylex,out,indent = 4)
# out.write('\n' * 6)
# json.dump(parser.myyacc,out,indent = 4)
# out.write('\n' * 6)
# out.write("LexRead:"+str(parser.mylexRead)+"\n")
# out.write("YaccRead:"+str(parser.myyaccRead)+"\n")
# out.write("ContextRead:"+str(parser.mylexContextRead)+"\n")
#------------------