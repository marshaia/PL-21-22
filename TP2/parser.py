import ply.yacc as yacc
import re
from lexer import getLexer
from lexer import tokens




def p_prog(p):
    "prog : seccoes"
    #Cria lista de tuplos com os números das linhas dos "blocos" SPLY
    final = []
    for list in p[1]:
        tupl = (list[0],list.pop())
        final.append(tupl)
    p.parser.mycontents["fileIntervals"] = final



def p_seccoes_multi(p):
    "seccoes : seccoes seccao"
    p[0] = p[1] + [p[2]]

def p_seccoes_empty(p):
    "seccoes : "
    p[0] = []



def p_seccao_lex(p):
    "seccao : LEXSTART lex termino"
    p[0] = [p.lineno(1)] + p[3]
def p_seccao_yacc(p):
    "seccao : YACCSTART yacc termino"
    p[0] = [p.lineno(1)] + p[3]


def p_termino_END(p):
    "termino : END"
    p[0] = [p.lineno(1)]
def p_termino_seccao(p):
    "termino : seccao"
    p[0] = p[1]






def p_lex(p):
    "lex : lexParametros"


def p_lexParametros_empty(p):
    "lexParametros : "
def p_lexParametros_multi(p):
    "lexParametros : lexParametros lexParametro"
    p.parser.mycontents["lexRead"] = True


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
    tokenDic = {"nome":p[1], "ER":p[4], "funcao":p[5], "begin":p[6]}
    p.parser.mylex[p[2]]["tokens"].append(tokenDic)
    #Adiciona token à lista final
    if p[1] not in p.parser.mycontents["tokenlist"]:
        p.parser.mycontents["tokenlist"].append(p[1])
        
    
def p_context_empty(p):
    "context : "
    p[0] = "INITIAL"
def p_context_singl(p):
    "context : '(' ID ')'"
    p[0] = p[2]
def p_context_singlNoPar(p):
    "context : ID"
    p[0] = p[1]


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
def p_changeContext_singlNoPar(p):
    "changeContext : CHANGECONTEXT ID"
    p[0] = p[2] 
def p_changeContext_singl(p):
    "changeContext : CHANGECONTEXT '(' ID ')'"
    p[0] = p[3] 


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
        msg = "Parâmetro Error repetido (Lex)"
        if contexto != "INITIAL":
            msg += " no contexto '"+contexto+"'"
        msg += " na linha "+str(p.lineno(1))
        raise Exception(msg)
    #Adição
    if p[1]["mensagem"] != "None":
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
        msg = "Parâmetro Ignore repetido"
        if p[2] != "INITIAL":
            msg += " no contexto '"+p[2]+"'" 
        msg += " na linha "+str(p.lineno(1))
        raise Exception(msg)
    #Adição
    p.parser.mylex[p[2]]["ignore"] = p[4]
    p.parser.mylex[p[2]]["ignoreRead"] = True


def p_lexLiterals(p):
    "lexLiterals : LEXLITERALS context '=' STRING"
    #Verifica se o Literals não é repetido
    if p.parser.mycontents["literalsRead"]:
        raise Exception("Parâmetro Literals repetido na linha "+str(p.lineno(1)))
    #Adição
    p.parser.mycontents["literals"] = p[4]
    p.parser.mycontents["literalsRead"] = True
    #Adição à lista de literais
    for chr in p[4]:
        if chr not in p.parser.mycontents["literalslist"]:
            p.parser.mycontents["literalslist"].append(chr)


def p_lexContexts(p):
    "lexContexts : LEXCONTEXT '=' '(' lexContexTuplos ')'"
    #Verifica duplicação de contextos
    if p.parser.mycontents["lexContextRead"]:
        raise Exception("Parâmetro Contexts repetido na linha "+str(p.lineno(1)))
    p.parser.mycontents["lexContextRead"] = True


def p_lexContexTuplos_singl(p):
    "lexContexTuplos : lexContexTuplo"
def p_lexContexTuplos_multi(p):
    "lexContexTuplos : lexContexTuplos ',' lexContexTuplo"


def p_lexContexTuplo(p):
    "lexContexTuplo : '(' STRING ',' STRING ')'"
    nomeCont = p[2].strip("\"\'")
    tipoCont = p[4].strip("\"\'")
    #Verifica tipo de contexto
    if tipoCont != "exclusive" and tipoCont != "inclusive":
        raise Exception("Tipo de contexto inválido no contexto '"+nomeCont+"' ("+tipoCont+") na linha "+str(p.lineno(4)))
    #Verifica existência do contexto
    if nomeCont not in p.parser.mylex:
        p.parser.mylex[nomeCont] = generateLexContextDic()
    p.parser.mylex[nomeCont]["tipo"] = tipoCont


