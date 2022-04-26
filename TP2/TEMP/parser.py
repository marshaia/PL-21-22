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
    p.parser.mylexRead = True


def p_lexParametro_token(p):
    "lexParametro : lexToken"
def p_lexParametro_regra(p):
    "lexParametro : lexRegra"


def p_lexToken(p):
    "lexToken :  ID context '=' ER tokenFunc changeContext"
    #Verifica existência do contexto
    if p[2] not in p.parser.mylex:
        p.parser.mylex[p[2]] = generateLexContextDic()
    #Verifica se o Token não é repetido nesse contexto
    for tokDic in p.parser.mylex[p[2]]["tokens"]:
        if p[1] == tokDic["nome"]:
            msg = "Token "+p[1]+" repetido"
            if p[2] != "INITIAL":
                msg += " no contexto "+p[2] 
            raise Exception(msg)
    #Adição à lista
    tokenDic = {}
    tokenDic["nome"] = p[1]
    tokenDic["ER"] = p[4]
    tokenDic["funcao"] = p[5]
    tokenDic["begin"] = p[6] 
    p.parser.mylex[p[2]]["tokens"].append(tokenDic)
        
    
    
    # for toks in p.parser.myTokens:
    #     if toks.get("TokenName") == p[1]:
    #         raise Exception("Token repetido: "+str(p[1]))
    # tok = {}
    # tok["TokenName"] = p[1]
    # tok["ER"] = p[4]
    # tok["Func"] = p[5]
    # p.parser.myTokens.append(tok)

def p_context_empty(p):
    "context : "
    p[0] = "INITIAL"
def p_context_singl(p):
    "context : '(' ID ')'"
    p[0] = p[2]


def p_tokenFunc_empty(p):
    "tokenFunc : "
    p[0] = "None"
def p_tokenFunc_string(p):
    "tokenFunc : FSTR"
    p[0] = str(p[1]).strip("%").lower()
def p_tokenFunc_int(p):
    "tokenFunc : FINT"
    p[0] = str(p[1]).strip("%").lower()
def p_tokenFunc_float(p):
    "tokenFunc : FFLOAT"
    p[0] = str(p[1]).strip("%").lower()


def p_changeContext_empty(p):
    "changeContext : "
    p[0] = ""
def p_changeContext_singl(p):
    "changeContext : CHANGECONTEXT ID" 
    p[0] = p[2] 


def p_lexRegra_ignore(p):
    "lexRegra : lexIgnore"
def p_lexRegra_literals(p):
    "lexRegra : lexLiterals"
def p_lexRegra_contexts(p):
    "lexRegra : lexContexts"
def p_lexRegra_error(p):
    "lexRegra : comError"
    contexto = p[1]["contexto"]
    #Verifica existência do contexto
    if contexto not in p.parser.mylex:
        p.parser.mylex[contexto] = generateLexContextDic()
    #Verifica se o Ignore não é repetido nesse contexto
    if p.parser.mylex[contexto]["errorRead"]:
        msg = "Parâmetro Error repetido "
        if contexto != "INITIAL":
            msg += " no contexto "+contexto
        raise Exception(msg)
    #Adição
    p.parser.mylex[contexto]["error"]["mensagem"] = p[1]["mensagem"]
    p.parser.mylex[contexto]["error"]["comando"] = p[1]["comando"]
    p.parser.mylex[contexto]["errorRead"] = True


def p_lexIgnore(p):
    "lexIgnore : LEXIGNORE context '=' STRING"
    #Verifica existência do contexto
    if p[2] not in p.parser.mylex:
        p.parser.mylex[p[2]] = generateLexContextDic()
    #Verifica se o Ignore não é repetido nesse contexto
    if p.parser.mylex[p[2]]["ignoreRead"]:
        msg = "Parâmetro Ignore repetido "
        if p[2] != "INITIAL":
            msg += " no contexto "+p[2] 
        raise Exception(msg)
    #Adição
    p.parser.mylex[p[2]]["ignore"] = p[4]
    p.parser.mylex[p[2]]["ignoreRead"] = True


def p_lexLiterals(p):
    "lexLiterals : LEXLITERALS context '=' STRING"
    #Verifica existência do contexto
    if p[2] not in p.parser.mylex:
        p.parser.mylex[p[2]] = generateLexContextDic()
    #Verifica se o Literals não é repetido nesse contexto
    if p.parser.mylex[p[2]]["literalsRead"]:
        msg = "Parâmetro Literals repetido "
        if p[2] != "INITIAL":
            msg += " no contexto "+p[2] 
        raise Exception(msg)
    #Adição
    p.parser.mylex[p[2]]["literals"] = p[4]
    p.parser.mylex[p[2]]["literalsRead"] = True


def p_lexContexts(p):
    "lexContexts : LEXCONTEXT '=' '[' lexContexTuplos ']'"
    #Verifica duplicação de contextos
    if p.parser.mylexContextRead:
        raise Exception("Parâmetro Contexts repetido")
    p.parser.mylexContextRead = True


def p_lexContexTuplos_singl(p):
    "lexContexTuplos : lexContexTuplo"
def p_lexContexTuplos_multi(p):
    "lexContexTuplos : lexContexTuplos ',' lexContexTuplo"


def p_lexContexTuplo(p):
    "lexContexTuplo : '(' ID ',' ID ')'"
    #Verifica tipo de contexto
    if p[4] != "exclusive" and p[4] != "inclusive":
        raise Exception("Tipo de contexto inválido no contexto "+p[2]+" ("+p[4]+")")
    #Verifica existência do contexto
    if p[2] not in p.parser.mylex:
        p.parser.mylex[p[2]] = generateLexContextDic()
    p.parser.mylex[p[2]]["tipo"] = p[4]


