import re


def validFunction(function):
    function = str(function.lower())
    allFunc = ["count","sum","media","min","prod","max","min"]
    return allFunc.__contains__(function)

def readFirstLine(lexer):
    res = []
    count = 0
    typeRead = "none"

    for tok in lexer:
        dic = {}
        if (tok.type == "KEY"):
            dic["KEY"] = tok.value        
            res.append(dic)
            count += 1
        else:
            if typeRead == "none":
                raise Exception("Missing KEY value in column: "+str(tok.lexpos+1))
            elif tok.type == "MIN" and typeRead != "KEY":
                raise Exception("Missing KEY value in column: "+str(tok.lexpos+1))
            elif tok.type == "MAX" and typeRead != "MIN":
                raise Exception("Missing MIN value in column: "+str(tok.lexpos+1))
            elif tok.type == "FUNC" and (typeRead != "MIN" and typeRead != "MAX"):
                raise Exception("Missing interval value in column: "+str(tok.lexpos+1))
            elif tok.type == "FUNC" and not validFunction(str(tok.value)):
                raise Exception("Unknown Function: "+str(tok.value))
            else:
                dic = res[count-1]
                dic[tok.type] = tok.value
                res[count-1] = dic

        typeRead = tok.type

    return res


def applyFunc(func,numList):
    funcL = func.lower()

    if funcL == "count":
        return len(numList)

    elif funcL == "sum":
        return sum(numList)

    elif funcL == "media" or funcL == "avg":
        n = len(numList)
        total = sum(numList)
        if n == 0:
            return 0
        return total/n

    elif funcL == "prod":
        res = 1
        for i in numList:
            res *= i
        return res
    
    elif funcL == "max":
        return max(numList)

    elif funcL == "min":
        return min(numList)

    else:
        raise Exception('Unrecognized function: '+funcL)


def convertNum(num):
    if type(num) == str:
        return num
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
            valList = []

            min = field.get("MIN")
            max = min
            if field.__contains__("MAX"):
                max = field.get("MAX")

            for i in range(max):
                tok = lexer.token()
                if not tok or tok.type == "VIRG":
                    if i < min:
                        if not tok:
                            raise Exception('Missing required field on line:'+str(lexer.linha)) 
                        else:
                            raise Exception('Missing required field on line:'+str(lexer.linha)+' col:'+str(tok.lexpos+1)) 
                elif (tok.type == "STRING") and field.__contains__("FUNC") and (not field.get("FUNC").lower().__eq__("count")):
                    raise Exception('String value on non-string field in line:'+str(lexer.linha)+' col:'+str(tok.lexpos+1)+' -> \x1B[3m'+str(tok.value)+'\x1B[0m') 
                else:
                    valList.append(tok.value)
                    lexer.token()
            
            ##CASO HAJA CAMPO DE FUNCÃO, APLICA-A, SENÃO GRAVA
            if field.__contains__("FUNC"):
                try:
                    func = field.get("FUNC").lower()
                    res[field.get("KEY")+'_'+func] = convertNum(applyFunc(func,valList))
                except Exception:
                    raise
            else:    
                res[field.get("KEY")] = convertNumList(valList)
        
        else:
            tok = lexer.token()
            val = tok.value
            if tok.type == "NUM":
                res[field.get("KEY")] = str(convertNum(val))
            elif tok.type == "VIRG":
                raise Exception('Extra comma detected in line:'+str(lexer.linha)+' col:'+str(tok.lexpos+1)+'\nIf u wish to have a literal comma in a field use quotations. "exam,ple" ')
            else:
                res[field.get("KEY")] = val
            lexer.token()

    return res