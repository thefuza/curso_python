"""
Repetições
while (enquanto)
Executa uma ação enquanto uma condição for verdadeira;
Loop infinito -> Quando o código não tem fim

"""
condicao = True


while condicao:
    nome = input('Qual seu nome: ')
    print(f'Seu nome é {nome}')


    if nome == 'sair' or 'Sair':
        break

print('Acabou')