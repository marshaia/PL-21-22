#--------------------------LEX-----------------------

def strLiterals(parser):
    if not parser.mycontents["literalsRead"]:
        return ""
    return "literals = "+parser.mycontents["literals"]+"\n"


def strTokenList(parser):
    if not parser.mycontents["tokenlist"]:
        return ""
    return "tokens = "+str(parser.mycontents["tokenlist"])+"\n"


def strToken(context,tokenDic):
    msg = "def t_"
    if context != "INITIAL":
        msg += context+"_"
    msg += tokenDic["nome"]+"(t):\n\t"+tokenDic['ER']+"\n\t"
    if tokenDic["funcao"] != "None":
        msg += "t.value = "+tokenDic['funcao']+"(t.value)\n\t"
    if tokenDic["begin"] != "":
        msg += "t.lexer.begin(\""+tokenDic["begin"]+"\")\n\t"
    msg += "return t\n\n"
    return msg


def strContexts(parser):
    if not parser.mycontents["lexContextRead"]:
        return ""
    msg = "states = ("
    for context in parser.mylex:
        if context != "INITIAL":
            tuplo = (context,parser.mylex[context]["tipo"])
            msg += str(tuplo)+",\n\t\t  "
    msg = msg.strip("\n\t\t  ")
    msg += ")"
    return msg


def strLexIgnore(context,contextDic):
    ignore = contextDic["ignore"]
    if ignore == "":
        ignore = "\"\""
    if contextDic["tipo"] == "exclusive":
        if context != "INITIAL":
            return "t_"+context+"_ignore = "+ignore+"\n\n"
        return "t_ignore = "+ignore+"\n\n"
    return ""


def strLexError(context,contextDic):
    if contextDic["tipo"] == "exclusive":
        msg = ""
        if context != "INITIAL":
            msg += "def t_"+context+"_error(t):\n\t"
        else:
            msg += "def t_error(t):\n\t"

        msg += "print(\""+contextDic["error"]["mensagem"]+"\")\n\t"
        
        if contextDic["error"]["comando"] == "skip":
            msg += "t.lexer.skip(1)\n\n"
        else:
            msg += "exit()\n\n"
        return msg

    return ""


def strAllLexContexts(parser):
    msg = "\n"
    for context in parser.mylex:
        msg += "#----- CONTEXT: "+context+" -----\n\n"
        for tok in parser.mylex[context]["tokens"]:
            msg += strToken(context,tok)
        msg += strLexIgnore(context,parser.mylex[context])
        msg += strLexError(context,parser.mylex[context])
        msg += "\n\n"
    return msg


def strAllLex(parser):
    msg = "#--------------------LEX------------------\n\n"
    msg += "import ply.lex as lex\n\n"
    msg += strTokenList(parser)
    msg += strLiterals(parser)
    msg += "\n"
    msg += strContexts(parser)
    msg += "\n"
    msg += strAllLexContexts(parser)
    msg += "lexer = lex.lex()\n\n"
    msg += "#------------------LEX END------------------\n"
    return msg









##---------------------------YACC-------------------

def strPrecedence(parser):
    if parser.myyacc["precedence"] == "":
        return ""
    msg = "precedence = "+str(parser.myyacc["precedence"])+"\n\n"
    return msg


def strVariables(parser):
    msg = ""
    for var in parser.myyacc["variables"]:
        msg += f"parser.{var[0]} = {var[1]}\n"
    return msg


def strProduction(prodDic):
    msg = "def p_"+prodDic["nome"]+"_"+prodDic["alias"]+"(p):\n\t"
    msg += "\""+prodDic["nome"]+" : "+prodDic["conteudo"]+"\"\n\t"
    if prodDic["codigo"] != "":
        msg += prodDic["codigo"]+"\n"
    msg += "\n"
    return msg


def strAllProductions(parser):
    msg = "\n"
    for prod in parser.myyacc["productions"]:
        msg += strProduction(prod)
    return msg


def strYaccError(parser):
    msg = "\ndef p_error(p):\n\t"
    msg += "print(\""+parser.myyacc["error"]["mensagem"]+"\")\n\t"
    if parser.myyacc["error"]["comando"] == "noskip":
        msg += "exit()"
    msg += "\n"
    return msg


def strAllYacc(parser):
    msg = "#--------------------YACC------------------\n\n"
    msg += "import ply.yacc as yacc\n\n"
    msg += strPrecedence(parser)
    msg += strAllProductions(parser)
    msg += strYaccError(parser)
    msg += "\nparser = yacc.yacc()\n\n"
    msg += strVariables(parser)
    msg += "\n#-----------------YACC END------------------\n"
    return msg






def strFinalFile(parser):
    msg = "#------------------- Início da Compilação --------------------\n"
    if parser.mycontents["lexRead"]:
        msg += strAllLex(parser)
    if parser.mycontents["yaccRead"]:
        msg += strAllYacc(parser)
    msg += "#----------------- Compilação Terminada :) ------------------\n"
    return msg