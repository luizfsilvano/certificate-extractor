import tkinter as tk
from tkinter import filedialog, messagebox
import extrator

class InterfaceExtrator:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Extrator de Chave Pública")

        frame = tk.Frame(self.janela)
        frame.pack(padx=10, pady=10)

        self.entrada_caminho_arquivo = tk.Entry(frame, width=50)
        self.entrada_caminho_arquivo.pack(side=tk.LEFT, padx=(0,10))
        botao_selecionar_arquivo = tk.Button(frame, text="Selecionar Arquivo", command=self.selecionar_arquivo)
        botao_selecionar_arquivo.pack(side=tk.LEFT)

        self.entrada_senha = tk.Entry(frame, width=20, show="*")
        self.entrada_senha.pack(side=tk.LEFT, padx=(10,0))

        botao_extrair = tk.Button(self.janela, text="Extrair Chave Pública", command=self.extrair_chave_publica)
        botao_extrair.pack(pady=(10,0))

    def iniciar_interface(self):
        self.janela.mainloop()

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename()
        self.entrada_caminho_arquivo.delete(0, tk.END)
        self.entrada_caminho_arquivo.insert(0, caminho_arquivo)

    def extrair_chave_publica(self):
        caminho_arquivo = self.entrada_caminho_arquivo.get()
        senha = self.entrada_senha.get()
        try:
            extrator.extrair_chave_publica(caminho_arquivo, senha)
            messagebox.showinfo("Extração de chave pública", "Chave pública extraída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    app = InterfaceExtrator()
    app.iniciar_interface()