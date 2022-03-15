from multiprocessing.sharedctypes import Value
import re
import ply.lex as lex

# TEM DE SER O NOME "TOKENS"
tokens = [
    "NUM",
    "FUNC",
    "AGREG",
    "STRING",
    "ERRO"
]

# t_TOKEN para identificar a expressão do token
t_STRING = r'[^,]+'
t_AGREG = r'[^,]+\{\d+(,\d+)?\}'
t_ERRO = r'.'

t_ignore = " \n\t,"

def t_NUM(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_FUNC(t):
    r'(?:::)[a-zA-Z]+'
    t.value = str(t.value).lstrip(":")
    return t

def t_error(t):
    print('Illegal character')
    exit()

def getLexer():
    return lex.lex()
