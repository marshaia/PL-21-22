from numpy import empty
from tokenizer import *
import ply.lex as lex
import sys

file = open("agregacaoSUM.csv")

lexer = getLexer()

dic = {}

for line in file:
    lexer.input(line)
    for tok in lexer:
        print(tok.type)
        print(tok.value)