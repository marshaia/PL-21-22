import ply.yacc as yacc
from lexer import getLexer
from lexer import tokens



def p_prog(p):
    "prog : contextos"


def p_contextos_singl(p):
    "contextos : contexto END"
def p_contextos_multi(p):
    "contextos : contextos contexto END"


def p_contexto_lex(p):
    "contexto : LEXSTART lex"
def p_contexto_yacc(p):
    "contexto : YACCSTART yacc"


def p_lex(p):
    "lex : lexParametros"


def p_lexParametros_empty(p):
    "lexParametros : "
def p_lexParametros_multi(p):
    "lexParametros : lexParametros lexParametro"


def p_lexParametro_token(p):
    "lexParametro : lexToken"
def p_lexParametro_regra(p):
    "lexParametro : lexRegra"


def p_lexToken(p):
    "lexToken : TOKENID '=' '(' ER lexTokenOp"
    for toks in p.parser.myTokens:
        if toks.get("TokenName") == p[1]:
            raise Exception("Token repetido: "+str(p[1]))
    tok = {}
    tok["TokenName"] = p[1]
    tok["ER"] = p[4]
    tok["Func"] = p[5]
    p.parser.myTokens.append(tok)
    


def p_lexTokenOp_close(p):
    "lexTokenOp : ')'"
    p[0] = "str"
def p_lexTokenOp_rec(p):
    "lexTokenOp : ',' tokenFunc ')'"
    p[0] = p[2]


def p_tokenFunc_string(p):
    "tokenFunc : FSTR"
    p[0] = p[1]
def p_tokenFunc_int(p):
    "tokenFunc : FINT"
    p[0] = p[1]
def p_tokenFunc_float(p):
    "tokenFunc : FFLOAT"
    p[0] = p[1]
def p_tokenFunc_double(p):
    "tokenFunc : FDOUBLE"
    p[0] = p[1]


def p_lexRegra_ignore(p):
    "lexRegra : lexIgnore"
def p_lexRegra_literals(p):
    "lexRegra : lexLiterals"
def p_lexRegra_error(p):
    "lexRegra : comError"
    if p.parser.myReadLexError:
        raise Exception("Lex Error rule duplicated")
    p.parser.myLexError = p[1]
    p.parser.myReadLexError = True


def p_lexIgnore(p):
    "lexIgnore : LEXIGNORE '=' STRING"
    if p.parser.myReadIgnore:
        raise Exception("Ignore rule duplicated")
    p.parser.myIgnore = p[3]
    p.parser.myReadIgnore = True


def p_lexLiterals(p):
    "lexLiterals : LEXLITERALS '=' STRING"
    if p.parser.myReadLiterals:
        raise Exception("Literals rule duplicated")
    p.parser.myLiterals = p[3]
    p.parser.myReadLiterals = True


def p_comError(p):
    "comError : COMERROR '=' '(' STRING comErrorOP"
    error = {}
    error["Mensagem"] = p[4]
    error["Comando"] = p[5]
    p[0] = error



def p_comErrorOP_close(p):
    "comErrorOP : ')'"
    p[0] = "skip"
def p_comErrorOP_rec(p):
    "comErrorOP : ',' skipOps ')'"
    p[0] = p[2]


def p_skipOps_skip(p):
    "skipOps : SKIP"
    p[0] = p[1]
def p_skipOps_noskip(p):
    "skipOps : NOSKIP"
    p[0] = p[1]





def p_yacc(p):
    "yacc : yaccParametros"


def p_yaccParametros_empty(p):
    "yaccParametros : "
def p_yaccParametros_multi(p):
    "yaccParametros : yaccParametros yaccParametro"


def p_yaccParametro_var(p):
    "yaccParametro : yaccVar"
def p_yaccParametro_regra(p):
    "yaccParametro : yaccRegra"
def p_yaccParametro_gram(p):
    "yaccParametro : yaccProd"


def p_yaccRegra_error(p):
    "yaccRegra : comError"
    if p.parser.myReadYaccError:
        raise Exception("Yacc Error rule duplicated")
    p.parser.myYaccError = p[1]
    p.parser.myReadYaccError = True
def p_yaccRegra_precedence(p):
    "yaccRegra : yaccPrecedence"


def p_yaccPrecedence(p):
    "yaccPrecedence : YACCPRECEDENCE '=' '(' yaccPreTuplos ')'"
    if p.parser.myReadPrecedence:
        raise Exception("Precedence rule duplicated")
    finalList = []
    for elem in p[4]:
        finalList.append(tuple(elem))
    p.parser.myPrecedence = tuple(finalList)
    p.parser.myReadPrecedence = True

def p_PreTuplos_single(p):
    "yaccPreTuplos : yaccPreTuplo"
    p[0] = p[1]
def p_PreTuplos_multi(p):
    "yaccPreTuplos : yaccPreTuplos ',' yaccPreTuplo"
    p[0] = [p[1],p[3]]


def p_PreTuplo(p):
    "yaccPreTuplo : '(' STRING ',' STRING yaccPreTuploOP"
    p[0] = joinLists([p[2],p[4]],p[5])


def p_yaccPreTuploOP_close(p):
    "yaccPreTuploOP : ')'"
    p[0] = []
def p_yaccPreTuploOP_rec(p):
    "yaccPreTuploOP : ',' STRING yaccPreTuploOP"
    p[0] = joinLists([p[2]],p[3])


def p_yaccVar(p):
    "yaccVar : YACCVAR YACCVALUE"
    for vars in p.parser.myVariables:
        if vars.get("VarName") == p[1]:
            raise Exception("Variável repetida: "+str(p[1]))
    var = {}
    var["VarName"] = p[1]
    var["Value"] = p[2]
    p.parser.myVariables.append(var)


def p_yaccProd(p):
    "yaccProd : YACCPROD YACCPRODVALUE yaccProdOp"
    prod = {}
    prod["ProdName"] = p[1] 
    if p[2] == "$empty":
        prod["Value"] = ""
    else:
        prod["Value"] = p[2]
    prod["Code"] = p[3]

    p.parser.myProductions.append(prod)


def p_yaccProdOp_empty(p):
    "yaccProdOp : "
    p[0] = ""
def p_yaccProdOp_com(p):
    "yaccProdOp : YACCPRODCOM"
    p[0] = p[1]


def p_error(p):
    print("Parser Error",p.value[0])
    print(str(p))


def joinLists(l1,l2):
    final = []
    for elem in l1:
        final.append(elem)
    for elem in l2:
        final.append(elem)  
    return final


def setVariables(parser):
    parser.myTokens = []
    parser.myIgnore = ""
    parser.myLiterals = ""
    parser.myLexError = {}
    parser.myLexError["Mensagem"] = "Erro Léxico"
    parser.myLexError["Comando"] = 'skip'
    parser.myReadLiterals = False
    parser.myReadIgnore = False
    parser.myReadLexError = False
    parser.myPrecedence = []
    parser.myVariables = []
    parser.myProductions = []
    parser.myYaccError = {}
    parser.myYaccError["Mensagem"] = "Erro Gramático"
    parser.myYaccError["Comando"] = 'skip'
    parser.myReadPrecedence = False
    parser.myReadYaccError = False
    parser

def getParser():
    parser = yacc.yacc()
    lexer = getLexer()
    setVariables(parser)
    return parser