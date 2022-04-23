from parser import getParser
from lexer import getLexer
from writer import *

f = open("Exemplo.txt","r")
r = f.read()

parser = getParser()

parser.parse(r)
print(parser.myTokens)
print(parser.myIgnore)
print(parser.myLiterals)
print(parser.myLexError)
print(parser.myPrecedence)
print(parser.myVariables)
print(parser.myProductions)
print(parser.myYaccError)
print("")
print("")
print("")


print(strAllTokens(parser.myTokens))
print(strTokenList(parser.myTokens))
print(strLiterals(parser.myLiterals))
print(strIgnore(parser.myIgnore))
print(strError(parser.myLexError))
print(strError(parser.myYaccError))
print(strVariables(parser.myVariables))

# for prod in parser.myProductions:
#     print(strProduction(prod,1))

print(strAllProductions(parser.myProductions))