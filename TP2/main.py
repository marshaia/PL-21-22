from parser import getParser
from lexer import getLexer

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