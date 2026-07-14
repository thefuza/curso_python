# Exercício - Lista de tarefas com desfazer e refazer
# Música para codar =)
# Everybody wants to rule the world - Tears for fears
# todo = [] -> lista de tarefas
# todo = ['fazer café'] -> Adicionar fazer café
# todo = ['fazer café', 'caminhar'] -> Adicionar caminhar
# desfazer = ['fazer café',] -> Refazer ['caminhar']
# desfazer = [] -> Refazer ['caminhar', 'fazer café']
# refazer = todo ['fazer café']
# refazer = todo ['fazer café', 'caminhar']
import os
import json





#############################################
#                 FUNÇÕES
#############################################

def listar(tarefas):
    print()
    if not tarefas:
        print('Nenhuma tarefa para listar!')
        print()
        return

    print('Tarefas: ')
    for tarefa in tarefas:
        print(f'\t{tarefa}')
    print()
    



def desfazer(tarefas, tarefas_refazer):
    print()
    if not tarefas:
        print('Nenhuma tarefa para desfazer!')
        print()
        return

    tarefa = tarefas.pop()
    print(f'{tarefa=} removida da lista de tarefas!')
    tarefas_refazer.append(tarefa)
    print()
    listar(tarefas) 



def refazer(tarefas, tarefas_refazer):
    print()
    if not tarefas_refazer:
        print('Nenhuma tarefa para refazer!')
        print()
        return

    tarefa = tarefas_refazer.pop()
    print(f'{tarefa=} adionada da lista de tarefas!')
    tarefas.append(tarefa)
    print()
    listar(tarefas) 



def adicionar(tarefa, tarefas):
    print()
    tarefa = tarefa.strip()
    if not tarefa:
        print('Nenhuma tarefa digitada!')
        return
    print(f'{tarefa=} adionada da lista de tarefas!')
    tarefas.append(tarefa)
    print()
    listar(tarefas) 

def ler(tarefas, caminho_arquivo):
    dados = []
    try:
        with open(caminho_arquivo, 'r', encoding='utf8') as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print('Arquvo não existe!')
        salvar(tarefas, caminho_arquivo)
    return dados

def salvar(tarefas, caminho_arquivo):
    dados = tarefas
    with open(caminho_arquivo, 'w', encoding='utf8') as arquivo:
        dados = json.dump(tarefas, arquivo, indent=2, ensure_ascii=False)
    return dados
        

CAMINHO_ARQUIVO = 'aula119.json'
tarefas = ler([],CAMINHO_ARQUIVO)
tarefas_refazer = []
#############################################
#                 CÓDIGOS
#############################################

while True:
    print('Comandos: listar, desfazer, refazer')
    tarefa = input('Digite uma tarefa ou comando: ')

    comandos = {
        'listar': lambda: listar(tarefas),
        'desfazer': lambda: desfazer(tarefas, tarefas_refazer),
        'refazer': lambda: refazer(tarefas, tarefas_refazer),
        'clear': lambda: os.system('cls'),
        'adicionar': lambda: adicionar(tarefa, tarefas),
    }

    comando = comandos.get(tarefa) if comandos.get(tarefa) is not None else comandos['adicionar']
    comando()
    salvar(tarefas, CAMINHO_ARQUIVO)




# while True:
#     print('Comandos: listar, desfazer, refazer')
#     tarefa = input('Digite uma tarefa ou comando: ')

#     if tarefa == 'listar':
#         listar(tarefas)
#         continue
            

#     elif tarefa == 'desfazer':
#         desfazer(tarefas, tarefas_refazer)
#         listar(tarefas)
#         continue

#     elif tarefa == 'refazer':
#         refazer(tarefas, tarefas_refazer)
#         listar(tarefas)
#         continue
       
#     elif tarefa == 'clear':
#         os.system('cls')
#         continue
       
#     else:
#         adicionar(tarefa, tarefas)
#         listar(tarefas)
#         continue