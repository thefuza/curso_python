# Exercício - Salve sua classe em JSON
# Salve os dados da sua classe em JSON
# e depois crie novamente as instâncias
# da classe com os dados salvos
# faça em arquivos separados
import json
from aula127_exercicio16_classe import CAMINHO_ARQUIVO, Gato

CAMINHO_ARQUIVO = 'gatinhas.json'


morgana = Gato('Morgana', 1, 'Cinza')
margot = Gato('Margot', 1, 'Cinza com branco')
nala = Gato('Nala', 3, 'Mariscada Siamês')
flor = Gato('Flor', 0, 'Tricolor')

gatas = [
    morgana.__dict__,
    margot.__dict__,
    nala.__dict__,
    flor.__dict__,
]

with open(CAMINHO_ARQUIVO, 'w', encoding='utf8') as arquivo:
    json.dump(
        gatas,
        arquivo,
        ensure_ascii=False,
        indent=2,
        )
# print(morgana.nome)
# print(morgana.idade)
# print(morgana.cor)

# print()

# print(margot.nome)
# print(margot.idade)
# print(margot.cor)

# print()

# print(nala.nome)
# print(nala.idade)
# print(nala.cor)

# print()

# print(flor.nome)
# print(flor.idade)
# print(flor.cor)

