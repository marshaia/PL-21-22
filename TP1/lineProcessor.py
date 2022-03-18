def readFirstLine(lexer):
    res = []
    count = 0
    for tok in lexer:
        dic = {}
        if (tok.type == "KEY"):
            dic["KEY"] = tok.value        
            res.append(dic)
            count = count + 1
        else:
            dic = res[count-1]
            dic[tok.type] = tok.value
            res[count-1] = dic

    return res


def applyFunc(func,numList):
    func = func.lower()

    if func == "count":
        res = 0
        for i in numList:
            res += 1
        return res

    elif func == "sum":
        res = 0
        for i in numList:
            res += i
        return res

    elif func == "media" or func == "avg":
        n = applyFunc("count",numList)
        sum = applyFunc("sum",numList)
        if n == 0:
            return 0
        return sum/n

    elif func == "prod":
        res = 1
        for i in numList:
            res *= i
        return res

    else:
        raise Exception('Unrecognized function: '+func)


def convertNum(num):
    if int(num) - num == 0:
        return int(num)
    return num

def convertNumList(numList):
    res=[]
    for num in numList:
        res.append(convertNum(num))
    return res
   

def processLine(keyList,lexer):
    res = {}
    for field in keyList:

        #CASO O FIELD CONTENHA 1 OU MAIS ELEMS
        if field.__contains__("MIN"):
            numList = []

            min = field.get("MIN")
            max = min
            if field.__contains__("MAX"):
                max = field.get("MAX")

            for i in range(max):
                tok = lexer.token()
                if not tok or tok.type == "VIRG":
                    if i < min:
                        raise Exception('Missing required number on line:'+str(tok.lineno+1)+' col:'+str(tok.lexpos+1)) 
                elif tok.type == "STRING":
                    raise Exception('String value on non-string field in line:'+str(tok.lineno+1)+' col:'+str(tok.lexpos+1)+' -> \x1B[3m'+str(tok.value)+'\x1B[0m') 
                elif tok.type == "NUM":
                    numList.append(tok.value)
                    lexer.token()
            
            ##CASO HAJA CAMPO DE FUNCÃO, APLICA-A, SENÃO GRAVA
            if field.__contains__("FUNC"):
                try:
                    func = field.get("FUNC").lower()
                    res[field.get("KEY")+'_'+func] = convertNum(applyFunc(func,numList))
                except Exception:
                    raise
            else:    
                res[field.get("KEY")] = convertNumList(numList)
        
        else:
            tok = lexer.token()
            val = tok.value
            if tok.type == "NUM":
                res[field.get("KEY")] = str(convertNum(val))
            else:
                res[field.get("KEY")] = val
            lexer.token()

    return res