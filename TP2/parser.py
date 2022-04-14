import ply.yacc as yacc
from lexer import getLexer
from lexer import tokens



def p_prog(p):
    "prog : lexOp yaccOp END"


def p_lexOp_empty(p):
    "lexOp : "
def p_lexOp_lex(p):
    "lexOp : LEXSTART lex"


def p_yaccOp_empty(p):
    "yaccOp : "
def p_yaccOp_yacc(p):
    "yaccOp : YACCSTART yacc"


def p_lex(p):
    "lex : lexParametros"


def p_lexParametros_single(p):
    "lexParametros : lexParametro"
def p_lexParametros_multi(p):
    "lexParametros : lexParametros lexParametro"


def p_lexParametro_token(p):
    "lexParametro : lexToken"
def p_lexParametro_regra(p):
    "lexParametro : lexRegra"


def p_lexToken(p):
    "lexToken : TOKENID '=' '(' ER lexTokenOp"


def p_lexTokenOp_close(p):
    "lexTokenOp : ')'"
def p_lexTokenOp_rec(p):
    "lexTokenOp : ',' tokenFunc ')'"


def p_tokenFunc_string(p):
    "tokenFunc : FSTR"
def p_tokenFunc_int(p):
    "tokenFunc : FINT"
def p_tokenFunc_float(p):
    "tokenFunc : FFLOAT"
def p_tokenFunc_double(p):
    "tokenFunc : FDOUBLE"


def p_lexRegra_ignore(p):
    "lexRegra : lexIgnore"
def p_lexRegra_literals(p):
    "lexRegra : lexLiterals"
def p_lexRegra_error(p):
    "lexRegra : comError"
def p_lexRegra_tokenEnd(p):
    "lexRegra : TOKENEND"


def p_lexIgnore(p):
    "lexIgnore : LEXIGNORE '=' STRING"


def p_lexLiterals(p):
    "lexLiterals : LEXLITERALS '=' STRING"


def p_comError(p):
    "comError : COMERROR '=' '(' STRING comErrorOP"


def p_comErrorOP_close(p):
    "comErrorOP : ')'"
def p_comErrorOP_rec(p):
    "comErrorOP : ',' skipOps ')'"


def p_skipOps_skip(p):
    "skipOps : SKIP"
def p_skipOps_noskip(p):
    "skipOps : NOSKIP"





def p_yacc(p):
    "yacc : yaccParametros"


def p_yaccParametros_single(p):
    "yaccParametros : yaccParametro"
def p_yaccParametros_multi(p):
    "yaccParametros : yaccParametros yaccParametro"


def p_yaccParametro_var(p):
    "yaccParametro : yaccVar"
def p_yaccParametro_regra(p):
    "yaccParametro : yaccRegra"
def p_yaccParametro_gram(p):
    "yaccParametro : yaccGram"


def p_yaccRegra_error(p):
    "yaccRegra : comError"
def p_yaccRegra_precedence(p):
    "yaccRegra : yaccPrecedence"


def p_yaccPrecedence(p):
    "yaccPrecedence : YACCPRECEDENCE '=' '(' yaccPreTuplos ')'"


def p_PreTuplos_single(p):
    "yaccPreTuplos : yaccPreTuplo"
def p_PreTuplos_multi(p):
    "yaccPreTuplos : yaccPreTuplos ',' yaccPreTuplo"


def p_PreTuplo(p):
    "yaccPreTuplo : '(' STRING ',' STRING yaccPreTuploOP"


def p_yaccPreTuploOP_close(p):
    "yaccPreTuploOP : ')'"
def p_yaccPreTuploOP_rec(p):
    "yaccPreTuploOP : ',' STRING yaccPreTuploOP"


def p_yaccVar(p):
    "yaccVar : YACCVAR YACCVALUE"


def p_yaccGram(p):
    "yaccGram : YACCGRAM YACCGRAMVALUE yaccGramOp"


def p_yaccGramOp_empty(p):
    "yaccGramOp : "
def p_yaccGramOp_com(p):
    "yaccGramOp : YACCGRAMCOM"


def p_error(p):
    print("Parser Error",p.value[0])
    print(str(p))

def getParser():
    lexer = getLexer()
    parser = yacc.yacc()
    return parser