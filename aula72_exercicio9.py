
# Exercício com funções

# Crie uma função que multiplica todos os argumentos não nomeados recebidos

# Retorne o total para uma variavel e mostre o valor da variavel.

def multiplicar(*args):
    total = 1
    for numero in args:
        total *= numero
    return total
multiplicacao = multiplicar(1,2,3,4,5,6)
print(multiplicacao)

# Crie uma função 'fala' se um numero é par ou impar
# Retorne se o número é par ou impar

def fala(x):
    if x % 2 == 0:
        return(f'O número {x} é par')
    return(f'O número {x} é impar')

print(fala(3))