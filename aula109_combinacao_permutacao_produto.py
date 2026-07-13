# Combinations, Permutations e Product
# Combinação - Ordem não importa - iteravel + tamanho do grupo
# # Permutação - Ordem importa
# # Produto - Ordem importa e repete valores únicos
from itertools import combinations, permutations, product

def print_iter(iterator):
    print(*list(iterator), sep='\n')
    print()

pessoas = [
    'João', 'Joana', 'Luiz', 'Leticia',
]

camisetas = [
    ['preta', 'branca'],
    ['p', 'm', 'g'],
    ['masculino', 'feminino', 'unisex'],
    ['algodao', 'poliester'],
]

# print_iter(combinations(pessoas, 2))
# print_iter(permutations(pessoas, 2))
print_iter(product(*camisetas))