import customtkinter as ctk

ctk.set_appearance_mode("Dark") # Dark, System, Light
ctk.set_default_color_theme("blue") # blue, green, dark-blue


class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro de Clientes")
        self.geometry("900x600")

        # Criar divisão da tela. weight=1 expande junto com a tela

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # parte lateral
        self.barra_lateral = ctk.CTkFrame(self, width=200)
        self.barra_lateral.grid(row=0, column=0, sticky="nsew", pady=17)

        # parte principal
        self.janela_abas = ctk.CTkTabview(self, width=400)
        self.janela_abas.grid(row=0, column=1, sticky="nsew", padx=17)

        # preencher as partes/abas

        # preencher aba lateral
        self.construir_aba_lateral()
        
        # preencher aba perfil
        self.construir_aba_perfil()

        # preencher aba preferências
        self.construir_aba_preferencias()

        # preencher aba sistemas
        self.construir_aba_sistema()



    def construir_aba_lateral(self):
        self.titulo = ctk.CTkLabel(self.barra_lateral, text="Meu App", font=ctk.CTkFont(size=24, weight="bold", family="arial"))
        self.titulo.pack(pady=(30, 10), padx=(20,20))

        self.botao_principal = ctk.CTkButton(self.barra_lateral, text="Dashboard Principal")
        self.botao_principal.pack(pady=(60, 30), padx=(20,20))

        self.switch_mododark = ctk.CTkSwitch(self.barra_lateral, text="Modo Escuro")
        self.switch_mododark.pack(pady=(10,30), side="bottom")
        
    def construir_aba_perfil(self):
        # Campo de nome
        # Radio button do nível de usuário
        # Checkbox
        pass
    def construir_aba_preferencias(self):
        pass
    def construir_aba_sistema(self):
        pass
        
    

janela = Aplicativo()
janela.mainloop()