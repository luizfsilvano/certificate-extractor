import tkinter as tk
from tkinter import filedialog, messagebox
import extrator
import analisar_certificado
from PIL import Image, ImageTk
import sys, os

# Função para determinar se o script está sendo executado como um executável
def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, para uso em PyInstaller """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class InterfaceExtrator:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Extrator e Analisador de Certificados")
        self.janela.iconbitmap(resource_path('icon.ico'))
        self.janela.config()
        
        self.janela.resizable(False, False)

        # Adiciona o tratamento para o evento de fechamento da janela
        self.janela.protocol("WM_DELETE_WINDOW", self.on_close)

        # carrega a imagem de fundo
        self.imagem_fundo = Image.open(resource_path("v904-nunny-010-e.jpg"))
        self.imagem_fundo = self.imagem_fundo.resize((800, 600), Image.Resampling.LANCZOS)  # Ajusta o tamanho da imagem conforme necessário
        self.foto_fundo = ImageTk.PhotoImage(self.imagem_fundo)

        # Cria um Label para a imagem de fundo e o posiciona
        self.label_fundo = tk.Label(self.janela, image=self.foto_fundo)
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        self.chave_publica = None

        # Estilo padrão para botões
        estilo_botao = {'font': ('Arial', 8), 'bg': '#4CAF50', 'fg': 'white', 'relief': 'raised', 'padx': 8, 'pady': 3}

        # Frame para extração de chave pública
        frame_extracao = tk.LabelFrame(self.janela, text="Extração de Chave Pública", font=('Arial', 10, 'bold'))
        frame_extracao.pack(padx=10, pady=10, fill="x")

        self.entrada_caminho_arquivo = tk.Entry(frame_extracao, width=30, relief='sunken', font=('Arial', 10))
        self.entrada_caminho_arquivo.pack(side=tk.LEFT, padx=(5,5), pady=5)
        self.entrada_caminho_arquivo.insert(0, "Selecione um arquivo PFX...")
        self.entrada_caminho_arquivo.bind("<FocusIn>", self.remover_placeholder)
        self.entrada_caminho_arquivo.bind("<FocusOut>", self.adicionar_placeholder)
        self.entrada_caminho_arquivo.bind("<Button-1>", self.selecionar_arquivo_pfx)

        self.entrada_senha = tk.Entry(frame_extracao, width=20, relief='sunken', font=('Arial', 10), show="*")
        self.entrada_senha.pack(side=tk.LEFT, padx=(5,5), pady=5)
        self.entrada_senha.insert(0, "Senha")
        self.entrada_senha.bind("<FocusIn>", self.on_focus_in_senha)
        self.entrada_senha.bind("<FocusOut>", self.on_focus_out_senha)

        botao_extrair = tk.Button(frame_extracao, text="Extrair Chave Pública", command=self.extrair_chave_publica, **estilo_botao)
        botao_extrair.pack(side=tk.LEFT, padx=(5,5), pady=5)

        # Frame para análise de certificado
        frame_analise = tk.LabelFrame(self.janela, text="Análise de Certificado", font=('Arial', 10, 'bold'))
        frame_analise.pack(padx=10, pady=10, fill="x")

        self.entrada_chave_publica = tk.Entry(frame_analise, width=30, relief='sunken', font=('Arial', 10))
        self.entrada_chave_publica.pack(side=tk.LEFT, padx=(5,5), pady=5)
        self.entrada_chave_publica.insert(0, "Selecione um arquivo PEM...")
        self.entrada_chave_publica.bind("<FocusIn>", self.remover_placeholder)
        self.entrada_chave_publica.bind("<FocusOut>", self.adicionar_placeholder)
        self.entrada_chave_publica.bind("<Button-1>", self.selecionar_arquivo_pem)

        self.btn_analisar = tk.Button(frame_analise, text="Analisar Certificado", command=self.analisar_certificado, **estilo_botao)
        self.btn_analisar.pack(side=tk.LEFT, padx=(5,5), pady=5)

    def on_close(self):
        # Aqui você pode adicionar uma mensagem de confirmação se desejar
        # Por exemplo:
        if messagebox.askokcancel("Sair", "Você realmente deseja sair?"):
            self.janela.destroy() 

    def iniciar_interface(self):
        self.janela.mainloop()

    def on_focus_in_senha(self, event):
        if self.entrada_senha.get() == self.placeholder_senha:
            self.entrada_senha.delete(0, tk.END)  # Remove o placeholder
            self.entrada_senha.config(show="*")  # Restaura a ocultação dos caracteres
    
    def on_focus_out_senha(self, event):
        if not self.entrada_senha.get():
            self.entrada_senha.config(show="")  # Remove a ocultação dos caracteres
            self.entrada_senha.insert(0, self.placeholder_senha)  # Adiciona o placeholder


    def remover_placeholder(self, event):
        widget = event.widget
        if widget == self.entrada_senha and widget.get() == self.placeholder_senha:
            widget.delete(0, tk.END)  # Remove o placeholder
            widget.config(show="*")  # Restaura a ocultação de caracteres
        elif widget.get() == self.placeholder_text:
            widget.delete(0, tk.END)  # Remove o placeholder para outros campos


    def adicionar_placeholder(self, event):
        widget = event.widget
        if widget == self.entrada_senha and not widget.get():
            widget.config(show="")  # Remove a ocultação de caracteres temporariamente
            widget.insert(0, self.placeholder_senha)  # Adiciona o placeholder
        elif not widget.get():
            widget.insert(0, self.placeholder_text)  # Adiciona o placeholder para outros campos

    def selecionar_arquivo_pfx(self, event):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PFX", "*.pfx")])
        if caminho_arquivo:
            self.entrada_caminho_arquivo.delete(0, tk.END)
            self.entrada_caminho_arquivo.insert(0, caminho_arquivo)
            self.entrada_caminho_arquivo.config(fg='black')

    def selecionar_arquivo_pem(self, event):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PEM", "*.pem")])
        if caminho_arquivo:
            self.entrada_chave_publica.delete(0, tk.END)
            self.entrada_chave_publica.insert(0, caminho_arquivo)
            self.entrada_chave_publica.config(fg='black')
            self.chave_publica = caminho_arquivo

    def extrair_chave_publica(self):
        caminho_arquivo = self.entrada_caminho_arquivo.get()
        senha = self.entrada_senha.get()
        try:
            self.chave_publica = extrator.extrair_chave_publica(caminho_arquivo, senha)
            self.entrada_chave_publica.delete(0, tk.END)
            self.entrada_chave_publica.insert(0, self.chave_publica)
            messagebox.showinfo("Extração de chave pública", "Chave pública extraída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def analisar_certificado(self):
        caminho_chave_publica = self.entrada_chave_publica.get()
        if not caminho_chave_publica or caminho_chave_publica == "Selecione um arquivo PEM...":
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo de chave pública PEM.")
            return
        try:
            analisar_certificado.iniciar_programa(caminho_chave_publica)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao analisar o certificado: {str(e)}")

if __name__ == "__main__":
    app = InterfaceExtrator()
    app.iniciar_interface()