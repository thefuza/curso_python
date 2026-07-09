# Funções decoradoras e decoradores
# Decorar = Adcionar / Remover / Restringir / Alterar
# Funções decoradoras são funções que decoram outras funções
# Decoradores são usados para fazer o python
# usar as funções decoradoras em outras funções.
# Decoradores são 'Syntax Sugar" (Açucar Sintatico)

def criar_funcao(func):
    def interna(*args, **kwargs):
        for arg in args:
            print('Vou te decorar')
            is_string(arg)
        resultado = func(*args, **kwargs)
        print(f'O seu resultado foi {resultado}')
        print('OK, AGORA VOCÊ FOI DECORADA')
        return resultado
    return interna 

@criar_funcao
def inverte_string(string):
    return string[::-1]

def is_string(param):
    if not isinstance(param, str):
        raise TypeError ('parametro deve ser uma string')
    

invertida = inverte_string('123')
print(invertida)