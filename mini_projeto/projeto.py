# -*- coding: utf-8 -*-
"""
Sistema de Gestão de Diligências
=================================
Aplicação desktop em Python + Tkinter para cadastro e acompanhamento de
diligências judiciais/administrativas, com controle de prazos e emissão
automática de texto de cobrança para diligências em atraso.

Requisitos: apenas biblioteca padrão do Python (tkinter e sqlite3).
Execução:  python3 gestao_diligencias.py
"""

import os
import re
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --------------------------------------------------------------------------- #
# CONFIGURAÇÕES GERAIS
# --------------------------------------------------------------------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "diligencias.db")

SECRETARIAS_SUGESTOES = [
    "1ª Vara Cível", "2ª Vara Cível", "1ª Vara de Família",
    "2ª Vara de Família", "Vara da Fazenda Pública", "Vara Criminal",
    "Juizado Especial Cível", "Juizado Especial Criminal",
    "Vara do Trabalho", "Secretaria Administrativa",
]

TEMPLATE_COBRANCA = """Prezado(a) {quem_recebeu},

Vimos, por meio deste, cobrar o cumprimento da diligência abaixo identificada,
tendo em vista que o prazo estabelecido já se encontra vencido.

    Processo SAJ nº: {saj}
    Processo SEI nº: {sei}
    Secretaria de origem: {secretaria}
    Data de envio: {data_envio}
    Prazo estabelecido: {prazo}
    Dias em atraso: {dias_atraso}
    Diligência enviada por: {quem_mandou}
    Diligência destinada a: {quem_recebeu}

Solicitamos a URGENTE regularização e o retorno quanto ao andamento da
referida diligência, evitando-se prejuízos ao regular trâmite processual.

Atenciosamente,
{quem_mandou}
"""

