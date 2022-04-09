import re
import ply.lex as lex

literals = ["=","(",")",",",";",":"]
tokens = ["LEXSTART","YACCSTART","END","TOKENID","ER","FSTR","FINT","FFLOAT",
        "FDOUBLE","LEXIGNORE","LEXLITERALS","STRING","COMERROR",
        "INSTRUCTION","YACCVAR","YACCVALUE","YACCGRAM","YACCGRAMVALUE","YACCGRAMCOM","COMMENT"]

states = (
    ('lex','inclusive'),
    ('yacc','inclusive'),
    ('outside','exclusive'),
    ('yaccgram','inclusive'),
    ('yaccvarvalue','inclusive'),
)

def t_LEXSTART(t):
    r'%%LEX'
    t.lexer.begin("lex")
    return t

def t_YACCSTART(t):
    r'%%YACC'
    t.lexer.begin("yacc")
    return t

def t_END(t):
    r'%%'
    t.lexer.begin("outside")
    return t


t_lex_TOKENID = r'[A-Z]+'

t_lex_ER = r'r\'.+\''

t_lex_FSTR = r'str'

t_lex_FINT = r'int'

t_lex_FFLOAT = r'float'

t_lex_FDOUBLE = r'double'

t_lex_LEXIGNORE = r'%ignore'

t_lex_LEXLITERALS = r'%literals'

def t_yacc_YACCVAR(t):
    r'&[a-zA-Z_]+'
    t.lexer.begin("yaccvarvalue")
    return t

def t_yaccvarvalue_YACCVALUE(t):
    r'([^\n#=]+|\"[^"]\")'
    t.lexer.begin("yacc")
    return t


def t_yacc_YACCGRAM(t):
    r'[a-z]+'
    t.lexer.begin("yaccgram")
    return t

t_yacc_YACCGRAMCOM = r'{.+}'



def t_yaccgram_YACCGRAMVALUE(t):
    r'[^{\n:]+'
    t.lexer.begin("yacc")
    return t


def t_COMMENT(t):
    r'\#[^\n]*' 
    return t

t_STRING = r'f?\".+\"'

t_COMERROR = r'%error' 

t_INSTRUCTION = r'[a-zA-Z\.\[\]0-9 ]+' #HELP


t_ignore = " \n\t\r"



def t_outside_LEXSTART(t):
    r'%%LEX'
    t.lexer.begin("lex")
    return t

def t_outside_YACCSTART(t):
    r'%%YACC'
    t.lexer.begin("yacc")
    return t

t_outside_ignore = "=(),;:"

def t_outside_error(t):
    t.lexer.skip(1)




def t_error(t):
    print("Illegal Character:",t.value[0])
    t.lexer.skip


def getLexer():
    lexer = lex.lex()
    lexer.begin("outside")
    return lexer