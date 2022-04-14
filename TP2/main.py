from lexer import getLexer

f = open("Exemplo.txt","r")
r = f.read()

lexer = getLexer()

lexer.input(r)
for tok in lexer:
    print(tok)