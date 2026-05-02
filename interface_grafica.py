import tkinter as tk
from tkinter import ttk, messagebox
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Carrega as credenciais
load_dotenv()
URL_BASE = "https://api-ib22.onrender.com"
USUARIO = os.getenv("API_USER")
SENHA = os.getenv("API_PASSWORD")

class AppBrasileirao:
    def __init__(self, root):
        self.root = root
        self.root.title("Brasileirão API - Dashboard Desktop")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")

        # Estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", rowheight=25)
        self.style.map("Treeview", background=[('selected', '#0078d7')])

        self.criar_widgets()
        self.atualizar_tabela()

    def criar_widgets(self):
        # Frame de Busca
        frame_busca = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        frame_busca.pack(fill="x", padx=20)

        tk.Label(frame_busca, text="Buscar Time:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(side="left")
        self.ent_busca = tk.Entry(frame_busca, font=("Arial", 10))
        self.ent_busca.pack(side="left", padx=10, expand=True, fill="x")
        
        btn_busca = tk.Button(frame_busca, text="Buscar", command=self.buscar_time, bg="#0078d7", fg="white", font=("Arial", 9, "bold"), padx=15)
        btn_busca.pack(side="left")

        # Tabela (Treeview)
        frame_tabela = tk.Frame(self.root)
        frame_tabela.pack(expand=True, fill="both", padx=20, pady=10)

        colunas = ("posicao", "time", "pontos", "gols_f", "gols_s", "saldo")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        
        self.tree.heading("posicao", text="Pos")
        self.tree.heading("time", text="Time")
        self.tree.heading("pontos", text="Pts")
        self.tree.heading("gols_f", text="GP")
        self.tree.heading("gols_s", text="GC")
        self.tree.heading("saldo", text="SG")

        self.tree.column("posicao", width=50, anchor="center")
        self.tree.column("time", width=200)
        self.tree.column("pontos", width=60, anchor="center")
        self.tree.column("gols_f", width=60, anchor="center")
        self.tree.column("gols_s", width=60, anchor="center")
        self.tree.column("saldo", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

        # Botão Atualizar
        btn_refresh = tk.Button(self.root, text="🔄 Atualizar Tabela", command=self.atualizar_tabela, bg="#28a745", fg="white", font=("Arial", 10, "bold"))
        btn_refresh.pack(pady=10)

    def atualizar_tabela(self):
        try:
            response = requests.get(f"{URL_BASE}/tabela", auth=HTTPBasicAuth(USUARIO, SENHA))
            if response.status_code == 200:
                # Limpa tabela
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                dados = response.json()
                for time in dados:
                    self.tree.insert("", "end", values=(
                        f"{time['posicao']}º",
                        time['time'],
                        time['pontos'],
                        time['gols_feitos'],
                        time['gols_sofridos'],
                        time['saldo_gols']
                    ))
            else:
                messagebox.showerror("Erro", "Falha na autenticação ou API fora do ar.")
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

    def buscar_time(self):
        nome = self.ent_busca.get()
        if not nome:
            return
        
        try:
            response = requests.get(f"{URL_BASE}/time/{nome}", auth=HTTPBasicAuth(USUARIO, SENHA))
            if response.status_code == 200:
                t = response.json()
                msg = f"Time: {t['time']}\nPosição: {t['posicao']}º\nPontos: {t['pontos']}\nSaldo: {t['saldo_gols']}"
                messagebox.showinfo("Resultado da Busca", msg)
            else:
                messagebox.showwarning("Aviso", "Time não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AppBrasileirao(root)
    root.mainloop()
