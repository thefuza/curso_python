# Problema dos parâmetros mutáveis em funções Python
def adiciona_clientes(nome, lista=None):
    if lista is None:
        lista = []
    lista.append(nome)
    return lista


cliente_1 = adiciona_clientes('luiz')
adiciona_clientes('Joana', cliente_1)
adiciona_clientes('Fernando', cliente_1)
cliente_1.append('Edu')

cliente_2 = adiciona_clientes('Helena')
adiciona_clientes('Maria', cliente_2)

cliente_3 = adiciona_clientes('Moreira')
adiciona_clientes('Vivi', cliente_3)

print(cliente_1)
print(cliente_2)
print(cliente_3)