"""
Faça um programa que peça ao usuário para digitar um numero inteiro,
informe se este numero é par ou impar. Caso o usuário não digite um
numero inteiro, informe que não é um número inteiro.
"""
# numero_str = input('Me informe um número: ')


# try:
#     if int(numero_str) % 2 == 0:
#         print('Esté número é par')
#     else:
#         print('Este número é impar')
# except:
#     print('o valor digitado não é um inteiro')


"""
Faça um programa que pergunte a hora ao usuário e, baseando-se no
horário descrito, exiba a saudação apropriada.
Ex.: Bom dia 0-11, Boa tarde 12-17 e Boa noite 18-23
"""
# entrada= input('Que horas são: ')

# try:
#     hora = int(entrada)
#     if hora >= 0 and hora <= 11:
#         print('Bom dia!')
#     elif hora >= 12 and hora <= 17:
#         print('Boa tarde!')
#     elif hora >= 18 and hora <=23:
#         print('Boa noite!')
#     else:
#         print('valor de hora inexistente!')
# except:
#     print('Valor não é inteiro!')

"""
Faça um programa que peça o primeiro nome do usuário. 
Se o nome tiver 4 letras ou menos escreva "Seu nome é curto";
Se o nome tiver entre 5 e 6 letras, escreva "Seu nome é normal";
Se o nome tiver mais que 6 letras, escreva "Seu nome é muito grande;
"""

nome = input('Digite seu primeiro nome: ')
tamanho_nome = len(nome)

if tamanho_nome > 1:
    if tamanho_nome <= 4:
        print('Seu nome é curto!')
    elif tamanho_nome >= 5 and tamanho_nome <= 6:
        print('Seu nome é normal!')
    else:
        print('Seu nome é muito grande')
else:
    print('Digite mais de uma letra')