# --------------------------------------------------------------------------- #
# BANCO DE DADOS
# --------------------------------------------------------------------------- #

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_banco():
    conn = conectar()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS diligencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            saj TEXT,
            sei TEXT,
            secretaria TEXT NOT NULL,
            data_envio TEXT NOT NULL,
            prazo TEXT NOT NULL,
            quem_mandou TEXT NOT NULL,
            quem_recebeu TEXT NOT NULL,
            cumprida INTEGER NOT NULL DEFAULT 0,
            data_cumprimento TEXT
        )
    """)
    conn.commit()
    conn.close()


# --------------------------------------------------------------------------- #
# FUNÇÕES DE MÁSCARA / VALIDAÇÃO
# --------------------------------------------------------------------------- #

def aplicar_mascara(digitos, grupos, separadores):
    """Recebe apenas dígitos e devolve a string formatada de acordo com os
    tamanhos de grupos definidos e os separadores entre eles."""
    resultado = ""
    pos = 0
    for i, tamanho in enumerate(grupos):
        parte = digitos[pos:pos + tamanho]
        if not parte:
            break
        resultado += parte
        pos += tamanho
        if pos >= len(digitos):
            break
        if i < len(separadores):
            resultado += separadores[i]
    return resultado


def total_digitos(grupos):
    return sum(grupos)


class EntradaMascarada(ttk.Entry):
    """Entry do Tkinter que aplica uma máscara numérica automaticamente
    enquanto o usuário digita (ex.: SAJ, SEI, datas)."""

    def __init__(self, master, grupos, separadores, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grupos = grupos
        self.separadores = separadores
        self.max_digitos = total_digitos(grupos)
        self.bind("<KeyRelease>", self._on_key_release)

    def _on_key_release(self, event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Tab"):
            return
        texto_atual = self.get()
        digitos = re.sub(r"\D", "", texto_atual)[: self.max_digitos]
        novo_texto = aplicar_mascara(digitos, self.grupos, self.separadores)
        if novo_texto != texto_atual:
            self.delete(0, tk.END)
            self.insert(0, novo_texto)
            self.icursor(tk.END)

    def get_digitos(self):
        return re.sub(r"\D", "", self.get())

    def esta_completo_ou_vazio(self):
        d = self.get_digitos()
        return len(d) == 0 or len(d) == self.max_digitos


# Definições de máscara específicas
MASCARA_SAJ = dict(grupos=[4, 2, 6], separadores=[".", "."])          # 0000.00.000000
MASCARA_SEI = dict(grupos=[2, 6, 4, 2], separadores=[".", "/", "-"])   # 00.000000/0000-00
MASCARA_DATA = dict(grupos=[2, 2, 4], separadores=["/", "/"])          # dd/mm/aaaa


def validar_data(texto):
    """Valida se o texto está no formato dd/mm/aaaa e é uma data real."""
    try:
        datetime.strptime(texto.strip(), "%d/%m/%Y")
        return True
    except ValueError:
        return False


def data_para_datetime(texto):
    return datetime.strptime(texto.strip(), "%d/%m/%Y")


# --------------------------------------------------------------------------- #
# APLICAÇÃO PRINCIPAL
# --------------------------------------------------------------------------- #

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Diligências")
        self.geometry("1150x650")
        self.minsize(1000, 600)

        self.id_em_edicao = None  # controla se o formulário está editando um registro existente

        self._configurar_estilo()
        self._montar_layout()
        self.atualizar_todas_as_listas()

    # ------------------------------------------------------------------ #
    # ESTILO
    # ------------------------------------------------------------------ #
    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("TNotebook.Tab", padding=[14, 6])
        estilo.configure("Atraso.TButton", foreground="white", background="#c0392b")
        estilo.map("Atraso.TButton", background=[("active", "#992d22")])

    # ------------------------------------------------------------------ #
    # LAYOUT GERAL (ABAS)
    # ------------------------------------------------------------------ #
    def _montar_layout(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.aba_cadastro = ttk.Frame(self.notebook)
        self.aba_ativas = ttk.Frame(self.notebook)
        self.aba_atraso = ttk.Frame(self.notebook)

        self.notebook.add(self.aba_cadastro, text="  Cadastro de Diligência  ")
        self.notebook.add(self.aba_ativas, text="  Diligências Ativas  ")
        self.notebook.add(self.aba_atraso, text="  Diligências em Atraso  ")

        self._montar_aba_cadastro()
        self._montar_aba_ativas()
        self._montar_aba_atraso()

        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.atualizar_todas_as_listas())

    # ------------------------------------------------------------------ #
    # ABA 1 - CADASTRO
    # ------------------------------------------------------------------ #
    def _montar_aba_cadastro(self):
        frame = self.aba_cadastro

        form = ttk.LabelFrame(frame, text="Dados da Diligência")
        form.pack(fill="x", padx=10, pady=10)

        for col in range(4):
            form.columnconfigure(col, weight=1)

        # Linha 0: SAJ / SEI
        ttk.Label(form, text="SAJ (0000.00.000000):").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.ent_saj = EntradaMascarada(form, **MASCARA_SAJ, width=20)
        self.ent_saj.grid(row=0, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(form, text="SEI (00.000000/0000-00):").grid(row=0, column=2, sticky="w", padx=8, pady=6)
        self.ent_sei = EntradaMascarada(form, **MASCARA_SEI, width=22)
        self.ent_sei.grid(row=0, column=3, sticky="w", padx=8, pady=6)

        # Linha 1: Secretaria / Data de envio
        ttk.Label(form, text="Secretaria:").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.cmb_secretaria = ttk.Combobox(form, values=SECRETARIAS_SUGESTOES, width=30)
        self.cmb_secretaria.grid(row=1, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(form, text="Data de envio (dd/mm/aaaa):").grid(row=1, column=2, sticky="w", padx=8, pady=6)
        self.ent_data_envio = EntradaMascarada(form, **MASCARA_DATA, width=14)
        self.ent_data_envio.grid(row=1, column=3, sticky="w", padx=8, pady=6)

        # Linha 2: Prazo / Quem mandou
        ttk.Label(form, text="Prazo (dd/mm/aaaa):").grid(row=2, column=0, sticky="w", padx=8, pady=6)
        self.ent_prazo = EntradaMascarada(form, **MASCARA_DATA, width=14)
        self.ent_prazo.grid(row=2, column=1, sticky="w", padx=8, pady=6)

        ttk.Label(form, text="Quem mandou a diligência:").grid(row=2, column=2, sticky="w", padx=8, pady=6)
        self.ent_quem_mandou = ttk.Entry(form, width=30)
        self.ent_quem_mandou.grid(row=2, column=3, sticky="w", padx=8, pady=6)

        # Linha 3: Quem recebeu
        ttk.Label(form, text="Quem recebeu a diligência:").grid(row=3, column=0, sticky="w", padx=8, pady=6)
        self.ent_quem_recebeu = ttk.Entry(form, width=30)
        self.ent_quem_recebeu.grid(row=3, column=1, sticky="w", padx=8, pady=6)

        # Botões de ação do formulário
        botoes = ttk.Frame(form)
        botoes.grid(row=3, column=2, columnspan=2, sticky="e", padx=8, pady=6)

        self.btn_salvar = ttk.Button(botoes, text="Salvar", command=self.salvar_diligencia)
        self.btn_salvar.pack(side="left", padx=4)

        self.btn_limpar = ttk.Button(botoes, text="Limpar", command=self.limpar_formulario)
        self.btn_limpar.pack(side="left", padx=4)

        # Lista de todas as diligências cadastradas
        lista_frame = ttk.LabelFrame(frame, text="Diligências Cadastradas (clique para editar)")
        lista_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        colunas = ("id", "saj", "sei", "secretaria", "data_envio", "prazo",
                   "quem_mandou", "quem_recebeu", "status")
        self.tree_cadastro = self._criar_treeview(lista_frame, colunas, self._titulos_colunas())
        self.tree_cadastro.bind("<<TreeviewSelect>>", self._carregar_selecionado_no_form)

        acoes_frame = ttk.Frame(frame)
        acoes_frame.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(acoes_frame, text="Marcar como cumprida",
                   command=self.marcar_como_cumprida).pack(side="left", padx=4)
        ttk.Button(acoes_frame, text="Excluir selecionada",
                   command=self.excluir_diligencia).pack(side="left", padx=4)

    def _titulos_colunas(self):
        return {
            "id": "ID", "saj": "SAJ", "sei": "SEI", "secretaria": "Secretaria",
            "data_envio": "Data Envio", "prazo": "Prazo",
            "quem_mandou": "Enviado por", "quem_recebeu": "Recebido por",
            "status": "Status",
        }

    def _criar_treeview(self, container, colunas, titulos, largura_padrao=110):
        tree = ttk.Treeview(container, columns=colunas, show="headings", height=12)
        for c in colunas:
            tree.heading(c, text=titulos.get(c, c))
            largura = 60 if c == "id" else largura_padrao
            tree.column(c, width=largura, anchor="center")
        scroll_y = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        tree.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)
        scroll_y.pack(side="right", fill="y", pady=6)
        return tree

    # ------------------------------------------------------------------ #
    # ABA 2 - DILIGÊNCIAS ATIVAS
    # ------------------------------------------------------------------ #
    def _montar_aba_ativas(self):
        frame = self.aba_ativas
        ttk.Label(frame, text="Diligências dentro do prazo (não cumpridas)",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 4))

        colunas = ("id", "saj", "sei", "secretaria", "data_envio", "prazo",
                   "dias_restantes", "quem_mandou", "quem_recebeu")
        titulos = self._titulos_colunas()
        titulos["dias_restantes"] = "Dias restantes"

        lista_frame = ttk.Frame(frame)
        lista_frame.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree_ativas = self._criar_treeview(lista_frame, colunas, titulos)

        ttk.Button(frame, text="Atualizar lista",
                   command=self.atualizar_todas_as_listas).pack(anchor="e", padx=10, pady=(0, 10))

    # ------------------------------------------------------------------ #
    # ABA 3 - DILIGÊNCIAS EM ATRASO
    # ------------------------------------------------------------------ #
    def _montar_aba_atraso(self):
        frame = self.aba_atraso
        ttk.Label(frame, text="Diligências com prazo vencido (não cumpridas)",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 4))

        colunas = ("id", "saj", "sei", "secretaria", "data_envio", "prazo",
                   "dias_atraso", "quem_mandou", "quem_recebeu")
        titulos = self._titulos_colunas()
        titulos["dias_atraso"] = "Dias em atraso"

        lista_frame = ttk.Frame(frame)
        lista_frame.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree_atraso = self._criar_treeview(lista_frame, colunas, titulos)

        acoes = ttk.Frame(frame)
        acoes.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(acoes, text="Atualizar lista",
                   command=self.atualizar_todas_as_listas).pack(side="left", padx=4)
        ttk.Button(acoes, text="COBRAR DILIGÊNCIA SELECIONADA", style="Atraso.TButton",
                   command=self.gerar_cobranca).pack(side="left", padx=4)

    # ------------------------------------------------------------------ #
    # LÓGICA - CADASTRO / EDIÇÃO / EXCLUSÃO
    # ------------------------------------------------------------------ #
    def _ler_formulario(self):
        saj = self.ent_saj.get().strip()
        sei = self.ent_sei.get().strip()
        secretaria = self.cmb_secretaria.get().strip()
        data_envio = self.ent_data_envio.get().strip()
        prazo = self.ent_prazo.get().strip()
        quem_mandou = self.ent_quem_mandou.get().strip()
        quem_recebeu = self.ent_quem_recebeu.get().strip()
        return saj, sei, secretaria, data_envio, prazo, quem_mandou, quem_recebeu

    def _validar_formulario(self, saj, sei, secretaria, data_envio, prazo, quem_mandou, quem_recebeu):
        erros = []

        if saj and not self.ent_saj.esta_completo_ou_vazio():
            erros.append("O campo SAJ está incompleto (formato esperado: 0000.00.000000).")
        if sei and not self.ent_sei.esta_completo_ou_vazio():
            erros.append("O campo SEI está incompleto (formato esperado: 00.000000/0000-00).")
        if not saj and not sei:
            erros.append("Informe pelo menos o número do SAJ ou do SEI.")
        if not secretaria:
            erros.append("Informe a Secretaria.")
        if not data_envio or not validar_data(data_envio):
            erros.append("Data de envio inválida. Use o formato dd/mm/aaaa.")
        if not prazo or not validar_data(prazo):
            erros.append("Prazo inválido. Use o formato dd/mm/aaaa.")
        if not quem_mandou:
            erros.append("Informe quem mandou a diligência.")
        if not quem_recebeu:
            erros.append("Informe quem recebeu a diligência.")

        if not erros and data_envio and prazo and validar_data(data_envio) and validar_data(prazo):
            if data_para_datetime(prazo) < data_para_datetime(data_envio):
                erros.append("O prazo não pode ser anterior à data de envio.")

        return erros

    def salvar_diligencia(self):
        dados = self._ler_formulario()
        erros = self._validar_formulario(*dados)
        if erros:
            messagebox.showerror("Verifique os dados", "\n".join(f"• {e}" for e in erros))
            return

        saj, sei, secretaria, data_envio, prazo, quem_mandou, quem_recebeu = dados
        conn = conectar()
        if self.id_em_edicao is None:
            conn.execute("""
                INSERT INTO diligencias
                    (saj, sei, secretaria, data_envio, prazo, quem_mandou, quem_recebeu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (saj, sei, secretaria, data_envio, prazo, quem_mandou, quem_recebeu))
            mensagem = "Diligência cadastrada com sucesso!"
        else:
            conn.execute("""
                UPDATE diligencias
                   SET saj=?, sei=?, secretaria=?, data_envio=?, prazo=?,
                       quem_mandou=?, quem_recebeu=?
                 WHERE id=?
            """, (saj, sei, secretaria, data_envio, prazo, quem_mandou, quem_recebeu,
                  self.id_em_edicao))
            mensagem = "Diligência atualizada com sucesso!"
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", mensagem)
        self.limpar_formulario()
        self.atualizar_todas_as_listas()

    def limpar_formulario(self):
        self.id_em_edicao = None
        for campo in (self.ent_saj, self.ent_sei, self.ent_data_envio, self.ent_prazo,
                      self.ent_quem_mandou, self.ent_quem_recebeu):
            campo.delete(0, tk.END)
        self.cmb_secretaria.set("")
        self.btn_salvar.config(text="Salvar")
        if self.tree_cadastro.selection():
            self.tree_cadastro.selection_remove(self.tree_cadastro.selection())

    def _carregar_selecionado_no_form(self, event=None):
        selecionado = self.tree_cadastro.selection()
        if not selecionado:
            return
        valores = self.tree_cadastro.item(selecionado[0], "values")
        (id_, saj, sei, secretaria, data_envio, prazo,
         quem_mandou, quem_recebeu, _status) = valores

        self.id_em_edicao = int(id_)
        self.ent_saj.delete(0, tk.END); self.ent_saj.insert(0, saj)
        self.ent_sei.delete(0, tk.END); self.ent_sei.insert(0, sei)
        self.cmb_secretaria.set(secretaria)
        self.ent_data_envio.delete(0, tk.END); self.ent_data_envio.insert(0, data_envio)
        self.ent_prazo.delete(0, tk.END); self.ent_prazo.insert(0, prazo)
        self.ent_quem_mandou.delete(0, tk.END); self.ent_quem_mandou.insert(0, quem_mandou)
        self.ent_quem_recebeu.delete(0, tk.END); self.ent_quem_recebeu.insert(0, quem_recebeu)
        self.btn_salvar.config(text="Atualizar")

    def _id_selecionado(self, tree):
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma diligência na lista primeiro.")
            return None
        valores = tree.item(selecionado[0], "values")
        return int(valores[0])

    def excluir_diligencia(self):
        id_ = self._id_selecionado(self.tree_cadastro)
        if id_ is None:
            return
        if not messagebox.askyesno("Confirmar exclusão",
                                    "Tem certeza que deseja excluir esta diligência?"):
            return
        conn = conectar()
        conn.execute("DELETE FROM diligencias WHERE id=?", (id_,))
        conn.commit()
        conn.close()
        self.limpar_formulario()
        self.atualizar_todas_as_listas()

    def marcar_como_cumprida(self):
        id_ = self._id_selecionado(self.tree_cadastro)
        if id_ is None:
            return
        conn = conectar()
        conn.execute("""UPDATE diligencias SET cumprida=1,
                         data_cumprimento=? WHERE id=?""",
                     (datetime.now().strftime("%d/%m/%Y"), id_))
        conn.commit()
        conn.close()
        messagebox.showinfo("Ok", "Diligência marcada como cumprida.")
        self.limpar_formulario()
        self.atualizar_todas_as_listas()

    # ------------------------------------------------------------------ #
    # ATUALIZAÇÃO DAS LISTAS
    # ------------------------------------------------------------------ #
    def atualizar_todas_as_listas(self):
        conn = conectar()
        registros = conn.execute("SELECT * FROM diligencias ORDER BY id DESC").fetchall()
        conn.close()

        hoje = datetime.now()

        # --- Aba Cadastro: todas as diligências ---
        for item in self.tree_cadastro.get_children():
            self.tree_cadastro.delete(item)
        for r in registros:
            if r["cumprida"]:
                status = f"Cumprida em {r['data_cumprimento']}"
            else:
                status = "Em atraso" if data_para_datetime(r["prazo"]) < hoje else "Ativa"
            self.tree_cadastro.insert("", "end", values=(
                r["id"], r["saj"], r["sei"], r["secretaria"], r["data_envio"], r["prazo"],
                r["quem_mandou"], r["quem_recebeu"], status,
            ))

        # --- Aba Ativas ---
        for item in self.tree_ativas.get_children():
            self.tree_ativas.delete(item)
        ativas = [r for r in registros
                  if not r["cumprida"] and data_para_datetime(r["prazo"]) >= hoje]
        ativas.sort(key=lambda r: data_para_datetime(r["prazo"]))
        for r in ativas:
            dias_restantes = (data_para_datetime(r["prazo"]) - hoje).days
            self.tree_ativas.insert("", "end", values=(
                r["id"], r["saj"], r["sei"], r["secretaria"], r["data_envio"], r["prazo"],
                dias_restantes, r["quem_mandou"], r["quem_recebeu"],
            ))

        # --- Aba Atraso ---
        for item in self.tree_atraso.get_children():
            self.tree_atraso.delete(item)
        atrasadas = [r for r in registros
                     if not r["cumprida"] and data_para_datetime(r["prazo"]) < hoje]
        atrasadas.sort(key=lambda r: data_para_datetime(r["prazo"]))
        for r in atrasadas:
            dias_atraso = (hoje - data_para_datetime(r["prazo"])).days
            self.tree_atraso.insert("", "end", values=(
                r["id"], r["saj"], r["sei"], r["secretaria"], r["data_envio"], r["prazo"],
                dias_atraso, r["quem_mandou"], r["quem_recebeu"],
            ))

    # ------------------------------------------------------------------ #
    # COBRANÇA
    # ------------------------------------------------------------------ #
    def gerar_cobranca(self):
        id_ = self._id_selecionado(self.tree_atraso)
        if id_ is None:
            return

        conn = conectar()
        r = conn.execute("SELECT * FROM diligencias WHERE id=?", (id_,)).fetchone()
        conn.close()
        if r is None:
            return

        dias_atraso = (datetime.now() - data_para_datetime(r["prazo"])).days
        texto = TEMPLATE_COBRANCA.format(
            saj=r["saj"] or "não informado",
            sei=r["sei"] or "não informado",
            secretaria=r["secretaria"],
            data_envio=r["data_envio"],
            prazo=r["prazo"],
            dias_atraso=dias_atraso,
            quem_mandou=r["quem_mandou"],
            quem_recebeu=r["quem_recebeu"],
        )
        self._exibir_janela_cobranca(texto)

    def _exibir_janela_cobranca(self, texto):
        janela = tk.Toplevel(self)
        janela.title("Texto de Cobrança")
        janela.geometry("560x420")
        janela.transient(self)

        ttk.Label(janela, text="Texto padrão de cobrança gerado:",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 4))

        caixa_texto = tk.Text(janela, wrap="word", font=("Segoe UI", 10))
        caixa_texto.insert("1.0", texto)
        caixa_texto.pack(fill="both", expand=True, padx=10, pady=4)

        def copiar():
            self.clipboard_clear()
            self.clipboard_append(caixa_texto.get("1.0", "end-1c"))
            messagebox.showinfo("Copiado", "Texto de cobrança copiado para a área de transferência.")

        botoes = ttk.Frame(janela)
        botoes.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(botoes, text="Copiar texto", command=copiar).pack(side="left", padx=4)
        ttk.Button(botoes, text="Fechar", command=janela.destroy).pack(side="left", padx=4)


# --------------------------------------------------------------------------- #
# PONTO DE ENTRADA
# --------------------------------------------------------------------------- #

def main():
    inicializar_banco()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()