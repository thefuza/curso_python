# import time
# def contagem_regressiva(numeros):

#     for numero in range(numeros, -1, -1):

#         print(numero)
#         time.sleep(1)
#         if numero == 0:
#             print('BOOOOOOOOOOOOOOOOOOOOOOOOOOM')

# contagem_regressiva(5)

# def maior_numero_lista(lista):
#     maior = max(lista)
#     return maior
#     # maior = lista[0]
        
#     # for numero in lista:
#     #     if numero > maior:
#     #         maior = numero
#     # return maior


# lista_positivo = [2, 5, 7, 9, 6, 0, 5, 4, 0, 10]
# lista_negativos = [-5, -12, -2, -8]

# print(maior_numero_lista(lista_positivo))
# print(maior_numero_lista(lista_negativos))

def formatar_diligência(numero, ano):
    numero_formatado = f'{numero:04d}/{ano}'
    return numero_formatado

print(formatar_diligência(125,2026))
print(formatar_diligência(9,2026))
print(formatar_diligência(1050,2026))
print(formatar_diligência(23,2026))



