#============================
#           IMPORTS
#============================
from datetime import datetime

#============================
#           FUNÇÕES
#============================
def pontilhado():
    print('=' *60)

def calcular_status(data_prazo_str):
    hoje = datetime.now()
    data_limite = datetime.strptime(data_prazo_str, '%d/%m/%Y')
    prazo = data_limite - hoje
    dias = prazo.days
    if data_limite > hoje:
        return 'No prazo', dias
    
    return 'Em atraso', dias
    


#============================
#           CÓDIGO
#============================

pontilhado()
print('\tBEM VINDO AO SISTEMA DE GESTÃO DE DILIGÊNCIAS')
print()
print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
pontilhado()



diligencia = {
    'saj': input('Digite o número do SAJ (2026.01.000000): '),
    'sei': input('Digite o número do SEI (00.000000/2026-00): '),
    'diligencia': input('Digite o número da Diligência (nº/ano): '),
    'secretaria': input('Informe a Secretaria de destino: '),
    'prazo': input('Informe o prazo da diligência (dd/mm/aaaa): '),

}   

status_calculado, dias_calculados = calcular_status(diligencia['prazo'])
diligencia['status'] = status_calculado
diligencia['dias_restantes'] = dias_calculados

for chave, valor in diligencia.items():
    print(f'{chave}: {valor}')