def p_comError(p):
    "comError : COMERROR context '=' comErrorMessage skipOps"
    error = {"contexto": p[2],"mensagem": p[4],"comando": p[5]}
    p[0] = error



def p_comErrorMessage_empty(p):
    "comErrorMessage : "
    p[0] = "None"
def p_comErrorMessage_singl(p):
    "comErrorMessage : STRING"
    p[0] = p[1].strip("\"")


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
    p.parser.mycontents["yaccRead"] = True


def p_yaccParametro_var(p):
    "yaccParametro : yaccVar"
def p_yaccParametro_regra(p):
    "yaccParametro : yaccRegra"
def p_yaccParametro_gram(p):
    "yaccParametro : yaccProd"


def p_yaccRegra_precedence(p):
    "yaccRegra : yaccPrecedence"
def p_yaccRegra_error(p):
    "yaccRegra : comError"
    #Check Flag
    if p.parser.myyacc["errorRead"]:
        raise Exception("Parâmetro Error repetido (Yacc)")
    #Default value override
    if p[1]["mensagem"] != "None":
        p.parser.myyacc["error"]["mensagem"] = p[1]["mensagem"]
    p.parser.myyacc["error"]["comando"] = p[1]["comando"]
    p.parser.myyacc["errorRead"] = True


def p_yaccPrecedence(p):
    "yaccPrecedence : YACCPRECEDENCE '=' '(' yaccPreTuplos ')'"
    #Check Flag
    if p.parser.myyacc["precedenceRead"]:
        raise Exception("Parâmetro Precedence repetido na linha "+str(p.lineno(1)))
    #Adição
    p.parser.myyacc["precedence"] = p[4]
    p.parser.myyacc["precedenceRead"] = True


def p_PreTuplos_single(p):
    "yaccPreTuplos : yaccPreTuplo"
    p[0] = p[1]
def p_PreTuplos_multi(p):
    "yaccPreTuplos : yaccPreTuplos ',' yaccPreTuplo"
    p[0] = tuple([p[1],p[3]])


def p_PreTuplo(p):
    "yaccPreTuplo : '(' STRING ',' STRING yaccPreTuploOP"
    tipo = p[2].lower().strip("\"'")
    fst = p[4].lower().strip("\"'")
    #Verifica tipagem
    if tipo != "left" and tipo != "right":
        raise Exception("Tipo de precedência inválido ("+p[2]+") na linha "+str(p.lineno(2)))
    p[0] = tuple([tipo,fst] + p[5])


def p_yaccPreTuploOP_close(p):
    "yaccPreTuploOP : ')'"
    p[0] = []
def p_yaccPreTuploOP_rec(p):
    "yaccPreTuploOP : ',' STRING yaccPreTuploOP"
    p[0] = [p[2].strip("\"'")] + p[3]


def p_yaccVar(p):
    "yaccVar : ID '=' VarValue"
    #Verifica repetição
    for var in p.parser.myyacc["variables"]:
        if var[0] == p[1]:
            raise Exception("Nome de variável "+p[1]+" repetido na linha "+str(p.lineno(1)))
    #Adição
    var = (p[1],p[3])
    p.parser.myyacc["variables"].append(var)


def p_VarValue_String(p):
    "VarValue : STRING"
    p[0] = p[1]
def p_VarValue_NumVal(p):
    "VarValue : NUMVAL"
    p[0] = p[1]
def p_VarValue_EmptyList(p):
    "VarValue : EMPTYLIST"
    p[0] = p[1]
def p_VarValue_EmptyDic(p):
    "VarValue : EMPTYDIC"
    p[0] = "{}"


def p_yaccProd(p):
    "yaccProd : ID yaccProdAlias ':' yaccProdValue yaccProdCod"
    #Verifica Producao repetida (nome e alias)
    if p[2] != "":
        for prod in p.parser.myyacc["productions"]:
            if prod["nome"] == p[1] and prod["alias"] == p[2]:
                raise Exception("Duas produções com alias repetido ("+p[1]+"/"+p[2]+") na linha "+str(p.lineno(1)))
    #Incrementa contador da producao
    if p[1] not in p.parser.myyacc["aliascounter"]:
        p.parser.myyacc["aliascounter"][p[1]] = 0
    p.parser.myyacc["aliascounter"][p[1]] += 1
    #Monta e adiciona
    prod={"nome" : p[1],"conteudo" : p[4],"codigo" : p[5]}
    if p[2] != "":
        prod["alias"] = p[2]
    else:
        prod["alias"] = "p"+str(p.parser.myyacc["aliascounter"][p[1]])
    p.parser.myyacc["productions"].append(prod)
    #Adiciona à lista de producoes
    if p[1] not in p.parser.mycontents["prodlist"]:
        p.parser.mycontents["prodlist"].append(p[1])


