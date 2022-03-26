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
    "VIRG"
]

# t_TOKEN para identificar a expressão do token
def t_firstline_NEWLINE(t):
    r'\n'
    t.lexer.begin('INITIAL')
    pass

def t_firstline_MIN(t):
    r'{\d+(,|})'
    t.value = int(str(t.value).strip("{,}"))
    return t

def t_firstline_MAX(t):
    r'\d+}'
    t.value = int(str(t.value).strip(",}"))
    return t

def t_firstline_FUNC(t):
    r'::[a-zA-Z]+'
    t.value = str(t.value).lstrip(":")
    return t

t_firstline_KEY = r'[^,{;\n]+'

t_firstline_ignore = " ,;"

def t_firstline_error(t):
    raise Exception('Illegal character detected on first line in column: '+str(t.lexpos+1))



def t_NUM(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'("[^"]+"|[^,;\n]+)'
    t.value = str(t.value).strip("\"")
    return t

t_VIRG = r',|;'


t_ignore = " \n\t"

def t_error(t):
    raise Exception('Illegal character detected on line: '+str(t.lexer.linha)+' column: '+str(t.lexpos+1))

def getCSVLexer():
    res = lex.lex()
    res.linha = 0
    res.begin('firstline')
    return res
