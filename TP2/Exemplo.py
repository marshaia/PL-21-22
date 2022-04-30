import ply.lex as lex
import ply.yacc as yacc


#-------------------- LEX MODULE -------------------

literals = "+-*/()=;"
tokens = ["INT","ID","Print","Read","DUMP"]


def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_ID(t):
	r'[a-zA-Z_]\w*'
	t.value = str(t.value)
	return t

def t_Print(t):
	r'(print|PRINT)'
	t.value = str(t.value)
	return t

def t_Read(t):
	r'(read|READ)'
	t.value = str(t.value)
	return t

def t_DUMP(t):
	r'(dump|DUMP)'
	t.value = str(t.value)
	return t

t_ignore = " \n\t\r"

def t_error(t):
	print("Mensagem de erro")
	t.lexer.skip(1)

#------------------- YACC MODULE --------------------

precedence = (("left", "+"), ("left", "-"))

def p_prog_p1(p):
	"prog : comandos"

def p_comandos_p1(p):
	"comandos : "

def p_comandos_p2(p):
	"comandos : comandos comando ';'"

def p_comando_p1(p):
	"comando : ID '=' exp"
	p.parser.tabelaIDs[p[1]] = p[3]

def p_comando_p2(p):
	"comando : Print exp"
	print(p[2])

def p_comando_p3(p):
	"comando : Read exp"
	r = int(input())
	p.parser.tabelaIDs[p[2]] = r

def p_comando_p4(p):
	"comando : DUMP"
	print(p.parser.tabelaIDs)

def p_exp_p1(p):
	"exp : aexp"
	p[0] = p[1]

def p_aexp_p1(p):
	"aexp : termo"
	p[0] = p[1]

def p_aexp_p2(p):
	"aexp : aexp '+' termo"
	p[0] = p[1] + p[3]

def p_aexp_p3(p):
	"aexp : aexp '-' termo"
	p[0] = p[1] - p[3]

def p_termo_p1(p):
	"termo : fator"
	p[0] = p[1]

def p_termo_p2(p):
	"termo : termo '*' INT"
	p[0] = p[1] * p[3]

def p_termo_p3(p):
	"termo : termo '/' INT"
	p[0] = p[1] / p[3]

def p_fator_p1(p):
	"fator : INT"
	p[0] = p[1]

def p_fator_p2(p):
	"fator : ID"
	getVar()

def p_fator_p3(p):
	"fator : '(' exp ')'"
	p[0] = p[2]

def p_error(p):
	print("Mensagem")
	exit()


parser = yacc.yacc()
parser.ola = "ola"
parser.val = 1
parser.tabelaIDs = {}
parser.lista = [   ]

#Tradução PLY-Simples concluída