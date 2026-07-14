# class - Classes são moldes para criar novos objetos
# As classes geram novos objetos (instancias)
# podem ter seus prórpios atribuos e metodos.
# Os objetos gerados pela classe podem usar seus dados internos para realziar várias ações.
# Por convenção, usamos PascalCAse para nomes de classes.
# string = 'Gabriel' # str
# print(string.upper())
# print(isinstance(string, str))

class Pessoa:
    def __init__(self, nome, sobrenome):
        self.nome = nome
        self.sobrenome = sobrenome

p1 = Pessoa('Gabriel', 'Melo')
# p1.nome = 'Gabriel'
# p1.sobrenome = 'Melo'
p2 = Pessoa('Maria', 'Joana')
# p2.nome = 'Maria'
# p2.sobrenome = 'Joana'

print(p1.nome)
print(p1.sobrenome)

print(p2.nome)
print(p2.sobrenome)