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
    flagList = ["-input","-output","-help","-divide","-debug","-wall","-verbose"]
    arguments = {}
    arguments["-input"] = ""
    arguments["-output"] = ""
    for flag in flagList:
        if flag != "-input" and flag != "-output":
            arguments[flag] = False
    argv.pop(0)
    argslen = len(argv)
    skip = False
    for i in range (0,argslen):

        if skip:
            skip = False

        elif argv[i][0] == '-':

            if argv[i] not in flagList:
                raise Exception("Opção desconhecida "+str(argv[i]))

            if argv[i] == "-input" or argv[i] == "-output":
                if i+1 >= argslen or argv[i+1][0] == "-":
                    raise Exception("Ficheiro de "+argv[i].strip("-")+" em falta")
                if arguments[argv[i]] != "":
                    raise Exception("Ficheiro de "+argv[i].strip("-")+" repetido")
                arguments[argv[i]] = argv[i+1]
                skip = True
            else:
                arguments[argv[i]] = True
                
        else:
            if arguments["-input"] != "":
                    raise Exception("Ficheiro de input repetido")
            arguments["-input"] = argv[i]
    
    if arguments["-input"] == "":
        raise Exception("Ficheiro de input em falta")

    return arguments


def progHelp():
    help = """Help
I helped
Yay"""
    return help

def printVerbose(msg):
    global args
    if args["-verbose"]:
        print("Verbose: "+str(msg))

def printWarning(msg):
    global args
    if args["-wall"]:
        print("WARNING: "+str(msg))


def verifyData(parser):
    for context in parser.mylex:
        if parser.mylex[context]["tipo"] == "None":
            raise Exception("Contexto '"+str(context)+"' declarado implicitamente, sem declaração explicita.")
    



#-----START HERE-----------

global args
#------------READ ARGS
try:
    args = readArguments(sys.argv)
except Exception as e:
    print("ERROR-ARGS: "+str(e))
    exit(1)


#------------HELP FLAG
if args["-help"]:
    print(progHelp())
    exit(0)

#------------READ & PARSE
printVerbose("Iniciando a leitura do ficheiro "+args["-input"])
finput = open(args["-input"],"r")
rinput = finput.read()
parser = getParser()
parser.parse(rinput)
printVerbose("Ficheiro lido com sucesso")


#-------------DEBUG FLAG
if args["-debug"]:
    print("DEBUG: A descarregar os conteúdos do parser em 'debug.JSON'")
    debugExtra = {}
    debugExtra["LexRead"] = parser.mylexRead
    debugExtra["YaccRead"] = parser.myyaccRead
    debugExtra["ContextRead"] = parser.mylexContextRead
    debugfile = open("debug.JSON","w+")
    json.dump([parser.mylex,parser.myyacc,debugExtra],debugfile,indent = 4)
    debugfile.close()


#-------------VERIFIER
verifyData(parser)
printVerbose("Verificado!")