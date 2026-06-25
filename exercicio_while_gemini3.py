'''
Crie um programa que peça para o usuário digitar uma senha. 
O programa deve ficar pedindo a senha infinitamente até que o 
usuário digite a senha correta 
(defina uma senha secreta, ex: "python123"). Quando acertar,
 imprima "Acesso permitido".
'''

senha_correta = 'python123'
tentativa_usuario = ''

while tentativa_usuario != senha_correta:
    tentativa_usuario = input('Digite sua senha: ')
   
    if tentativa_usuario != senha_correta:
        print('Senha invalida, tente novamente!')
        
print('Acesso Permitido!')