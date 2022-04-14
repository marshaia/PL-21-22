import re
import ply.lex as lex
from urllib3 import Retry

literals = ["=","(",")",",",":"]
tokens = ["LEXSTART","YACCSTART","END","ER","TOKENID","FSTR","FINT","FFLOAT","TOKENEND",
        "SKIP","NOSKIP","FDOUBLE","LEXIGNORE","LEXLITERALS","STRING","COMERROR","YACCVAR",
        "YACCVALUE","YACCGRAM","YACCGRAMVALUE","YACCGRAMCOM","YACCPRECEDENCE","COMMENT"]

states = (
    ('lex','inclusive'),
    ('yacc','inclusive'),
    ('yaccgram','inclusive'),
    ('yaccvarvalue','inclusive'),
    ('outside','exclusive'),
)

##---------OUTSIDE------------

def t_outside_LEXSTART(t):
    r'%%LEX'
    t.lexer.begin("lex")
    return t

t_outside_ignore = "=,():"

def t_outside_error(t):
    t.lexer.skip(1)

##--------------LEX----------

t_lex_ER = r'r\'.+\''

t_lex_FSTR = r'str'

t_lex_FINT = r'int'

t_lex_FFLOAT = r'float'

t_lex_FDOUBLE = r'double'

t_lex_TOKENID = r'[A-Z_][a-z-A-Z_]*'

t_lex_LEXIGNORE = r'%ignore'

t_lex_LEXLITERALS = r'%literals'

t_lex_TOKENEND = r'%tokenEnd'



def t_lex_YACCSTART(t):
    r'%%YACC'
    t.lexer.begin("yacc")
    return t


##--------YACC----------------

def t_yacc_END(t):
    r'%%'
    t.lexer.begin("outside")
    return t


def t_yacc_YACCVAR(t):
    r'[a-zA-Z_]+\ {0,}='
    t.lexer.begin("yaccvarvalue") #r'[a-zA-Z_]+ {0,}='
    return t

def t_yaccvarvalue_YACCVALUE(t):
    r'(\[ {0,}\]|\{ {0,}\}|-?\d+(.\d+)?|\"[^"]+\")'
    t.lexer.begin("yacc")
    return t

def t_yacc_YACCGRAM(t):
    r'[a-zA-Z_]+\ {0,}:'
    t.lexer.begin("yaccgram")
    return t

def t_yaccgram_YACCGRAMVALUE(t):
    r'([^\n]+|$empty)'
    t.lexer.begin("yacc")
    return t

def t_yacc_YACCGRAMCOM(t):
    r'\{(.|\n)*?\}'
    return t

def t_yacc_YACCPRECEDENCE(t):
    r'%precedence'
    return t


##-------INITIAL----------

t_SKIP = r'skip'

t_NOSKIP = r'noskip'

def t_COMERROR(t):
    r'%error'
    return t

def t_COMMENT(t):
    r'\#.*'

def t_STRING(t):
    r'\"[^"]*\"'
    return t

def t_error(t):
    print("Illegal Character REEE:",t.value[0])
    exit()

t_ignore = " \n\t\r"




def getLexer():
    lexer = lex.lex()
    lexer.begin("outside")
    return lexer