import ply.lex as lex

#Estado 'firstline', para a leitura de tokens na primeira linha do CSV (cabeçalho)
states = (
    ('firstline','exclusive'),
)

#Todos os Tokens da Linguagem
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

#---------------REGRAS TOKENS Firstline--------------------

# Quando lê o caracter '\n' inicia o estado 'INITIAL'
def t_firstline_NEWLINE(t):
    r'\n'
    t.lexer.begin('INITIAL')
    pass

# Capta o valor mínimo de um campo-lista
def t_firstline_MIN(t):
    r'{\d+(,|})'
    t.value = int(str(t.value).strip("{,}"))
    return t

# Capta o valor máximo de um campo-lista
def t_firstline_MAX(t):
    r'\d+}'
    t.value = int(str(t.value).strip(",}"))
    return t

# Capta a função de agregação a ser aplicada a um campo-lista
def t_firstline_FUNC(t):
    r'::[a-zA-Z]+'
    t.value = str(t.value).lstrip(":")
    return t

# Capta o nome do campo (coluna)
t_firstline_KEY = r'[^,{;\n]+'

# Caracteres a serem ignorados
t_firstline_ignore = " ,;"

# Erro do estado 'firstline'
def t_firstline_error(t):
    raise Exception('Illegal character detected on first line in column: '+str(t.lexpos+1))



#---------------REGRAS TOKENS INITIAL--------------------
# Capta um número inteiro ou decimal (positivo ou negativo)
def t_NUM(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value)
    return t

# Capta a string do campo 
def t_STRING(t):
    r'("[^"]+"|[^,;\n]+)'
    t.value = str(t.value).strip("\"")
    return t

# Capta a vírgula (delimitador de campos)
t_VIRG = r',|;'

# Caracteres a serem ignorados
t_ignore = " \n\t"

# Erro do estado 'INITIAL'
def t_error(t):
    raise Exception('Illegal character detected on line: '+str(t.lexer.linha)+' column: '+str(t.lexpos+1))



#Função de construção do lexer
def getCSVLexer():
    res = lex.lex()
    res.linha = 0
    res.begin('firstline')
    return res