from lexer import getLexer

f = open("vicSug.txt","r")
r = f.read()

lexer = getLexer()

lexer.input(r)
for tok in lexer:
    print(tok)