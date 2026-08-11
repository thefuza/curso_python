#============================
# IMPORTS
#============================
import re
from datetime import datetime
import mysql.connector
import customtkinter as ctk
from tkinter import ttk, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#============================
# BANCOS DE DADOS E CONEXÕES
#============================
def conectar_banco_diligencias():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",               # Altere para seu usuário
            password="Gx-3201383",     # Altere para sua senha
            database="db_gestao_diligencias"
        )
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro Conexão Diligências", f"Erro ao conectar ao banco de Diligências:\n{erro}")
        return None

def conectar_banco_usucapiao():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",               # Altere para seu usuário
            password="Gx-3201383",     # Altere para sua senha
            database="db_gestao_usucapiao"
        )
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro Conexão Usucapião", f"Erro ao conectar ao banco de Usucapião:\n{erro}")
        return None

#============================
# FUNÇÕES DE MÁSCARA E DATA
#============================
def calcular_status_diligencia(data_prazo_str):
    if not data_prazo_str or data_prazo_str == 'None':
        return 'Sem Prazo', 0
    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        data_limite = datetime.strptime(str(data_prazo_str), '%Y-%m-%d')
    except ValueError:
        return 'Erro: Data inválida', 0
    
    prazo = data_limite - hoje
    dias = prazo.days
    return ('No prazo' if data_limite >= hoje else 'Em atraso'), dias

def formatar_e_validar_data(data_str):
    if not data_str or data_str.strip() == "":
        return None, "O campo de data não pode estar vazio."
    if len(data_str) == 10 and data_str.count('/') == 2:
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            return data_obj.strftime("%Y-%m-%d"), None
        except ValueError:
            return None, "Data inválida (ex: dias inexistentes no mês)."
    return None, "Formato incorreto. Use DD/MM/AAAA."

def formatar_saj(valor):
    if not valor or not valor.strip():
        return ""
    if '.' in valor or '-' in valor or ' ' in valor:
        partes = [p for p in re.split(r'[^\d]', valor) if p]
        if len(partes) >= 3:
            return f"{partes[0].zfill(4)[:4]}.{partes[1].zfill(2)[:2]}.{partes[2].zfill(6)[:6]}"
        elif len(partes) == 2:
            return f"{partes[0].zfill(4)[:4]}.01.{partes[1].zfill(6)[:6]}"
        elif len(partes) == 1:
            valor = partes[0]

    digitos = re.sub(r'\D', '', valor)
    if not digitos:
        return ""
    if len(digitos) >= 6:
        return f"{digitos[:4]}.{digitos[4:6]}.{digitos[6:12].zfill(6)}"
    elif len(digitos) > 4:
        return f"{digitos[:4]}.01.{digitos[4:].zfill(6)}"
    return f"{digitos.zfill(4)}.01.000000"

def formatar_sei(valor):
    if not valor or not valor.strip():
        return ""
    partes = [p for p in re.split(r'[^\d]', valor) if p]
    if len(partes) >= 4:
        return f"{partes[0].zfill(2)[:2]}.{partes[1].zfill(6)[:6]}/{partes[2].zfill(4)[:4]}-{partes[3].zfill(2)[:2]}"
    elif len(partes) == 3:
        return f"{partes[0].zfill(2)[:2]}.{partes[1].zfill(6)[:6]}/{partes[2].zfill(4)[:4]}-00"
    
    digitos = re.sub(r'\D', '', valor)
    if not digitos:
        return ""
    if len(digitos) == 14:
        return f"{digitos[:2]}.{digitos[2:8]}/{digitos[8:12]}-{digitos[12:]}"
    elif len(digitos) > 8:
        return f"{digitos[:2]}.{digitos[2:-6].zfill(6)[:6]}/{digitos[-6:-2]}-{digitos[-2:]}"
    return digitos

def formatar_diligencia(valor):
    if not valor or not valor.strip():
        return ""
    ano_atual = str(datetime.now().year)
    if '/' in valor:
        partes = valor.split('/')
        num = re.sub(r'\D', '', partes[0])
        ano = re.sub(r'\D', '', partes[1]) if len(partes) > 1 and partes[1] else ano_atual
        return f"{num.zfill(4)}/{ano}" if num else ""
    digitos = re.sub(r'\D', '', valor)
    if not digitos:
        return ""
    if len(digitos) > 4 and len(digitos) <= 8:
        return f"{digitos[:-4].zfill(4)}/{digitos[-4:]}"
    return f"{digitos.zfill(4)}/{ano_atual}"

#============================
# TELA DE LOGIN
#============================
class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Acesso ao Sistema")
        self.geometry("380x420")
        self.resizable(False, False)

        self.usuario_logado = None
        self.perfil_logado = None

        ctk.CTkLabel(self, text="Sistema de Gestão", font=("Arial", 22, "bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Informe suas credenciais para acessar", font=("Arial", 11), text_color="gray").pack(pady=(0, 25))

        self.e_login = ctk.CTkEntry(self, placeholder_text="Login", width=280, height=35)
        self.e_login.pack(pady=10)

        self.e_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=280, height=35)
        self.e_senha.pack(pady=10)

        ctk.CTkButton(self, text="Entrar", command=self.autenticar, width=280, height=40, font=("Arial", 12, "bold")).pack(pady=25)

    def autenticar(self):
        login = self.e_login.get().strip()
        senha = self.e_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Aviso", "Preencha o login e a senha.")
            return

        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT * FROM tb_usuarios WHERE login=%s AND senha=%s", (login, senha))
                usuario = cur.fetchone()

                if usuario:
                    self.usuario_logado = usuario['login']
                    self.perfil_logado = usuario['perfil']
                    self.destroy()
                else:
                    messagebox.showerror("Erro de Acesso", "Login ou senha incorretos.")
            finally:
                cur.close(); con.close()

