import re
import ply.lex as lex
from urllib3 import Retry

literals = ["=","(",")",",",":"]
tokens = ["LEXSTART","YACCSTART","END","ID","COMERROR","SKIP","NOSKIP","STRING","COMMENT","NEWLINE",
        "ER","FSTR","FINT","FFLOAT","LEXIGNORE","LEXLITERALS","LEXCONTEXT","CHANGECONTEXT",
        "NUMVAL","EMPTYLIST","EMPTYDIC","CODIGO","YACCPRECEDENCE"]

states = (
    ('lex','inclusive'),
    ('yacc','inclusive'),
    ('outside','exclusive'),
)

##---------OUTSIDE------------

def t_outside_LEXSTART(t):
    r'%%(?i:LEX)'
    t.lexer.begin("lex")
    return t

def t_outside_YACCSTART(t):
    r'%%(?i:YACC)'
    t.lexer.begin("yacc")
    return t

def t_outside_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1

t_outside_ignore = "=,():"

def t_outside_error(t):
    t.lexer.skip(1)

##--------------LEX----------

def t_lex_YACCSTART(t):
    r'%%(?i:YACC)'
    t.lexer.begin("yacc")
    return t

t_lex_ER = r'r\'.+\''

t_lex_FSTR = r'%(?i:str)'

t_lex_FINT = r'%(?i:int)'

t_lex_FFLOAT = r'%(?i:float)'

t_lex_LEXIGNORE = r'%(?i:ignore)'

t_lex_LEXLITERALS = r'%(?i:literals)'

t_lex_LEXCONTEXT = r'%(?i:contexts)'

t_lex_CHANGECONTEXT = r'%(?i:begin)'



##--------YACC----------------

def t_yac_LEXSTART(t):
    r'%%(?i:LEX)'
    t.lexer.begin("lex")
    return t

def t_yacc_NUMVAL(t):
    r'-?\d+(.\d+)?'
    if "." in str(t.value):
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

t_yacc_EMPTYLIST = r'\[\ *\]'

t_yacc_EMPTYDIC = r'%((?i:newdict)|(?i:dict)|(?i:dic)|(?i:newdic))'

def t_yacc_CODIGO(t):
    r'\{(.|\n)*?\}'
    numPar = str(t.value).count("\n")
    t.lexer.lineno += numPar
    return t

t_yacc_YACCPRECEDENCE = r'%(?i:precedence)'



##-------INITIAL----------

def t_END(t):
    r'%%(?i:END)'
    t.lexer.begin("outside")
    return t

t_ID = r'[a-zA-Z_]\w*'

t_COMERROR = r'%(?i:error)'

t_SKIP = r'%(?i:skip)'

t_NOSKIP = r'%(?i:noskip)'

t_STRING = r'(f?\"[^"]*\")|(\'[^\']*\')'

def t_COMMENT(t):
    r'\#.*'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1


def t_error(t):
    print("Illegal Character ("+str(t.value[0])+") on line "+str(t.lexer.lineno))
    exit()

t_ignore = " \t\r"


#Função para gerar o Lexer
def getLexer():
    lexer = lex.lex()
    lexer.begin("outside")
    return lexer

#Função de DEBUG. Gera uma lista de tokens lido no ficheiro
def getTokenList(filename):
    lexer = getLexer()
    fin = open(filename,"r")
    rin = fin.read()
    lexer.input(rin)
    list = []
    
    for tok in lexer:
        list.append(str(tok))

    fin.close()
    return list