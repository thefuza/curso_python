primeiro_valor = input('Digite um valor: ')
segundo_valor = input('Digite outro valor: ')

# int_primeiro_valor = int(primeiro_valor)
# int_segundo_valor = int(segundo_valor)

if primeiro_valor > segundo_valor:
    print(f'{primeiro_valor=}, é maior '
          f'que o {segundo_valor=}'
    )
elif primeiro_valor == segundo_valor:
    print(f'{primeiro_valor=} é igual ao {segundo_valor=}')
else:
    print(f'{segundo_valor=}, é maior '
          f'que o {primeiro_valor=}'
    )