def p_yaccProdAlias_empty(p):
    "yaccProdAlias : "
    p[0] = ""
def p_yaccProdAlias_singl(p):
    "yaccProdAlias : '(' ID ')'"
    p[0] = p[2]
def p_yaccProdAlias_singlNoPar(p):
    "yaccProdAlias : ID"
    p[0] = p[1]


def p_yaccProdValue_empty(p):
    "yaccProdValue : "
    p[0] = ""
def p_yaccProdValue_singl(p):
    "yaccProdValue : STRING"
    p[0] = p[1].strip("\"")


def p_yaccProdCod_empty(p):
    "yaccProdCod : "
    p[0] = ""
def p_yaccProdCod_singl(p):
    "yaccProdCod : CODIGO"
    code = p[1]
    if code != "":
        code = code.strip("}{\n\t ")
        code = re.sub(r';',r'\n',code)
        code = re.sub(r'\n',r'\n\t',code)
    p[0] = code


def p_error(p):
    raise Exception("Erro Sintático: '"+p.value+"' na linha "+str(p.lineno))





#####---------------------PARSER TERMINADO--------------

# parser.mylex = {
#     ["contexto"] = {
#         ["tipo"] = "inclusive"
#         ["tokens"] = [{
#             ["nome"] = "INT"
#             ["ER"] = "r'\d+'"
#             ["funcao"] = "int"
#             ["begin"] = "banana"
#         }]
#         ["ignore"] = "blabla"
#         ["ignoreRead"] = False
#         ["error"] = {
#             ["mensagem"] = "Olá"
#             ["comando"] = "skip"
#         }
#         ["errorRead"] = False
#     }
# }
def generateLexContextDic():
    dic = {}
    dic["tipo"] = "None"
    dic["tokens"] = []
    dic["ignore"] = ""
    dic["ignoreRead"] = False
    error = {"mensagem":"Erro léxico","comando":"skip"}
    dic["error"] = error
    dic["errorRead"] = False
    return dic


# parser.myyacc = {
#     ["precedence"] = "(...)"
#     ["precedenceRead"] = False
#     ["variables"] = [("VarName",Val),...]
#     ["productions"] = [{
#         ["nome"] = "comandos"
#         ["alias"] = "rec"
#         ["conteudo"] = "comandos comando ;"
#         ["codigo"] = "Olá\n\tAdeus"
#     }]
#     ["error"] = {
#         ["mensagem"] = "Olá"
#         ["comando"] = "skip"
#     }
#     ["errorRead"] = False
#     ["aliascounter"] = {
#         ["prodname"] = 1
#         ["prodname"] = 3
#     }
# }
def generateYaccDefaultDic():
    dic = {}
    dic["precedence"] = ""
    dic["precedenceRead"] = False
    dic["variables"] = []
    dic["productions"] = []
    error = {"mensagem":"Erro Sintático","comando":"skip"}
    dic["error"] = error
    dic["errorRead"] = False
    dic["aliascounter"] = {}
    return dic


# parser.mycontents = {
#     ["tokenlist"] = []
#     ["literals"] = ""
#     ["literalslist"] = []
#     ["literalsRead"] = False
#     ["lexContextRead"] = False
#     ["lexRead"] = False
#     ["yaccRead"] = False    
#     ["prodlist"] = []
#     ["fileIntervals"] = []
# }
def generateContentDic():
    dic = {}
    dic["tokenlist"] = []
    dic["literals"] = ""
    dic["literalslist"] = []
    dic["literalsRead"] = False
    dic["lexContextRead"] = False
    dic["lexRead"] = False
    dic["yaccRead"] = False    
    dic["prodlist"] = []
    dic["fileIntervals"] = []
    return dic


def getParser():
    parser = yacc.yacc()
    lexer = getLexer()

    parser.mylex = {}
    parser.myyacc = {}

    parser.mycontents = generateContentDic()
    dic = generateLexContextDic()
    dic["tipo"] = "exclusive"
    parser.mylex["INITIAL"] = dic
    parser.myyacc = generateYaccDefaultDic()

    return parser