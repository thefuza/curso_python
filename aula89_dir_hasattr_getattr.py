# dir, hasattr e getattr em Python

string = 'Luiz'
metodo = 'strip'

if hasattr(string, metodo):
    print('Existe Upper')
    print(getattr(string, metodo)())
else:
    print('Não existe o metodo', metodo )