import sys
import re
from parser import getParser
from lexer import getLexer
from auxiliary import *    


#-----START HERE-----------

global args

#------------READ ARGS
try:
    args = readArguments(sys.argv)

    if args["-output"] != "":
        args["-output"] = re.sub(r'\.\w+$',r'.py',args["-output"])
        if ".py" not in args["-output"]:
            args["-output"] += ".py"

    if args["-output"] == "":
        args["-output"] = re.sub(r'\.\w+$',r'-simPLY.py',args["-input"])

    if args["-output"] == args["-input"]:
        raise Exception("Ficheiro de Input e Output com o mesmo nome")
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
    finput.close()
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

if args["-verbose"]:
    print("Escrevendo no ficheiro output: "+args["-output"])

try:
    writeFile(args["-output"],parser,args["-plyonly"],args["-input"])
except Exception as e:
    print("ERROR: "+str(e))
    exit(1)

print("Compilação terminada com Sucesso! (Output: "+args["-output"]+")")