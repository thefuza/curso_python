"""
Valores padrão para parametros
Ao definiir uma função, os parametros podem ter valores padrão.
Caso o valor não seja enviado para o parametro, o valor será usado.
Refatorar: editar o seu código.
"""

def soma(x, y, z=None):
    if z is not None:
        print('Com Z')
        print(f'{x} + {y} + {z}', x + y + z)
    else:
        print('Sem Z')
        print(f'{x} + {y}', x + y)

soma(1, 2)
soma(3, 5)
soma(100, 200)
soma(7, 9, 0)
