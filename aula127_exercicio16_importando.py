# Exercício - Salve sua classe em JSON
# Salve os dados da sua classe em JSON
# e depois crie novamente as instâncias
# da classe com os dados salvos
# faça em arquivos separados
import json
from aula127_exercicio16_classe import CAMINHO_ARQUIVO, Gato


dados_carregados = []
with open('gatinhas.json', 'r', encoding='utf8') as arquivo:
    dados_carregados = json.load(arquivo)

for dados_gata in dados_carregados:
    gata_objeto = Gato(**dados_gata)
        
    print(gata_objeto.nome, "-", gata_objeto.idade, "-", gata_objeto.cor)


