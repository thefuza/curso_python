""" Calculadora com While """

while True:
    numero1 = input('Digite o primeiro número: ')
    operador = input('Digite qual operação deseja (+-*/): ')
    numero2 = input('Digite o segundo número: ')
    

    numeros_validos = None
    num_1_float = 0
    num_2_float = 0

    try:
        num_1_float = float(numero1)
        num_2_float = float(numero2)
        numeros_validos = True
    except:
        numeros_validos = None
        
    if numeros_validos is None:
        print('Um ou ambos os números digitados são invalidos.')
        continue

    ##########

    operadores_permitidos = '+-*/'
    
    if operador not in operadores_permitidos:
        print('Operador inválido')
        continue

    if len(operador) > 1:
        print('Digite apenas um operador')
        continue
    
    
    ##########

    print('Realizando sua conta, confira o resultado abaixo')

    if operador == '+':
        print(f'{num_1_float} + {num_2_float} =', num_1_float+num_2_float )
        
    elif operador == '-':
        print(f'{num_1_float} - {num_2_float} =', num_1_float-num_2_float )
        
    elif operador == '*':
        print(f'{num_1_float} * {num_2_float} =', num_1_float*num_2_float )
        
    elif operador == '/':
        print(f'{num_1_float} / {num_2_float} =', num_1_float/num_2_float )
    else:
        print('Nunca deveria chegar aqui')


    ##########
    sair = input('Quer sair? [s]im: ').lower().startswith('s')
    print(sair)

    if sair is True:
        break



# while operador 

# if operador == '+':
#     print(numero1 + numero2)
# if operador == '-':
#     print(numero1 - numero2)
# if operador == '*':
#     print(numero1 * numero2)
# if operador == '/':
#     print(numero1 / numero2)
    