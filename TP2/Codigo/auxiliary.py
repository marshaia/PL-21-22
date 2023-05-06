import json
import re
from strFormatter import strFinalFile
from lexer import getTokenList


def readArguments(argv):
    flagList = ["-input","-output","-help","-plyonly","-debug","-wall","-verbose"]
    arguments = {}
    arguments["-input"] = ""
    arguments["-output"] = ""
    #Todas as flags a FALSE
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
                raise Exception("Opção desconhecida "+str(argv[i])+".\nUse a flag -help para mais informação")

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
    
    if arguments["-input"] == "" and not arguments["-help"]:
        raise Exception("Ficheiro de input em falta.\nUse a flag -help para mais informação")

    return arguments




def progHelp():
    help = """
-------------------------------- BEM-VINDO AO SIMPLY! --------------------------------------

Um compilador de linguagem "sply" para Python, de forma a simplificar a escrita de código da biblioteca PLY

Modo de utilização:
$ python simPLY.py [FLAGS]

FLAGS:
-input [nome] -> Ficheiro de input a ser lido. Também pode ser escrito sem a flag.
-ouput [nome] -> Ficheiro de output gerado. Este será sempre um ficheiro do formato .py e não pode ser igual ao ficheiro de input
-help         -> Menu de ajuda
-debug        -> Depois do ficheiro input ser lido e verificado, será criada um ficheiro "debug.JSON" com a informação lida
-wall         -> Aviso de todos os erros possíveis encontrados.
-verbose      -> Escrita no terminal dos vários processos a ocorrer
-plyonly      -> Escrita no ficheiro de output apenas o conteúdo SPLY lido"""
    return help




def debugDump(parser,filename):
    tokens = getTokenList(filename)
    print("DEBUG: A descarregar os conteúdos do parser em 'debug.JSON'")
    debugfile = open("debug.JSON","w+")
    json.dump([parser.mylex,parser.myyacc,parser.mycontents,tokens],debugfile,indent = 4)
    debugfile.close()



def verifyData(parser,warning):

    if not parser.mycontents["lexRead"] and not parser.mycontents["yaccRead"]:
        raise Exception("Ficheiro Input Vazio - Nenhum bloco lido")

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
            
            
    
    
def writeFile(filename,parser,flag,inputfilename):

    foutput = open(filename,"w+")

    if flag:
        foutput.write(strFinalFile(parser))
        foutput.close()
        return
    
    list = parser.mycontents["fileIntervals"]
    intervalList = []
    for l in list:
        intervalList.append(l[0])
        intervalList.append(l[1])
    intervalList.reverse()

    finput = open(inputfilename,"r")
    resultWrite = False
    writeMode = True
    end = False
    lineno = 1
    target = intervalList.pop()

    for line in finput.readlines():

        if (lineno == target) and not end:

            if writeMode:
                writeMode = False
                if not resultWrite:
                    foutput.write(str(strFinalFile(parser)))
                    resultWrite = True
            else: 
                writeMode = True

            if intervalList:
                target = intervalList.pop()
            else:
                end = True
        

        elif writeMode:
            foutput.write(str(line))

        lineno += 1

    finput.close()
    foutput.close()


