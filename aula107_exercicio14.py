# Exercício - Unir lista
# Crie uma função zipper (como o zipper de roupa)
# O trabalho dessa função será unir duas listasna ordem.
# Use todos os valores da menor lista.
# Ex.: 
# ['Salvador', 'Ubatuba', 'Belo Horizonte']
# ['BA', 'SP', 'MG', 'RJ']
# Resultado
#[('Salvador', 'BA'), ('Ubatuba', 'SP'), ('Belo Horizonte', 'MG')]
# def zipper(l1, l2):
#     intervalo = min(len(l1), len(l2))
#     return [
#         (l1[i], l2[i],) for i in range(intervalo)
#     ]

# from itertools import zip_longest

# l1 = ['Salvador', 'Ubatuba', 'Belo Horizonte']
# l2 = ['BA', 'SP', 'MG', 'RJ']
# print(list(zip(l1, l2)))
# print(list(zip_longest(l1, l2, fillvalue='Sem cidade')))

l1 = [1,2,3,4,5,6,7,8]
l2 = [1,2,3,4]
lista_soma = [x + y for x, y in zip(l1, l2)]

print(lista_soma)



# lista_soma = []
# for i in range(len(l2)):
#     lista_soma.append(l1[i] + l2[i])

# print(lista_soma)

# lista_soma = []
# for i, _ in enumerate(l2):
#     lista_soma.append(l1[i] + l2[i])

# print(lista_soma)