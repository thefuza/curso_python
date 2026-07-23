# Heranca simples - Relações entre classes
# Associação - usa, Agregação - tem
# Composição -  É dono de, Herança - É um
#
# Herança vs Composição
#
# Classe principal (Pessoa)
#   -> super class, base class, parent class
# Classes filhas (Clientes)
#   -> sub class, child, derived class
class Pessoa:
    cpf: '1234'

    def __init__(self, nome, sobrenome):
        self.nome = nome
        self.sobrenome = sobrenome
        
    def falar_nome_classe(self):
        print('classe Pessoa')
        print(self.nome, self.sobrenome, self.__class__.__name__)

class Cliente(Pessoa):
    def falar_nome_classe(self):
        print('Classe Clinte')
        print(self.nome, self.sobrenome, self.__class__.__name__)

class Aluno(Pessoa):
    ...


c1 = Cliente('Luiz', 'Otávio')
c1.falar_nome_classe()
a1 = Aluno('Maria', 'Helena')
a1.falar_nome_classe()
# print(a1.cpf)
# help(Cliente)

