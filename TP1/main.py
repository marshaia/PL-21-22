from operator import imod
import re
from tokenizer import *
from lineProcessor import * 
import ply.lex as lex
import sys
import json


file = open("agregacaoSUM.csv")

lexer = getCSVLexer()

keyList = []
for line in file:
    lexer.input(line)
    if lexer.current_state() == 'firstline':
        keyList = readFirstLine(lexer)
    else:
        try:
            dic = processLine(keyList,lexer)
        except Exception as e:
            print(e)
            break
        print(dic)

