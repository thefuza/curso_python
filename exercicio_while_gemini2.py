'''
Crie um programa que peça ao usuário para digitar números repetidamente.
O programa deve somar esses números e mostrar o total. 
O loop deve parar apenas quando o usuário digitar o número 0.
'''
total = 0
contador = 0


while True:
    try:
        entrada = float(input('Digite um número (ou 0 para parar): '))
    except ValueError:
        print('Este dado não é um número')
        continue

    
    if entrada != 0:
        contador += 1

    else:
        break

    total += entrada

print(f'A soma total é: {total:.0f}')
print(f'A quantidade de números digitados foi: {contador}')