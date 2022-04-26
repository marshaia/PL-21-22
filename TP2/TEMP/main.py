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



finput = open("Exemplo.txt","r")
rinput = finput.read()

parser = getParser()
parser.parse(rinput)

out = open("Exemplo.JSON","w+")
json.dump(parser.mylex,out,indent = 4)

# Fazer um check qualquer se são dois ou um ficheiro de output
# if not dois:
#     foutput = open(filenameOutput,"w+")
#     foutput.write(strFinalFile(parser))

# elif dois:
#     foutputLex = open(filenameOutputLex, "w+")
#     foutputLex.write()

#     foutputYacc = open(filenameOutputYacc,"w+")
#     foutputYacc.write()







# finput = open("Exemplo.txt","r")
# rinput = finput.read()

# parser = getParser()
# parser.parse(rinput)

# foutput = open("Exemplo.py","w+")
# foutput.write(strFinalFile(parser))


# print(parser.myTokens)
# print(parser.myIgnore)
# print(parser.myLiterals)
# print(parser.myLexError)
# print(parser.myPrecedence)
# print(parser.myVariables)
# print(parser.myProductions)
# print(parser.myYaccError)
# print("")
# print("")
# print("")


# print(strAllTokens(parser.myTokens))
# print(strTokenList(parser.myTokens))
# print(strLiterals(parser.myLiterals))
# print(strIgnore(parser.myIgnore))
# print(strError(parser.myLexError))
# print(strError(parser.myYaccError))
# print(strVariables(parser.myVariables))
# print(strPrecedence(parser.myPrecedence))

# # for prod in parser.myProductions:
# #     print(strProduction(prod,1))

# print(strAllProductions(parser.myProductions))

