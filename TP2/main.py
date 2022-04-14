from parser import getParser
from lexer import getLexer

f = open("Exemplo.txt","r")
r = f.read()

parser = getParser()
lexer = getLexer()

lexer.input(r)

for tok in lexer:
    print(tok)

parser.parse(r)