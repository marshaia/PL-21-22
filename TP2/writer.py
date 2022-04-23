import re

def strLiterals(literals):
    return f"literals = {literals}\n"

def strTokenList(tokenList):
    res = "tokens = ["
    first = bool(True)
    for tok in tokenList:
        if not first:
            res += ","
        first = bool(False)
        res += "\""+tok['TokenName']+"\""
    res += "]\n"
    return res

def strAllTokens(tokenlist):
    res = ""
    for tok in tokenlist:
        res += strToken(tok)
        res += "\n"
    return res

def strToken(tokenDic):
    return f"def t_{tokenDic['TokenName']}(t):\n\t{tokenDic['ER']}\n\tt.value = {tokenDic['Func']}(t.value)\n\treturn t\n"

def strIgnore(ignore):
    return f"t_ignore = {ignore}\n"

def strError(error):
    res = f"def t_error(t):\n\tprint({error['Mensagem']})\n\t"
    if error['Comando'] == "skip":
        res += "t.lexer.skip(1)\n"
    else:
        res += "exit()\n"
    return res

def strPrecedence(prec):
    return f"precedence = {prec}\n"

def strVariables(varlist):
    res = ""
    for var in varlist:
        res += f"parser.{var['VarName']} = {var['Value']}\n"
    return res

def strProduction(prod,num):
    res = f"def p_{prod['ProdName']}_p{num}(p):\n\t"
    res += f"\"{prod['ProdName']} : {prod['Value']}\"\n"

    code = prod['Code']
    if not code == "":
        code = code.strip("}{")
        code = re.sub(r';',r'\n',code)
        code = re.sub(r'\n',r'\n\t',code)
        res += "\t"+code+"\n"
    
    return res

def strAllProductions(prodList):
    res = ""
    prodRead = {}
    for prod in prodList:
        name = prod['ProdName']
        
        if prodRead.get(name) != None:
            val = prodRead[name]
            prodRead[name] = val + 1
        else:
            prodRead[name] = 1
        res += strProduction(prod,prodRead[name])
        res += "\n"

    return res
