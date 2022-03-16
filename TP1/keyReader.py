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