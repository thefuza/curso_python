frase = 'O Python é uma linguagem de programação '\
    'multiparadigma. '\
    'Python foi criado por Guido Van Rossum.'.lower()

i = 0
aux1 = 0
aux2 = 0
aux3 = 0
primeira = ' '
segunda = ' '
terceira = ' '
letras_verificadas = '' # Criamos uma lista para não repetir o cálculo

while i < len(frase):
    letra_atual = frase[i]

    # Ignora espaços ou se a letra já foi processada
    if letra_atual == ' ' or letra_atual in letras_verificadas:
        i += 1
        continue
    
    contador_letras = frase.count(letra_atual)
    letras_verificadas += letra_atual # Marca a letra como verificada
  

    if contador_letras > aux1:
        # Move os valores antigos para baixo antes de atualizar
        aux3, terceira = aux2, segunda
        aux2, segunda = aux1, primeira
        aux1, primeira = contador_letras, letra_atual

    elif contador_letras > aux2:
        aux3, terceira = aux2, segunda
        aux2, segunda = contador_letras, letra_atual

    elif contador_letras > aux3:
        aux3, terceira = contador_letras, letra_atual


    i += 1

print(f'1ª letra mais repetida foi "{primeira}", se repetiu {aux1}x')
print(f'2ª letra mais repetida foi "{segunda}", se repetiu {aux2}x')
print(f'3ª letra mais repetida foi "{terceira}", se repetiu {aux3}x')