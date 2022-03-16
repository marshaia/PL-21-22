import ply.lex as lex

states = (
    ('firstline','exclusive'),
)

# TEM DE SER O NOME "TOKENS"
tokens = [
    "MIN",
    "MAX",
    "FUNC",
    "KEY",
    "NEWLINE",
    "NUM",
    "STRING",
    "VIRG",
    "ERRO"
]

# t_TOKEN para identificar a expressão do token
def t_firstline_NEWLINE(t):
    r'\n'
    t.lexer.begin('INITIAL')
    pass

def t_firstline_MIN(t):
    r'{\d+'
    t.value = int(str(t.value).lstrip("{"))
    return t

def t_firstline_MAX(t):
    r'\d+}'
    t.value = int(str(t.value).rstrip("}"))
    return t

def t_firstline_FUNC(t):
    r'::[a-zA-Z]+'
    t.value = str(t.value).lstrip(":")
    return t

t_firstline_KEY = r'[^,{]+'

t_firstline_ignore = " ,"

def t_firstline_error(t):
    print('Illegal character')
    exit()



def t_NUM(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value)
    return t

t_STRING = r'[^,;]+'

t_VIRG = r',|;'



t_ERRO = r'.'

t_ignore = " \n\t"

def t_error(t):
    print('Illegal character')
    exit()

lex.Lexer.current_state

def getCSVLexer():
    res = lex.lex()
    res.begin('firstline')
    return res
