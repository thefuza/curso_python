class Pessoa:
    ano_atual = 2026

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade


    def get_ano_nacimento(self):
        return Pessoa.ano_atual - self.idade

p1 = Pessoa('João', 35)
p2 = Pessoa('Helena', 12)

print(f'O ano atual é: {Pessoa.ano_atual}')

print(f'O ano de nascimento {p1.nome} é {p1.get_ano_nacimento()}')
print(f'O ano de nascimento {p2.nome} é {p2.get_ano_nacimento()}')
