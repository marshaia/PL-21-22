from parser import getParser
from lexer import getLexer
from writer import *

def strLex(parser):
    res = ""    
    res += strLiterals(parser.myLiterals)
    res += strTokenList(parser.myTokens)
    res += "\n\n"+strAllTokens(parser.myTokens)
    res += strIgnore(parser.myIgnore)
    res += "\n"+strError(parser.myLexError,"lex")
    return res

def strYacc(parser):
    res = ""
    res += strPrecedence(parser.myPrecedence)
    res += "\n"+strAllProductions(parser.myProductions,parser.myLiterals)
    res += strError(parser.myYaccError,"yacc")  
    res += "\n\nparser = yacc.yacc()\n"  
    res += strVariables(parser.myVariables)
    return res

def strFinalFile(parser):
    res = ""
    res += "import ply.lex as lex\nimport ply.yacc as yacc\n\n"
    res += "\n#LEX---------------\n\n"
    res += strLex(parser)
    res += "\n#YACC---------------\n\n"
    res += strYacc(parser)
    res += "\n#Tradução PLY-Simples concluída"
    return res


finput = open("Exemplo.txt","r")
rinput = finput.read()

parser = getParser()
parser.parse(rinput)

foutput = open("Exemplo.py","w+")
foutput.write(strFinalFile(parser))


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

