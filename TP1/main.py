from tokenizer import *
from keyReader import * 
import ply.lex as lex
import sys

file = open("agregacaoSUM.csv")

lex = getCSVLexer()

keyList = []
firstline = bool(True) 
for line in file:
    lex.input(line)
    if firstline:
        keyList = readFirstLine(lex)
        firstline = bool(False)
    else:
        print("Linha processada")


print(keyList)
