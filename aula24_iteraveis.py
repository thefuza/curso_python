# Operadores in e not in
# Strings são iteraveis
# 0 1 2 3 4 5 6
# G a b r i e l
#-7-6-5-4-3-2-1

# nome = 'Gabriel'
# # print(nome[2])
# # print(nome[-4])

# print('el' in nome)
# print('zero' in nome)
# print('zero' not in nome)
# print('el' not in nome)

nome = input(' Digite seu nome: ')
encontrar = input('Digite o que deseja encontrar: ')

if encontrar in nome:
    print(f'{encontrar} está em {nome}')
else: 
    print(f'{encontrar} não está em {nome}')