#============================
# JANELA DE GERENCIAMENTO DE USUÁRIOS (ADMIN)
#============================
class JanelaUsuarios(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gerenciamento de Usuários")
        self.geometry("600x420")
        self.transient(parent)
        self.id_sel = None

        f_form = ctk.CTkFrame(self, width=220)
        f_form.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(f_form, text="Usuário", font=("Arial", 14, "bold")).pack(pady=10)
        self.e_login = ctk.CTkEntry(f_form, placeholder_text="Login", width=180)
        self.e_login.pack(pady=5)
        self.e_senha = ctk.CTkEntry(f_form, placeholder_text="Senha", show="*", width=180)
        self.e_senha.pack(pady=5)
        
        self.cmb_perfil = ctk.CTkComboBox(f_form, values=["usuario", "admin"], width=180)
        self.cmb_perfil.pack(pady=5)

        ctk.CTkButton(f_form, text="Salvar Novo", command=self.salvar, fg_color="green", width=180).pack(pady=10)
        ctk.CTkButton(f_form, text="Atualizar", command=self.atualizar, fg_color="orange", width=180).pack(pady=3)
        ctk.CTkButton(f_form, text="Excluir", command=self.excluir, fg_color="red", width=180).pack(pady=3)

        f_list = ctk.CTkFrame(self)
        f_list.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)

        cols = ("id", "login", "perfil")
        self.tree = ttk.Treeview(f_list, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID"); self.tree.column("id", width=30)
        self.tree.heading("login", text="LOGIN"); self.tree.column("login", width=120)
        self.tree.heading("perfil", text="PERFIL"); self.tree.column("perfil", width=90)
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.carregar)

        self.listar()

    def limpar(self):
        self.id_sel = None
        self.e_login.delete(0, 'end')
        self.e_senha.delete(0, 'end')
        self.cmb_perfil.set("usuario")

    def listar(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT id, login, perfil FROM tb_usuarios")
                for u in cur.fetchall():
                    self.tree.insert("", "end", values=(u['id'], u['login'], u['perfil']))
            finally:
                cur.close(); con.close()

    def carregar(self, event):
        sel = self.tree.selection()
        if sel:
            v = self.tree.item(sel[0], "values")
            self.id_sel = v[0]
            self.e_login.delete(0, 'end'); self.e_login.insert(0, v[1])
            self.cmb_perfil.set(v[2])

    def salvar(self):
        log, sen, perf = self.e_login.get().strip(), self.e_senha.get().strip(), self.cmb_perfil.get()
        if not log or not sen: messagebox.showwarning("Aviso", "Preencha todos os campos.", parent=self); return
        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO tb_usuarios (login, senha, perfil) VALUES (%s, %s, %s)", (log, sen, perf))
                con.commit()
                self.limpar(); self.listar()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", str(err), parent=self)
            finally: cur.close(); con.close()

    def atualizar(self):
        if not self.id_sel: return
        log, sen, perf = self.e_login.get().strip(), self.e_senha.get().strip(), self.cmb_perfil.get()
        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor()
                if sen:
                    cur.execute("UPDATE tb_usuarios SET login=%s, senha=%s, perfil=%s WHERE id=%s", (log, sen, perf, self.id_sel))
                else:
                    cur.execute("UPDATE tb_usuarios SET login=%s, perfil=%s WHERE id=%s", (log, perf, self.id_sel))
                con.commit()
                self.limpar(); self.listar()
            finally: cur.close(); con.close()

    def excluir(self):
        if not self.id_sel: return
        if messagebox.askyesno("Confirmar", "Deseja excluir o usuário?", parent=self):
            con = conectar_banco_diligencias()
            if con:
                try:
                    cur = con.cursor()
                    cur.execute("DELETE FROM tb_usuarios WHERE id=%s", (self.id_sel,))
                    con.commit()
                    self.limpar(); self.listar()
                finally: cur.close(); con.close()

#============================
# CLASSE PRINCIPAL DA APLICAÇÃO
#============================
class Aplicativo(ctk.CTk):
    def __init__(self, usuario_atual, perfil_atual):
        super().__init__()
        self.usuario_atual = usuario_atual
        self.perfil_atual = perfil_atual
        self.deseja_fazer_logout = False

        self.title("Sistema de Gestão - Diligências e Usucapião")
        self.geometry("1280x720")

        self.id_diligencia_sel = None
        self.id_usucapiao_sel = None

        # --- BARRA SUPERIOR DE INFORMAÇÕES E LOGOUT ---
        f_top = ctk.CTkFrame(self, height=40)
        f_top.pack(fill="x", padx=10, pady=(5, 0))

        lbl_user = f"Usuário Logado: {self.usuario_atual} ({self.perfil_atual.upper()})"
        ctk.CTkLabel(f_top, text=lbl_user, font=("Arial", 12, "bold")).pack(side="left", padx=15)

        if self.perfil_atual == 'admin':
            ctk.CTkButton(f_top, text="⚙ Gerenciar Usuários", command=self.abrir_gerencial_usuarios, fg_color="#3a7ebf", height=28).pack(side="left", padx=10)

        # Botão de Logout
        ctk.CTkButton(f_top, text="🚪 Sair", command=self.fazer_logout, fg_color="#a83232", hover_color="#7a2323", height=28, width=70).pack(side="right", padx=10)

        self.switch_tema = ctk.CTkSwitch(f_top, text="Modo Claro", command=self.alternar_tema)
        self.switch_tema.pack(side="right", padx=10)
        
        # --- ABAS DAS LOTAÇÕES ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tab_diligencias = self.tabview.add("Lotação Diligência")
        self.tab_usucapiao = self.tabview.add("Lotação Usucapião")

        self.configurar_estilo_treeview("dark")

        self.montar_aba_diligencias()
        self.montar_aba_usucapiao()

    def fazer_logout(self):
        if messagebox.askyesno("Logout", "Deseja realmente sair da sua conta?"):
            self.deseja_fazer_logout = True
            self.destroy()

    def abrir_gerencial_usuarios(self):
        JanelaUsuarios(self)

    def configurar_estilo_treeview(self, modo):
        style = ttk.Style()
        style.theme_use("clam")
        if modo == "dark":
            style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=28, font=("Arial", 10))
            style.configure("Treeview.Heading", background="#1f1f1f", foreground="white", font=("Arial", 10, "bold"))
            style.map("Treeview", background=[("selected", "#1f538d")])
        else:
            style.configure("Treeview", background="#ffffff", foreground="#000000", fieldbackground="#ffffff", rowheight=28, font=("Arial", 10))
            style.configure("Treeview.Heading", background="#e0e0e0", foreground="#000000", font=("Arial", 10, "bold"))
            style.map("Treeview", background=[("selected", "#3a7ebf")])

    def alternar_tema(self):
        if self.switch_tema.get() == 1:
            ctk.set_appearance_mode("light")
            self.configurar_estilo_treeview("light")
        else:
            ctk.set_appearance_mode("dark")
            self.configurar_estilo_treeview("dark")

    # ==========================================
    # 1. LOTAÇÃO DILIGÊNCIA
    # ==========================================
    def montar_aba_diligencias(self):
        self.f_form_dil = ctk.CTkFrame(self.tab_diligencias, width=320)
        self.f_form_dil.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.f_form_dil, text="Lotação Diligência", font=("Arial", 18, "bold")).pack(pady=15)

        self.e_saj_dil = ctk.CTkEntry(self.f_form_dil, placeholder_text="SAJ (ex: 2025.01.24)", width=260)
        self.e_saj_dil.pack(pady=8)
        self.e_saj_dil.bind("<FocusOut>", lambda e: self.aplicar_mascara_campo(self.e_saj_dil, formatar_saj))

        self.e_sei_dil = ctk.CTkEntry(self.f_form_dil, placeholder_text="SEI (ex: 05.123/2024-01)", width=260)
        self.e_sei_dil.pack(pady=8)
        self.e_sei_dil.bind("<FocusOut>", lambda e: self.aplicar_mascara_campo(self.e_sei_dil, formatar_sei))

        self.e_num_dil = ctk.CTkEntry(self.f_form_dil, placeholder_text="Diligência (ex: 24)", width=260)
        self.e_num_dil.pack(pady=8)
        self.e_num_dil.bind("<FocusOut>", lambda e: self.aplicar_mascara_campo(self.e_num_dil, formatar_diligencia))

        self.e_sec_dil = ctk.CTkEntry(self.f_form_dil, placeholder_text="Secretaria", width=260)
        self.e_sec_dil.pack(pady=8)

        self.e_envio_dil = ctk.CTkEntry(self.f_form_dil, placeholder_text="Data Envio (DD/MM/AAAA)", width=260)
        self.e_envio_dil.pack(pady=8)

        self.e_prazo_dil = ctk.CTkEntry(self.f_form_dil, placeholder_text="Prazo (DD/MM/AAAA)", width=260)
        self.e_prazo_dil.pack(pady=8)

        ctk.CTkButton(self.f_form_dil, text="Salvar Novo", command=self.dil_cadastrar, fg_color="green", hover_color="darkgreen", width=260).pack(pady=10)
        ctk.CTkButton(self.f_form_dil, text="Atualizar Selecionado", command=self.dil_atualizar, fg_color="orange", hover_color="#b37400", width=260).pack(pady=5)
        ctk.CTkButton(self.f_form_dil, text="Limpar Campos", command=self.dil_limpar_campos, fg_color="gray", width=260).pack(pady=5)

        self.f_lista_dil = ctk.CTkFrame(self.tab_diligencias)
        self.f_lista_dil.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)

        f_pesq = ctk.CTkFrame(self.f_lista_dil, fg_color="transparent")
        f_pesq.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(f_pesq, text="Buscar:", font=("Arial", 12, "bold")).pack(side="left", padx=(0, 5))
        self.e_pesq_dil = ctk.CTkEntry(f_pesq, placeholder_text="Digite SAJ, SEI, Diligência...", width=300)
        self.e_pesq_dil.pack(side="left", fill="x", expand=True, padx=5)
        self.e_pesq_dil.bind("<KeyRelease>", lambda e: self.dil_listar())

        cols = ("id", "saj", "sei", "diligencia", "secretaria", "envio", "prazo", "status", "enviado_por")
        self.tab_dil_tree = ttk.Treeview(self.f_lista_dil, columns=cols, show="headings", selectmode="browse")
        
        headers = ("ID", "SAJ", "SEI", "DILIGÊNCIA", "SECRETARIA", "ENVIO", "PRAZO", "STATUS", "ENVIADO POR")
        for c, h in zip(cols, headers):
            self.tab_dil_tree.heading(c, text=h)

        self.tab_dil_tree.column("id", width=30, anchor="center")
        self.tab_dil_tree.column("saj", width=110)
        self.tab_dil_tree.column("sei", width=110)
        self.tab_dil_tree.column("diligencia", width=80)
        self.tab_dil_tree.column("secretaria", width=90)
        self.tab_dil_tree.column("envio", width=75, anchor="center")
        self.tab_dil_tree.column("prazo", width=75, anchor="center")
        self.tab_dil_tree.column("status", width=100)
        self.tab_dil_tree.column("enviado_por", width=90)

        self.tab_dil_tree.pack(pady=10, padx=10, fill="both", expand=True)
        self.tab_dil_tree.bind("<Double-1>", self.dil_carregar_campos)

        f_act = ctk.CTkFrame(self.f_lista_dil, fg_color="transparent")
        f_act.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(f_act, text="✔ Concluir", command=self.dil_concluir, fg_color="#1f538d", hover_color="#14375e", width=120).pack(side="left", padx=5)
        ctk.CTkButton(f_act, text="Ver Concluídas", command=self.dil_abrir_concluidas, fg_color="#454545", hover_color="#2b2b2b", width=120).pack(side="left", padx=5)
        ctk.CTkButton(f_act, text="✖ Excluir", command=self.dil_excluir, fg_color="red", hover_color="darkred", width=120).pack(side="right", padx=5)

        self.dil_listar()

    def aplicar_mascara_campo(self, widget, funcao_mascara):
        val = widget.get()
        if val.strip():
            widget.delete(0, 'end'); widget.insert(0, funcao_mascara(val))

    def dil_limpar_campos(self):
        self.id_diligencia_sel = None
        for e in (self.e_saj_dil, self.e_sei_dil, self.e_num_dil, self.e_sec_dil, self.e_envio_dil, self.e_prazo_dil):
            e.delete(0, 'end')

    def dil_cadastrar(self):
        self.aplicar_mascara_campo(self.e_saj_dil, formatar_saj)
        self.aplicar_mascara_campo(self.e_sei_dil, formatar_sei)
        self.aplicar_mascara_campo(self.e_num_dil, formatar_diligencia)

        saj, sei, dil, sec = self.e_saj_dil.get(), self.e_sei_dil.get(), self.e_num_dil.get(), self.e_sec_dil.get()
        if not saj: messagebox.showwarning("Aviso", "O SAJ é obrigatório!"); return

        envio_fmt, e_err = formatar_e_validar_data(self.e_envio_dil.get())
        if e_err: messagebox.showwarning("Data Envio", e_err); return
        prazo_fmt, p_err = formatar_e_validar_data(self.e_prazo_dil.get())
        if p_err: messagebox.showwarning("Prazo", p_err); return

        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor()
                sql = "INSERT INTO tb_gestao (saj, sei, diligencia, secretaria, data_envio, prazo, usuario_criacao, data_criacao) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"
                cur.execute(sql, (saj, sei, dil, sec, envio_fmt, prazo_fmt, self.usuario_atual))
                con.commit()
                messagebox.showinfo("Sucesso", "Diligência cadastrada!")
                self.dil_limpar_campos(); self.dil_listar()
            finally:
                cur.close(); con.close()

    def dil_listar(self):
        for item in self.tab_dil_tree.get_children(): self.tab_dil_tree.delete(item)
        busca = self.e_pesq_dil.get()
        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                if busca:
                    sql = "SELECT * FROM tb_gestao WHERE saj LIKE %s OR sei LIKE %s OR diligencia LIKE %s OR secretaria LIKE %s"
                    lk = f"%{busca}%"
                    cur.execute(sql, (lk, lk, lk, lk))
                else:
                    cur.execute("SELECT * FROM tb_gestao")
                
                for row in cur.fetchall():
                    pz_str = row['prazo'].strftime('%Y-%m-%d') if hasattr(row['prazo'], 'strftime') else str(row['prazo'])
                    env_str = row['data_envio'].strftime('%d/%m/%Y') if hasattr(row['data_envio'], 'strftime') else (row['data_envio'] or "")
                    ex_pz = row['prazo'].strftime('%d/%m/%Y') if hasattr(row['prazo'], 'strftime') else pz_str
                    st, dias = calcular_status_diligencia(pz_str)
                    
                    self.tab_dil_tree.insert("", "end", values=(
                        row['id'], row['saj'], row['sei'], row['diligencia'],
                        row['secretaria'], env_str, ex_pz, f"{st} ({dias}d)", row['usuario_criacao'] or "N/A"
                    ))
            finally: cur.close(); con.close()

    def dil_carregar_campos(self, event):
        sel = self.tab_dil_tree.selection()
        if sel:
            v = self.tab_dil_tree.item(sel[0], "values")
            self.id_diligencia_sel = v[0]
            for widget, val in zip([self.e_saj_dil, self.e_sei_dil, self.e_num_dil, self.e_sec_dil, self.e_envio_dil, self.e_prazo_dil], v[1:7]):
                widget.delete(0, 'end'); widget.insert(0, val)

    def dil_atualizar(self):
        if not self.id_diligencia_sel: messagebox.showwarning("Aviso", "Selecione uma diligência."); return
        self.aplicar_mascara_campo(self.e_saj_dil, formatar_saj)
        self.aplicar_mascara_campo(self.e_sei_dil, formatar_sei)
        self.aplicar_mascara_campo(self.e_num_dil, formatar_diligencia)

        envio_fmt, e_err = formatar_e_validar_data(self.e_envio_dil.get())
        if e_err: messagebox.showwarning("Data Envio", e_err); return
        prazo_fmt, p_err = formatar_e_validar_data(self.e_prazo_dil.get())
        if p_err: messagebox.showwarning("Prazo", p_err); return

        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor()
                sql = "UPDATE tb_gestao SET saj=%s, sei=%s, diligencia=%s, secretaria=%s, data_envio=%s, prazo=%s WHERE id=%s"
                cur.execute(sql, (self.e_saj_dil.get(), self.e_sei_dil.get(), self.e_num_dil.get(), self.e_sec_dil.get(), envio_fmt, prazo_fmt, self.id_diligencia_sel))
                con.commit()
                messagebox.showinfo("Sucesso", "Diligência atualizada!")
                self.dil_limpar_campos(); self.dil_listar()
            finally: cur.close(); con.close()

    def dil_excluir(self):
        sel = self.tab_dil_tree.selection()
        if not sel: messagebox.showwarning("Aviso", "Selecione um item."); return
        item_id = self.tab_dil_tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmar", "Deseja excluir a diligência?"):
            con = conectar_banco_diligencias()
            if con:
                try:
                    cur = con.cursor()
                    cur.execute("DELETE FROM tb_gestao WHERE id=%s", (item_id,))
                    con.commit()
                    self.dil_limpar_campos(); self.dil_listar()
                finally: cur.close(); con.close()

    def dil_concluir(self):
        sel = self.tab_dil_tree.selection()
        if not sel: messagebox.showwarning("Aviso", "Selecione um item."); return
        item_id = self.tab_dil_tree.item(sel[0], "values")[0]
        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT * FROM tb_gestao WHERE id=%s", (item_id,))
                reg = cur.fetchone()
                if messagebox.askyesno("Concluir", "Marcar como CONCLUÍDA e mover para o histórico?"):
                    sql = """
                        INSERT INTO tb_concluidas (id, saj, sei, diligencia, secretaria, data_envio, prazo, usuario_criacao, data_criacao, usuario_conclusao, data_conclusao)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    cur.execute(sql, (
                        reg['id'], reg['saj'], reg['sei'], reg['diligencia'], reg['secretaria'], 
                        reg['data_envio'], reg['prazo'], reg['usuario_criacao'], reg['data_criacao'], self.usuario_atual
                    ))
                    cur.execute("DELETE FROM tb_gestao WHERE id=%s", (item_id,))
                    con.commit()
                    self.dil_limpar_campos(); self.dil_listar()
            finally: cur.close(); con.close()

    def dil_abrir_concluidas(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Diligências Concluídas")
        janela.geometry("1100x420")
        janela.transient(self)

        ctk.CTkLabel(janela, text="Histórico de Concluídas (Diligência)", font=("Arial", 16, "bold")).pack(pady=10)
        tb_conc = ttk.Treeview(janela, columns=("id", "saj", "sei", "sec", "envio", "prazo", "enviado_por", "concluido_por", "conclusao"), show="headings")
        
        headers = ("ID", "SAJ", "SEI", "Secretaria", "Envio", "Prazo", "Enviado por", "Concluído por", "Data Conclusão")
        for col, t in zip(("id", "saj", "sei", "sec", "envio", "prazo", "enviado_por", "concluido_por", "conclusao"), headers):
            tb_conc.heading(col, text=t)
        tb_conc.pack(fill="both", expand=True, padx=10, pady=5)

        con = conectar_banco_diligencias()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT * FROM tb_concluidas")
                for row in cur.fetchall():
                    env = row['data_envio'].strftime('%d/%m/%Y') if hasattr(row['data_envio'], 'strftime') else ""
                    pz = row['prazo'].strftime('%d/%m/%Y') if hasattr(row['prazo'], 'strftime') else ""
                    conc = row['data_conclusao'].strftime('%d/%m/%Y %H:%M') if hasattr(row['data_conclusao'], 'strftime') else ""
                    tb_conc.insert("", "end", values=(
                        row['id'], row['saj'], row['sei'], row['secretaria'], env, pz, 
                        row['usuario_criacao'] or "N/A", row['usuario_conclusao'] or "N/A", conc
                    ))
            finally: cur.close(); con.close()

        def restaurar():
            sel = tb_conc.selection()
            if not sel: return
            item_id = tb_conc.item(sel[0], "values")[0]
            if messagebox.askyesno("Restaurar", "Restaurar para a fila ativa?", parent=janela):
                c = conectar_banco_diligencias()
                if c:
                    try:
                        cr = c.cursor(dictionary=True)
                        cr.execute("SELECT * FROM tb_concluidas WHERE id=%s", (item_id,))
                        reg = cr.fetchone()
                        cr.execute("INSERT INTO tb_gestao (id, saj, sei, diligencia, secretaria, data_envio, prazo, usuario_criacao, data_criacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (reg['id'], reg['saj'], reg['sei'], reg['diligencia'], reg['secretaria'], reg['data_envio'], reg['prazo'], reg['usuario_criacao'], reg['data_criacao']))
                        cr.execute("DELETE FROM tb_concluidas WHERE id=%s", (item_id,))
                        c.commit()
                        janela.destroy(); self.dil_listar()
                    finally: cr.close(); c.close()

        if self.perfil_atual == 'admin':
            ctk.CTkButton(janela, text="↩ Restaurar Selecionada (Admin)", command=restaurar, fg_color="#b37400", hover_color="orange").pack(pady=10)
        else:
            ctk.CTkLabel(janela, text="* Apenas usuários administradores podem restaurar processos concluídos.", text_color="gray").pack(pady=10)


    # ==========================================
    # 2. LOTAÇÃO USUCAPIÃO
    # ==========================================
    def montar_aba_usucapiao(self):
        self.f_form_usu = ctk.CTkFrame(self.tab_usucapiao, width=320)
        self.f_form_usu.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.f_form_usu, text="Lotação Usucapião", font=("Arial", 18, "bold")).pack(pady=15)

        self.e_saj_usu = ctk.CTkEntry(self.f_form_usu, placeholder_text="SAJ (ex: 2025.01.24)", width=260)
        self.e_saj_usu.pack(pady=6)
        self.e_saj_usu.bind("<FocusOut>", lambda e: self.aplicar_mascara_campo(self.e_saj_usu, formatar_saj))

        self.e_sei_usu = ctk.CTkEntry(self.f_form_usu, placeholder_text="SEI (ex: 05.123/2024-01)", width=260)
        self.e_sei_usu.pack(pady=6)
        self.e_sei_usu.bind("<FocusOut>", lambda e: self.aplicar_mascara_campo(self.e_sei_usu, formatar_sei))

        self.e_interessado_usu = ctk.CTkEntry(self.f_form_usu, placeholder_text="Interessado", width=260)
        self.e_interessado_usu.pack(pady=6)

        self.e_sec_usu = ctk.CTkEntry(self.f_form_usu, placeholder_text="Secretarias (ex: SEMOC, SEFIN, SEDUR)", width=260)
        self.e_sec_usu.pack(pady=6)

        self.e_envio_usu = ctk.CTkEntry(self.f_form_usu, placeholder_text="Data Envio (DD/MM/AAAA)", width=260)
        self.e_envio_usu.pack(pady=6)

        ctk.CTkLabel(self.f_form_usu, text="Tipo de Solicitação:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=(4, 0))
        self.cmb_tipo_usu = ctk.CTkComboBox(self.f_form_usu, values=["Judicial", "Extrajudicial"], width=260)
        self.cmb_tipo_usu.pack(pady=4)

        ctk.CTkLabel(self.f_form_usu, text="Respostas Recebidas:", font=("Arial", 11, "bold")).pack(anchor="w", padx=30, pady=(6, 0))
        
        self.chk_sec1_var = ctk.IntVar(value=0)
        self.chk_sec2_var = ctk.IntVar(value=0)
        self.chk_sec3_var = ctk.IntVar(value=0)

        self.chk_sec1 = ctk.CTkCheckBox(self.f_form_usu, text="1ª Secretaria Respondida", variable=self.chk_sec1_var)
        self.chk_sec1.pack(anchor="w", padx=35, pady=2)
        
        self.chk_sec2 = ctk.CTkCheckBox(self.f_form_usu, text="2ª Secretaria Respondida", variable=self.chk_sec2_var)
        self.chk_sec2.pack(anchor="w", padx=35, pady=2)

        self.chk_sec3 = ctk.CTkCheckBox(self.f_form_usu, text="3ª Secretaria Respondida", variable=self.chk_sec3_var)
        self.chk_sec3.pack(anchor="w", padx=35, pady=2)

        ctk.CTkButton(self.f_form_usu, text="Salvar Novo", command=self.usu_cadastrar, fg_color="green", hover_color="darkgreen", width=260).pack(pady=10)
        ctk.CTkButton(self.f_form_usu, text="Atualizar Selecionado", command=self.usu_atualizar, fg_color="orange", hover_color="#b37400", width=260).pack(pady=4)
        ctk.CTkButton(self.f_form_usu, text="Limpar Campos", command=self.usu_limpar_campos, fg_color="gray", width=260).pack(pady=4)

        self.f_lista_usu = ctk.CTkFrame(self.tab_usucapiao)
        self.f_lista_usu.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)

        f_pesq = ctk.CTkFrame(self.f_lista_usu, fg_color="transparent")
        f_pesq.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(f_pesq, text="Buscar:", font=("Arial", 12, "bold")).pack(side="left", padx=(0, 5))
        self.e_pesq_usu = ctk.CTkEntry(f_pesq, placeholder_text="Digite SAJ, SEI, Interessado...", width=300)
        self.e_pesq_usu.pack(side="left", fill="x", expand=True, padx=5)
        self.e_pesq_usu.bind("<KeyRelease>", lambda e: self.usu_listar())

        cols = ("id", "saj", "sei", "interessado", "secretarias", "envio", "tipo", "status", "enviado_por")
        self.tab_usu_tree = ttk.Treeview(self.f_lista_usu, columns=cols, show="headings", selectmode="browse")
        
        headers = ("ID", "SAJ", "SEI", "INTERESSADO", "SECRETARIAS", "ENVIO", "TIPO", "STATUS", "ENVIADO POR")
        for c, h in zip(cols, headers):
            self.tab_usu_tree.heading(c, text=h)

        self.tab_usu_tree.column("id", width=30, anchor="center")
        self.tab_usu_tree.column("saj", width=110)
        self.tab_usu_tree.column("sei", width=110)
        self.tab_usu_tree.column("interessado", width=120)
        self.tab_usu_tree.column("secretarias", width=120)
        self.tab_usu_tree.column("envio", width=75, anchor="center")
        self.tab_usu_tree.column("tipo", width=85)
        self.tab_usu_tree.column("status", width=140)
        self.tab_usu_tree.column("enviado_por", width=90)

        self.tab_usu_tree.pack(pady=10, padx=10, fill="both", expand=True)
        self.tab_usu_tree.bind("<Double-1>", self.usu_carregar_campos)

        f_act = ctk.CTkFrame(self.f_lista_usu, fg_color="transparent")
        f_act.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(f_act, text="✔ Concluir Usucapião", command=self.usu_concluir, fg_color="#1f538d", hover_color="#14375e", width=140).pack(side="left", padx=5)
        ctk.CTkButton(f_act, text="Ver Concluídas", command=self.usu_abrir_concluidas, fg_color="#454545", hover_color="#2b2b2b", width=120).pack(side="left", padx=5)
        ctk.CTkButton(f_act, text="✖ Excluir", command=self.usu_excluir, fg_color="red", hover_color="darkred", width=120).pack(side="right", padx=5)

        self.usu_listar()

    def calcular_status_usucapiao(self, s1, s2, s3):
        total = sum([s1, s2, s3])
        if total == 3: return "Pronto p/ Concluir (3/3)"
        elif total > 0: return f"Pendente ({total}/3 respondidas)"
        return "Aguardando (0/3 respondidas)"

    def usu_limpar_campos(self):
        self.id_usucapiao_sel = None
        for e in (self.e_saj_usu, self.e_sei_usu, self.e_interessado_usu, self.e_sec_usu, self.e_envio_usu):
            e.delete(0, 'end')
        self.cmb_tipo_usu.set("Judicial")
        self.chk_sec1_var.set(0); self.chk_sec2_var.set(0); self.chk_sec3_var.set(0)

    def usu_cadastrar(self):
        self.aplicar_mascara_campo(self.e_saj_usu, formatar_saj)
        self.aplicar_mascara_campo(self.e_sei_usu, formatar_sei)

        saj, sei = self.e_saj_usu.get(), self.e_sei_usu.get()
        interessado = self.e_interessado_usu.get()
        secretarias = self.e_sec_usu.get()
        tipo = self.cmb_tipo_usu.get()

        if not saj or not interessado:
            messagebox.showwarning("Aviso", "SAJ e Interessado são obrigatórios!"); return

        envio_fmt, e_err = formatar_e_validar_data(self.e_envio_usu.get())
        if e_err: messagebox.showwarning("Data Envio", e_err); return

        s1, s2, s3 = self.chk_sec1_var.get(), self.chk_sec2_var.get(), self.chk_sec3_var.get()
        status_txt = self.calcular_status_usucapiao(s1, s2, s3)

        con = conectar_banco_usucapiao()
        if con:
            try:
                cur = con.cursor()
                sql = """
                    INSERT INTO tb_usucapiao (saj, sei, interessado, secretarias, data_envio, tipo_solicitacao, sec1_ok, sec2_ok, sec3_ok, status, usuario_criacao, data_criacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """
                cur.execute(sql, (saj, sei, interessado, secretarias, envio_fmt, tipo, s1, s2, s3, status_txt, self.usuario_atual))
                con.commit()
                messagebox.showinfo("Sucesso", "Processo cadastrado!")
                self.usu_limpar_campos(); self.usu_listar()
            finally: cur.close(); con.close()

    def usu_listar(self):
        for item in self.tab_usu_tree.get_children(): self.tab_usu_tree.delete(item)
        busca = self.e_pesq_usu.get()
        con = conectar_banco_usucapiao()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                if busca:
                    sql = "SELECT * FROM tb_usucapiao WHERE saj LIKE %s OR sei LIKE %s OR interessado LIKE %s OR secretarias LIKE %s"
                    lk = f"%{busca}%"
                    cur.execute(sql, (lk, lk, lk, lk))
                else:
                    cur.execute("SELECT * FROM tb_usucapiao")

                for row in cur.fetchall():
                    env_str = row['data_envio'].strftime('%d/%m/%Y') if hasattr(row['data_envio'], 'strftime') else (row['data_envio'] or "")
                    self.tab_usu_tree.insert("", "end", values=(
                        row['id'], row['saj'], row['sei'], row['interessado'],
                        row['secretarias'], env_str, row['tipo_solicitacao'], row['status'], row['usuario_criacao'] or "N/A"
                    ))
            finally: cur.close(); con.close()

    def usu_carregar_campos(self, event):
        sel = self.tab_usu_tree.selection()
        if sel:
            v = self.tab_usu_tree.item(sel[0], "values")
            self.id_usucapiao_sel = v[0]
            con = conectar_banco_usucapiao()
            if con:
                try:
                    cur = con.cursor(dictionary=True)
                    cur.execute("SELECT * FROM tb_usucapiao WHERE id=%s", (self.id_usucapiao_sel,))
                    reg = cur.fetchone()
                    if reg:
                        self.e_saj_usu.delete(0, 'end'); self.e_saj_usu.insert(0, reg['saj'])
                        self.e_sei_usu.delete(0, 'end'); self.e_sei_usu.insert(0, reg['sei'])
                        self.e_interessado_usu.delete(0, 'end'); self.e_interessado_usu.insert(0, reg['interessado'])
                        self.e_sec_usu.delete(0, 'end'); self.e_sec_usu.insert(0, reg['secretarias'])
                        
                        env_str = reg['data_envio'].strftime('%d/%m/%Y') if hasattr(reg['data_envio'], 'strftime') else (reg['data_envio'] or "")
                        self.e_envio_usu.delete(0, 'end'); self.e_envio_usu.insert(0, env_str)
                        
                        self.cmb_tipo_usu.set(reg['tipo_solicitacao'])
                        self.chk_sec1_var.set(reg['sec1_ok'])
                        self.chk_sec2_var.set(reg['sec2_ok'])
                        self.chk_sec3_var.set(reg['sec3_ok'])
                finally: cur.close(); con.close()

    def usu_atualizar(self):
        if not self.id_usucapiao_sel: messagebox.showwarning("Aviso", "Selecione um processo."); return
        self.aplicar_mascara_campo(self.e_saj_usu, formatar_saj)
        self.aplicar_mascara_campo(self.e_sei_usu, formatar_sei)

        envio_fmt, e_err = formatar_e_validar_data(self.e_envio_usu.get())
        if e_err: messagebox.showwarning("Data Envio", e_err); return

        s1, s2, s3 = self.chk_sec1_var.get(), self.chk_sec2_var.get(), self.chk_sec3_var.get()
        status_txt = self.calcular_status_usucapiao(s1, s2, s3)

        con = conectar_banco_usucapiao()
        if con:
            try:
                cur = con.cursor()
                sql = """
                    UPDATE tb_usucapiao 
                    SET saj=%s, sei=%s, interessado=%s, secretarias=%s, data_envio=%s, tipo_solicitacao=%s, sec1_ok=%s, sec2_ok=%s, sec3_ok=%s, status=%s
                    WHERE id=%s
                """
                cur.execute(sql, (
                    self.e_saj_usu.get(), self.e_sei_usu.get(), self.e_interessado_usu.get(),
                    self.e_sec_usu.get(), envio_fmt, self.cmb_tipo_usu.get(), s1, s2, s3, status_txt, self.id_usucapiao_sel
                ))
                con.commit()
                messagebox.showinfo("Sucesso", "Processo atualizado!")
                self.usu_limpar_campos(); self.usu_listar()
            finally: cur.close(); con.close()

    def usu_excluir(self):
        sel = self.tab_usu_tree.selection()
        if not sel: messagebox.showwarning("Aviso", "Selecione um processo."); return
        item_id = self.tab_usu_tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir?"):
            con = conectar_banco_usucapiao()
            if con:
                try:
                    cur = con.cursor()
                    cur.execute("DELETE FROM tb_usucapiao WHERE id=%s", (item_id,))
                    con.commit()
                    self.usu_limpar_campos(); self.usu_listar()
                finally: cur.close(); con.close()

    def usu_concluir(self):
        sel = self.tab_usu_tree.selection()
        if not sel: messagebox.showwarning("Aviso", "Selecione um processo."); return
        item_id = self.tab_usu_tree.item(sel[0], "values")[0]

        con = conectar_banco_usucapiao()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT * FROM tb_usucapiao WHERE id=%s", (item_id,))
                reg = cur.fetchone()

                if reg['sec1_ok'] + reg['sec2_ok'] + reg['sec3_ok'] < 3:
                    if not messagebox.askyesno("Respostas Pendentes", "Nem todas as secretarias responderam. Concluir mesmo assim?"): return

                if messagebox.askyesno("Concluir Usucapião", "Marcar como CONCLUÍDO e mover para o histórico?"):
                    sql = """
                        INSERT INTO tb_usucapiao_concluidas (id, saj, sei, interessado, secretarias, data_envio, tipo_solicitacao, usuario_criacao, data_criacao, usuario_conclusao, data_conclusao)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """
                    cur.execute(sql, (
                        reg['id'], reg['saj'], reg['sei'], reg['interessado'], reg['secretarias'], 
                        reg['data_envio'], reg['tipo_solicitacao'], reg['usuario_criacao'], reg['data_criacao'], self.usuario_atual
                    ))
                    cur.execute("DELETE FROM tb_usucapiao WHERE id=%s", (item_id,))
                    con.commit()
                    self.usu_limpar_campos(); self.usu_listar()
            finally: cur.close(); con.close()

    def usu_abrir_concluidas(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Usucapião - Histórico de Concluídas")
        janela.geometry("1100x420")
        janela.transient(self)

        ctk.CTkLabel(janela, text="Histórico de Usucapião Concluídos", font=("Arial", 16, "bold")).pack(pady=10)
        tb_conc = ttk.Treeview(janela, columns=("id", "saj", "sei", "interessado", "sec", "envio", "tipo", "enviado_por", "concluido_por", "conclusao"), show="headings")
        
        headers = ("ID", "SAJ", "SEI", "Interessado", "Secretarias", "Envio", "Tipo", "Enviado por", "Concluído por", "Data Conclusão")
        for col, t in zip(("id", "saj", "sei", "interessado", "sec", "envio", "tipo", "enviado_por", "concluido_por", "conclusao"), headers):
            tb_conc.heading(col, text=t)
            
        tb_conc.pack(fill="both", expand=True, padx=10, pady=5)

        con = conectar_banco_usucapiao()
        if con:
            try:
                cur = con.cursor(dictionary=True)
                cur.execute("SELECT * FROM tb_usucapiao_concluidas")
                for row in cur.fetchall():
                    env = row['data_envio'].strftime('%d/%m/%Y') if hasattr(row['data_envio'], 'strftime') else ""
                    conc = row['data_conclusao'].strftime('%d/%m/%Y %H:%M') if hasattr(row['data_conclusao'], 'strftime') else ""
                    tb_conc.insert("", "end", values=(
                        row['id'], row['saj'], row['sei'], row['interessado'], row['secretarias'], 
                        env, row['tipo_solicitacao'], row['usuario_criacao'] or "N/A", row['usuario_conclusao'] or "N/A", conc
                    ))
            finally: cur.close(); con.close()

        def restaurar():
            sel = tb_conc.selection()
            if not sel: return
            item_id = tb_conc.item(sel[0], "values")[0]
            if messagebox.askyesno("Restaurar", "Devolver este processo para a fila ativa de Usucapião?", parent=janela):
                c = conectar_banco_usucapiao()
                if c:
                    try:
                        cr = c.cursor(dictionary=True)
                        cr.execute("SELECT * FROM tb_usucapiao_concluidas WHERE id=%s", (item_id,))
                        reg = cr.fetchone()
                        
                        sql = """
                            INSERT INTO tb_usucapiao (id, saj, sei, interessado, secretarias, data_envio, tipo_solicitacao, sec1_ok, sec2_ok, sec3_ok, status, usuario_criacao, data_criacao)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, 1, 1, 1, 'Restaurado (3/3)', %s, %s)
                        """
                        cr.execute(sql, (
                            reg['id'], reg['saj'], reg['sei'], reg['interessado'], reg['secretarias'], 
                            reg['data_envio'], reg['tipo_solicitacao'], reg['usuario_criacao'], reg['data_criacao']
                        ))
                        cr.execute("DELETE FROM tb_usucapiao_concluidas WHERE id=%s", (item_id,))
                        c.commit()
                        janela.destroy(); self.usu_listar()
                    finally: cr.close(); c.close()

        if self.perfil_atual == 'admin':
            ctk.CTkButton(janela, text="↩ Restaurar Selecionado (Admin)", command=restaurar, fg_color="#b37400", hover_color="orange").pack(pady=10)
        else:
            ctk.CTkLabel(janela, text="* Apenas usuários administradores podem restaurar processos concluídos.", text_color="gray").pack(pady=10)

#============================
# INICIALIZAÇÃO COM LAÇO DE LOGOUT
#============================
if __name__ == "__main__":
    while True:
        login_app = TelaLogin()
        login_app.mainloop()

        if login_app.usuario_logado:
            app = Aplicativo(usuario_atual=login_app.usuario_logado, perfil_atual=login_app.perfil_logado)
            app.mainloop()

            # Se fechou a janela pelo botão de Logout, reabre a tela de login
            if not app.deseja_fazer_logout:
                break
        else:
            break