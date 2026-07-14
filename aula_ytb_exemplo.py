import json
import os
# pessoas = [
#     {
#         "nome":'maria',
#         "sobrenome":'vieira',
#         "idade":25,
#         "ativo":False,
#         "notas":['A', 'A+'],
#         "telefones": {
#             "residencial": "00 0000-0000",
#             "celular": "00 0000-0000"
#         }
#     },
#     {
#         "nome":'Joana',
#         "sobrenome":'Moreira',
#         "idade":32,
#         "ativo":True,
#         "notas":['B', 'A'],
#         "telefones": {
#             "residencial": "00 0000-0000",
#             "celular": "00 0000-0000"
#         }
#     },
# ]

# BASE_DIR = os.path.dirname(__file__)
# SAVE_TO = os.path.join(BASE_DIR, 'arquivo-python.json')

# with open(SAVE_TO, 'w') as arquivo:
#     json.dump(pessoas, arquivo, indent=2)

# print(json.dumps(pessoas, indent=2))

# BASE_DIR = os.path.dirname(__file__)
# JSON_FILE = os.path.join(BASE_DIR, 'arquivo-python.json')

# with open(JSON_FILE, 'r') as file:
#     pessoas = json.load(file)
#     print(json.dumps(pessoas))

    # for pessoa in pessoas:
    #     print(pessoa['nome'])

json_string = """
[{"nome": "maria", "sobrenome": "vieira", "idade": 25, "ativo": false, "notas": ["A", "A+"], "telefones": {"residencial": "00 0000-0000", "celular": "00 0000-0000"}}, {"nome": "Joana", "sobrenome": "Moreira", "idade": 32, "ativo": true, "notas": ["B", "A"], "telefones": {"residencial": "00 0000-0000", "celular": "00 0000-0000"}}]
"""

pessoas = json.loads(json_string)

for pessoa in pessoas:
    print(pessoa['nome'])