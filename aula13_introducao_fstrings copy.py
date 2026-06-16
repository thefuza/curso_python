nome = 'Gabriel Melo'
altura = 1.74
peso = 58
imc = peso / altura ** 2 # IMC = peso / (altura x altura)

# f-strings - f -> format
linha_1 = f'{nome} tem {altura:.2f} de altura'
linha_2 = f'pesa, {peso}, quilos e seu IMC é'
linha_3 = f'{imc:.2f}'

print(linha_1)
print(linha_2)
print(linha_3)

# Gabriel Melo tem 1.74 de altura,
# pesa 58 quilos e seu IMC é
# 19.157088122605362