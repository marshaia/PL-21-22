import re



# Método que valida a função de agregação presente no ficheiro de input
# ao confirmar a sua presença na lista de funções disponíveis no programa.
def validFunction(function):
    function = str(function.lower())
    allFunc = ["count","sum","media","min","prod","max","min"]
    return allFunc.__contains__(function)



# Método responsável pela leitura e interpretação do cabeçalho do ficheiro de input.
def readFirstLine(lexer):
    res = []    # Lista de armazenamento das informações dos vários campos (Lista de chaves)
    count = 0
    typeRead = "none" # Variável auxiliar para verificar o token lido anteriormente

    for tok in lexer:
        dic = {} # Cria um dicionário para cada campo para armazenar as suas informações

        if (tok.type == "KEY"):     # Se for uma chave vai criar uma nova entrada no dicionário
            dic["KEY"] = tok.value  # e coloca-o na lista de chaves      
            res.append(dic)
            count += 1
        else:
            if typeRead == "none": # Se ler qualquer token sem ter lido nenhuma KEY antes
                raise Exception("Missing KEY value in column: "+str(tok.lexpos+1))

            elif tok.type == "MIN" and typeRead != "KEY": # Se ler um mínimo sem ter lido uma KEY antes
                raise Exception("Missing KEY value in column: "+str(tok.lexpos+1))

            elif tok.type == "MAX" and typeRead != "MIN": # Se ler um máximo sem ter lido um mínimo
                raise Exception("Missing MIN value in column: "+str(tok.lexpos+1))

            elif tok.type == "FUNC" and (typeRead != "MIN" and typeRead != "MAX"): # Se leu uma função sem ter nenhuma lista para aplicar no campo
                raise Exception("Missing interval value in column: "+str(tok.lexpos+1))

            elif tok.type == "FUNC" and not validFunction(str(tok.value)): # Se leu uma função não válida no campo
                raise Exception("Unknown Function: "+str(tok.value))

            else: # Caso contrário adiciona a nova informação ao dicionário do campo respetivo
                dic = res[count-1]
                dic[tok.type] = tok.value
                res[count-1] = dic

        typeRead = tok.type     # Atualiza a variável do tipo lido

    return res



# Método que aplica a função do campo aos seus elementos (lista) 
def applyFunc(func,numList):
    funcL = func.lower()

    if funcL == "count":    # Aplica a função de count
        return len(numList)

    elif funcL == "sum":    # Aplica a função de soma
        return sum(numList)

    elif funcL == "media" or funcL == "avg": # Aplica a função de média
        n = len(numList)
        total = sum(numList)
        if n == 0:
            return 0
        return total/n

    elif funcL == "prod":   # Aplica a função de produtório
        res = 1
        for i in numList:
            res *= i
        return res
    
    elif funcL == "max":    # Aplica a função de máximo
        return max(numList)

    elif funcL == "min":    # Aplica a função de mínimo
        return min(numList)

    else: # Caso a função não seja reconhecida
        raise Exception('Unrecognized function: '+funcL)



# Método que converte floats em inteiros (caso estes não contenham casas decimais)
def convertNum(num):
    if type(num) == str:    # Se for uma string, devolve como tal
        return num
    if int(num) - num == 0: # Se for um float sem casas decimais, devolve como inteiro
        return int(num)
    return num              # Caso contrário devolve em formato float


# Método que converte uma lista de elementos em números
def convertNumList(numList):
    res=[]
    for num in numList:
        res.append(convertNum(num))
    return res
   



# Método que processa uma linha do conteúdo do ficheiro input através da informação
# do cabeçalho e dos tokens da linguagem
def processLine(keyList,lexer):
    res = {}
    for field in keyList:

        #CASO O FIELD/CHAVE CONTENHA RESTRIÇÕES ADICIONAIS
        if field.__contains__("MIN"):
            valList = []

            #CASO O FIELD NÃO CONTENHA MAX DEFINE MAX = MIN
            min = field.get("MIN")
            max = min
            if field.__contains__("MAX"):
                max = field.get("MAX")

            #EFETUA A LEITURA DE VÁRIOS CAMPOS ATÉ MAX
            for i in range(max):
                tok = lexer.token()
                #CASO CHEGOU AO FIM DA LINHA OU LEU VÍRGULA DUPLICADA
                if not tok or tok.type == "VIRG":
                    #CASO NÃO TENHA LIDO O NÚMERO MÍNIMO DE ELEMENTOS, DÁ ERRO, SENÃO IGNORA
                    if i < min:
                        if not tok:
                            raise Exception('Missing required field on line:'+str(lexer.linha)) 
                        else:
                            raise Exception('Missing required field on line:'+str(lexer.linha)+' col:'+str(tok.lexpos+1))
                #CASO TENHA LIDO UMA STRING NUM CAMPO QUE CONTÊM UMA FUNÇÃO DE AGREGAÇÃO NÚMERICA, DÁ ERRO 
                elif (tok.type == "STRING") and field.__contains__("FUNC") and (not field.get("FUNC").lower().__eq__("count")):
                    raise Exception('String value on non-string field in line:'+str(lexer.linha)+' col:'+str(tok.lexpos+1)+' -> \x1B[3m'+str(tok.value)+'\x1B[0m') 
                #CASO OK, ADICONA O CAMPO À LISTA
                else:
                    valList.append(tok.value)
                    lexer.token()
            
            #CASO HAJA CAMPO DE FUNCÃO, APLICA-A, SENÃO GRAVA COMO LISTA
            if field.__contains__("FUNC"):
                try:
                    func = field.get("FUNC").lower()
                    res[field.get("KEY")+'_'+func] = convertNum(applyFunc(func,valList))
                except Exception:
                    raise
            else:    
                res[field.get("KEY")] = convertNumList(valList)
        
        #CASO O FIELD/CHAVE SEJA UMA CHAVE SIMPLES, APENAS LÊ O CAMPO
        else:
            tok = lexer.token()
            if not tok:
                raise Exception('Empty field detected at the end of line:'+str(lexer.linha))
            elif tok.type == "VIRG":
                raise Exception('Empty field detected in line:'+str(lexer.linha)+' col:'+str(tok.lexpos+1))
            
            val = tok.value
            if tok.type == "NUM":
                res[field.get("KEY")] = str(convertNum(val))
            else:
                res[field.get("KEY")] = val
            lexer.token()

    return res