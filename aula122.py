# Métodos em instâncias de classes Python
# Hard coded - algo que foi escrito diretamente no código
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
