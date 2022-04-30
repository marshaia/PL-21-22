import sys
from parser import getParser
from lexer import getLexer
from strFormatter import strFinalFile
from auxiliary import *

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


# def readArguments(argv):
#     flagList = ["-input","-output","-help","-divide","-debug","-wall","-verbose"]
#     arguments = {}
#     arguments["-input"] = ""
#     arguments["-output"] = ""
#     for flag in flagList:
#         if flag != "-input" and flag != "-output":
#             arguments[flag] = False
#     argv.pop(0)
#     argslen = len(argv)
#     skip = False
#     for i in range (0,argslen):

#         if skip:
#             skip = False

#         elif argv[i][0] == '-':

#             if argv[i] not in flagList:
#                 raise Exception("Opção desconhecida "+str(argv[i]))

#             if argv[i] == "-input" or argv[i] == "-output":
#                 if i+1 >= argslen or argv[i+1][0] == "-":
#                     raise Exception("Ficheiro de "+argv[i].strip("-")+" em falta")
#                 if arguments[argv[i]] != "":
#                     raise Exception("Ficheiro de "+argv[i].strip("-")+" repetido")
#                 arguments[argv[i]] = argv[i+1]
#                 skip = True
#             else:
#                 arguments[argv[i]] = True
                
#         else:
#             if arguments["-input"] != "":
#                     raise Exception("Ficheiro de input repetido")
#             arguments["-input"] = argv[i]
    
#     if arguments["-input"] == "":
#         raise Exception("Ficheiro de input em falta")

#     return arguments


# def progHelp():
#     help = """Help
# I helped
# Yay"""
#     return help

# def debugDump(parser):
#     print("DEBUG: A descarregar os conteúdos do parser em 'debug.JSON'")
#     debugfile = open("debug.JSON","w+")
#     json.dump([parser.mylex,parser.myyacc,parser.mycontents],debugfile,indent = 4)
#     debugfile.close()

# def printVerbose(msg):
#     global args
#     if args["-verbose"]:
#         print(str(msg))

# def printWarning(msg):
#     global args
#     if args["-wall"]:
#         print("WARNING: "+str(msg))


# def verifyData(parser):

#     if not parser.mycontents["lexRead"]:
#         printWarning("Nenhum bloco LEX lido, impossível verificar as produções")
#         return

#     for context in parser.mylex:
#         #CHECK Contextos Nulos
#         if parser.mylex[context]["tipo"] == "None":
#             raise Exception("Contexto '"+str(context)+"' declarado implicitamente mas sem declaração explicita.")

#         if parser.mylex[context]["tipo"] == "exclusive":
#             #CHECK Regra IGNORE
#             if not parser.mylex[context]["ignoreRead"]:
#                 msg = "Parâmetro Ignore em falta"
#                 if context != "INITIAL":
#                     msg += " no contexto exclusivo '"+str(context)+"'"
#                 msg += ". Valor por defeito utilizado"
#                 printWarning(msg)

#             #CHECK Regra ERROR
#             if not parser.mylex[context]["errorRead"]:
#                 msg = "Parâmetro Error em falta (Lex)"
#                 if context != "INITIAL":
#                     msg += " no contexto exclusivo '"+str(context)+"'"
#                 msg += ". Valor por defeito utilizado"
#                 printWarning(msg)
    
#     for prod in parser.myyacc["productions"]:
#         words = prod["conteudo"].split()
#         for word in words:
#             word = word.strip("'")
#             if (word not in parser.mycontents["tokenlist"]) and (word not in parser.mycontents["literalslist"]) and (word not in parser.mycontents["prodlist"]):
#                 raise Exception("Termo desconhecido '"+word+"' encontrado na produção -> "+prod["nome"]+" ("+prod["alias"]+") : "+prod["conteudo"])

#         conteudo = prod["conteudo"].replace("'","")
#         #prod["conteudo"] = conteudo
#         for chr in parser.mycontents["literalslist"]:
#             #conteudo = prod["conteudo"]
#             conteudo = conteudo.replace(chr,"'"+chr+"'")
#             #prod["conteudo"] = conteudo
#         prod["conteudo"] = conteudo
            
            
    
    


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