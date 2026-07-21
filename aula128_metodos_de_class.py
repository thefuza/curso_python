# Metodos de Classe + factories (fabricas)
# São metodos onde o "self" será "cls", ou seja,
# ao invés de recber a instancia no primeiro
# parametro, recebemos a própria classe.
class Pessoa:
    ano = 2023 # atributo de classe

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    @classmethod
    def metodo_classe(cls):
        print('Hey')

    @classmethod
    def criar_com_50_anos(cls, nome):
        return cls(nome, 50)

    @classmethod
    def criar_sem_nome(cls, idade):
        return cls('Anônimo', idade)

p1 = Pessoa('João', 34)
p2 = Pessoa.criar_com_50_anos('Helena')
p3 = Pessoa('Anônima', 23)
p4 = Pessoa.criar_sem_nome(25)
print(p2.nome, p2.idade)
print(p3.nome, p3.idade)
print(p4.nome, p4.idade)

# Pessoa.metodo_classe()
# print(Pessoa.ano)