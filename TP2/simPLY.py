import sys
from parser import getParser
from lexer import getLexer
from strFormatter import strFinalFile
from auxiliary import *    


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
if args["-verbose"]:
    print("Iniciando a leitura do ficheiro "+args["-input"])

try:
    finput = open(args["-input"],"r")
    rinput = finput.read()
    parser = getParser()
    parser.parse(rinput)
except Exception as e:
    print("ERROR: "+str(e))
    exit(1)

if args["-verbose"]:
    print("Ficheiro lido com sucesso")

#-------------VERIFIER
try:
    verifyData(parser,args["-wall"])
except Exception as e:
    print("ERROR: "+str(e))
    exit(1)

if args["-verbose"]:
    print("Verificado!")

#-------------DEBUG FLAG
if args["-debug"]:
    debugDump(parser)


#-------------WRITE

print(strFinalFile(parser))