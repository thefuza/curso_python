"""
while/else
"""

string = 'Gabriel de Souza Costa Melo'

i = 0
espacos = 0

while i < len(string):
    letra = string[i]

    if string[i]== ' ':
        espacos +=1

    print(letra)
    i+=1

else:
    print(f'o nome {string} contém {espacos} espaços')
print('Fora do while')