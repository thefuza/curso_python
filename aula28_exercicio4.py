"""
Peça ao usuário para digitar seu nome
Peça ao usuário para digitar sua idade
Se o nome e idade forem digitados
    Exiba:
        Seu nome é: {nome}
        Seu nome invertido é {nome_invertido}
        Seu nome contém (ou não) espaços
        Seu nome contém {n} letras
        A primeira letra do seu nome é {letra}
        A última letra do seu nome é {letra}
Se nada for digitado em nome ou idade
    Exiba:
        "Desculpa, você deixou campos em brancos."
"""
nome = input('Digite seu nome: ')
idade = input('Digite sua idade: ')

if nome and idade:


    print(f'1. Seu nome é: {nome}')
    print(f'2. Seu nome invertido é {nome[::-1]}')
    print(f'3. Seu nome contém {len(nome)} letras')
    print(f'4. A primeira letra do seu nome é {nome[0]}')
    print(f'5. A última letra do seu nome é {nome[-1]}')

    if '' in nome:
        print('6. Seu nome CONTÉM espaços')
    else:
        print('6. Seu nome NÃO CONTÉM espaços')

else:
    print('Desculpe, você deixou campos vazios')
