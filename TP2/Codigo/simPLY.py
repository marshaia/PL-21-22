import sys
import re
import traceback
from parser import getParser
from lexer import getLexer
from auxiliary import *    


#-----START HERE-----------

global args

try:
    #------------READ ARGS
    args = readArguments(sys.argv)
except Exception as e:
    print("ERROR-ARGS: "+str(e))
    exit(1)


try:

    #------------HELP FLAG
    if args["-help"]:
        print(progHelp())
        exit(0)


    #OutPut File must be .py
    if args["-output"] != "":
        args["-output"] = re.sub(r'\.\w+$',r'.py',args["-output"])

    #Default Output File
    if args["-output"] == "":
        args["-output"] = re.sub(r'\.\w+$',r'-simPLY.py',args["-input"])

    #Force add .py
    if ".py" not in args["-output"]:
        args["-output"] += ".py"

    #Check Input and output
    if args["-output"] == args["-input"]:
        raise Exception("Ficheiro de Input e Output com o mesmo nome.")



    #------------READ & PARSE
    if args["-verbose"]:
        print("Iniciando a leitura do ficheiro "+args["-input"])

    finput = open(args["-input"],"r")
    rinput = finput.read()
    parser = getParser()
    parser.parse(rinput)
    finput.close()

    if args["-verbose"]:
        print("Ficheiro lido com sucesso")

    #-------------VERIFIER
    verifyData(parser,args["-wall"])


    if args["-verbose"]:
        print("Verificado!")

    #-------------DEBUG FLAG
    if args["-debug"]:
        debugDump(parser,args["-input"])


    #-------------WRITE

    if args["-verbose"]:
        print("Escrevendo no ficheiro output: "+args["-output"])

    writeFile(args["-output"],parser,args["-plyonly"],args["-input"])
    print("Compilação terminada com Sucesso! (Output: "+args["-output"]+")")

except Exception as e:
    print("ERROR: "+str(e))
    if args["-debug"]:
        print("\n----- DEBUG TRACEBACK -----\n")
        traceback.print_tb(e.__traceback__)
    exit(1)