def p_comError(p):
    "comError : COMERROR context '=' comErrorMessage skipOps"
    error = {}
    error["contexto"] = p[2]
    error["mensagem"] = p[4].strip("\"")
    error["comando"] = p[5]
    p[0] = error



def p_comErrorMessage_empty(p):
    "comErrorMessage : "
    p[0] = "None"
def p_comErrorMessage_singl(p):
    "comErrorMessage : STRING"
    p[0] = p[1]


def p_skipOps_skip(p):
    "skipOps : SKIP"
    p[0] = p[1].strip("%").lower()
def p_skipOps_noskip(p):
    "skipOps : NOSKIP"
    p[0] = p[1].strip("%").lower()





def p_yacc(p):
    "yacc : yaccParametros"


def p_yaccParametros_empty(p):
    "yaccParametros : "
def p_yaccParametros_multi(p):
    "yaccParametros : yaccParametros yaccParametro"
    p.parser.myyaccRead = True


def p_yaccParametro_var(p):
    "yaccParametro : yaccVar"
def p_yaccParametro_regra(p):
    "yaccParametro : yaccRegra"
def p_yaccParametro_gram(p):
    "yaccParametro : yaccProd"


def p_yaccRegra_error(p):
    "yaccRegra : comError"
    # if p.parser.myReadYaccError:
    #     raise Exception("Yacc Error rule duplicated")
    # p.parser.myYaccError = p[1]
    # p.parser.myReadYaccError = True
def p_yaccRegra_precedence(p):
    "yaccRegra : yaccPrecedence"


def p_yaccPrecedence(p):
    "yaccPrecedence : YACCPRECEDENCE '=' '(' yaccPreTuplos ')'"
    # if p.parser.myReadPrecedence:
    #     raise Exception("Precedence rule duplicated on line "+str(p.lexer.lineno))
    # finalList = []
    # for elem in p[4]:
    #     finalList.append(tuple(elem))
    # p.parser.myPrecedence = tuple(finalList)
    # p.parser.myReadPrecedence = True

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
    "yaccVar : ID '=' VarValue"
    # for vars in p.parser.myVariables:
    #     if vars.get("VarName") == p[1]:
    #         raise Exception("Variável repetida: "+str(p[1]))
    # var = {}
    # var["VarName"] = p[1]
    # var["Value"] = p[2]
    # p.parser.myVariables.append(var)


def p_VarValue_String(p):
    "VarValue : STRING"
def p_VarValue_NumVal(p):
    "VarValue : NUMVAL"
def p_VarValue_EmptyList(p):
    "VarValue : EMPTYLIST"
def p_VarValue_EmptyDic(p):
    "VarValue : EMPTYDIC"


def p_yaccProd(p):
    "yaccProd : ID yaccProdAlias ':' yaccProdValue yaccProdCod"
    # prod = {}
    # prod["ProdName"] = p[1] 
    # if p[2] == "$empty":
    #     prod["Value"] = ""
    # else:
    #     prod["Value"] = p[2]
    # prod["Code"] = p[3]

    # p.parser.myProductions.append(prod)


def p_yaccProdAlias_empty(p):
    "yaccProdAlias : "
def p_yaccProdAlias_singl(p):
    "yaccProdAlias : '(' ID ')'"


def p_yaccProdValue_empty(p):
    "yaccProdValue : "
def p_yaccProdValue_singl(p):
    "yaccProdValue : STRING"


def p_yaccProdCod_empty(p):
    "yaccProdCod : "
def p_yaccProdCod_singl(p):
    "yaccProdCod : CODIGO"




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

def generateLexContextDic():
    dic = {}
    dic["tipo"] = "None"
    dic["tokens"] = []
    dic["literals"] = ""
    dic["literalsRead"] = False
    dic["ignore"] = ""
    dic["ignoreRead"] = False
    error = {}
    error["mensagem"] = "Erro léxico"
    error["comando"] = "skip"
    dic["error"] = error
    dic["errorRead"] = False
    return dic

# parser.mylex = {
#     ["contexto"] = {
#         ["tipo"] = "inclusive"
#         ["tokens"] = [{
#             ["nome"] = "INT"
#             ["ER"] = "r'\d+'"
#             ["funcao"] = "int"
#             ["begin"] = "banana"
#         }]
#         ["literals"] = "blabla"
#         ["literalsRead"] = False
#         ["ignore"] = "blabla"
#         ["ignoreRead"] = False
#         ["error"] = {
#             ["mensagem"] = "Olá"
#             ["comando"] = "skip"
#         }
#         ["errorRead"] = False
#     }
# }


def setVariables(parser):
    parser.myPrecedence = []
    parser.myVariables = []
    parser.myProductions = []
    parser.myYaccError = {}
    parser.myYaccError["Mensagem"] = "Erro Gramático"
    parser.myYaccError["Comando"] = 'skip'
    parser.myReadPrecedence = False
    parser.myReadYaccError = False

def getParser():
    parser = yacc.yacc()
    lexer = getLexer()
    parser.mylex = {}
    parser.myyacc = {}
    parser.mylexRead = False
    parser.myyaccRead = False
    parser.mylexContextRead = False
    dic = generateLexContextDic()
    dic["tipo"] = "exclusive"
    parser.mylex["INITIAL"] = dic
    return parser