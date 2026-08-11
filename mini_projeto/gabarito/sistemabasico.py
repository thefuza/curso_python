import tkinter as tk
from tkinter.font import Font

janela = tk.Tk()

janela.title("Sistema de Cadastro de Usuários")
janela.geometry("900x600")

# criar o elemento
titulo = tk.Label(text="Meu app", font=Font(size=22, weight='bold', family="Times New Roman"))
# posicionar ele na janela
titulo.pack(pady=(20,20))

# criar o elemento
titulo = tk.Label(text="Bem Vindo!")
# posicionar ele na janela
titulo.pack(pady=(20, 20))

janela.mainloop()