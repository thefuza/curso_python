# Entendendo self em classes Python
# Classe - molde (geralmente sem dados)
# Instâncias da class (objeto) - Tem os dados
# Uma classe pode gerar várias instâncias.
# Na classe o self é a prórpia instância.

class Carro:
    def __init__(self, nome):
        self.nome = nome

    def acelerar(self):
        print(f'{self.nome} está acelerando...')

fusca = Carro('Fusca')
Carro.acelerar(fusca)
fusca.acelerar()
# print(fusca.nome)
celta = Carro('Celta')
Carro.acelerar(celta)
celta.acelerar()
# print(celta.nome)
