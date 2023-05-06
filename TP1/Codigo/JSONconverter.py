import re

def convertDicToJSONLine(dic):
    # Converte STRING
    # {'Número': '264', 'Nome': 'Marcelo Sousa', 'Curso': 'Ciência Política', 'Notas_sum': 76}
    dic = str(dic)



    # TROCA PLICAS POR ASPAS ('Chave' -> "Chave")
    # {"Número": "264", "Nome": "Marcelo Sousa", "Curso": "Ciência Política", "Notas_sum": 76}
    dic = re.sub(r'(\'|\")([^\'\"]+)\1',r'"\2"',dic)



    # Converte fim de atributos (no meio) com a identação correta
    # {"Número": "264",
    #             "Nome": "Marcelo Sousa",
    #             "Curso": "Ciência Política",
    #             "Notas_sum": 76}
    dic = re.sub(r'("|\d|]), ',r'\1,\n\t\t',dic)



    # Converte início da entrada com a identação correta
    # {
    #             "Número": "264",
    #             "Nome": "Marcelo Sousa",
    #             "Curso": "Ciência Política",
    #             "Notas_sum": 76}
    dic = re.sub(r'({")',r'\t{\n\t\t"',dic)



    # Converte o último atributo com a identação correta
    # {
    #             "Número": "264",
    #             "Nome": "Marcelo Sousa",
    #             "Curso": "Ciência Política",
    #             "Notas_sum": 76
    # }
    dic = re.sub(r'("|\d|])}',r'\1\n\t}',dic)
    return dic