import json


def readArguments(argv):
    flagList = ["-input","-output","-help","-divide","-debug","-wall","-verbose"]
    arguments = {}
    arguments["-input"] = ""
    arguments["-output"] = ""
    for flag in flagList:
        if flag != "-input" and flag != "-output":
            arguments[flag] = False
    argv.pop(0)
    argslen = len(argv)
    skip = False
    for i in range (0,argslen):

        arg = argv[i].lower()
        
        if skip:
            skip = False

        elif arg[0] == '-':

            if arg not in flagList:
                raise Exception("Opção desconhecida "+str(argv[i]))

            if arg == "-input" or arg == "-output":
                if i+1 >= argslen or argv[i+1][0] == "-":
                    raise Exception("Ficheiro de "+arg.strip("-")+" em falta")
                if arguments[arg] != "":
                    raise Exception("Ficheiro de "+arg.strip("-")+" repetido")
                arguments[arg] = argv[i+1]
                skip = True
            else:
                arguments[arg] = True
                
        else:
            if arguments["-input"] != "":
                    raise Exception("Ficheiro de input repetido")
            arguments["-input"] = argv[i]
    
    if arguments["-input"] == "":
        raise Exception("Ficheiro de input em falta")

    return arguments


def progHelp():
    help = """Help
I helped
Yay"""
    return help

def debugDump(parser):
    print("DEBUG: A descarregar os conteúdos do parser em 'debug.JSON'")
    debugfile = open("debug.JSON","w+")
    json.dump([parser.mylex,parser.myyacc,parser.mycontents],debugfile,indent = 4)
    debugfile.close()


def verifyData(parser,warning):

    if not parser.mycontents["lexRead"]:
        if warning:
            print("WARNING: Nenhum bloco LEX lido, impossível verificar as produções")
        return

    for context in parser.mylex:
        #CHECK Contextos Nulos
        if parser.mylex[context]["tipo"] == "None":
            raise Exception("Contexto '"+str(context)+"' declarado implicitamente mas sem declaração explicita.")

        if parser.mylex[context]["tipo"] == "exclusive":
            #CHECK Regra IGNORE
            if not parser.mylex[context]["ignoreRead"] and warning:
                msg = "WARNING: Parâmetro Ignore em falta"
                if context != "INITIAL":
                    msg += " no contexto exclusivo '"+str(context)+"'"
                msg += ". Valor por defeito utilizado"
                print(msg)

            #CHECK Regra ERROR
            if not parser.mylex[context]["errorRead"] and warning:
                msg = "WARNING: Parâmetro Error em falta (Lex)"
                if context != "INITIAL":
                    msg += " no contexto exclusivo '"+str(context)+"'"
                msg += ". Valor por defeito utilizado"
                print(msg)
    
    #CHECK Termos da produção
    for prod in parser.myyacc["productions"]:
        words = prod["conteudo"].split()
        for word in words:
            word = word.strip("'")
            if (word not in parser.mycontents["tokenlist"]) and (word not in parser.mycontents["literalslist"]) and (word not in parser.mycontents["prodlist"]):
                raise Exception("Termo desconhecido '"+word+"' encontrado na produção -> "+prod["nome"]+" ("+prod["alias"]+") : "+prod["conteudo"])

        #FIX Literals na produção
        conteudo = prod["conteudo"].replace("'","")
        for chr in parser.mycontents["literalslist"]:
            conteudo = conteudo.replace(chr,"'"+chr+"'")
        prod["conteudo"] = conteudo
            
            
    
    
