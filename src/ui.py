import tkinter as tk
from tkinter import filedialog, messagebox
import extrator
import analisar_certificado
from PIL import Image, ImageTk

class InterfaceExtrator:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Extrator de Chave Pública")
        self.janela.iconbitmap('img/icon.ico')
        self.janela.config()
        
        # self.janela.maxsize(800, 600)
        self.janela.resizable(False, False)

        # Adiciona o tratamento para o evento de fechamento da janela
        self.janela.protocol("WM_DELETE_WINDOW", self.on_close)

        # carrega a imagem de fundo
        self.imagem_fundo = Image.open("img/v904-nunny-010-e.jpg")
        self.imagem_fundo = self.imagem_fundo.resize((800, 600), Image.Resampling.LANCZOS)  # Ajusta o tamanho da imagem conforme necessário
        self.foto_fundo = ImageTk.PhotoImage(self.imagem_fundo)

        # Cria um Label para a imagem de fundo e o posiciona
        self.label_fundo = tk.Label(self.janela, image=self.foto_fundo)
        self.label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        frame = tk.Frame(self.janela)
        frame.pack(padx=10, pady=10)

        self.placeholder_text = "Selecione um arquivo..."
        self.entrada_caminho_arquivo = tk.Entry(frame, width=30, relief='flat', font=('Arial', 10))
        self.entrada_caminho_arquivo.pack(side=tk.LEFT, padx=(0,10))
        self.entrada_caminho_arquivo.insert(0, self.placeholder_text)
        self.entrada_caminho_arquivo.bind("<FocusIn>", self.remover_placeholder)
        self.entrada_caminho_arquivo.bind("<FocusOut>", self.adicionar_placeholder)
        self.entrada_caminho_arquivo.bind("<Button-1>", self.selecionar_arquivo)

        # Configuração do campo de senha
        self.placeholder_senha = "Digite sua senha..."
        self.entrada_senha = tk.Entry(self.janela, width=20, relief='flat', font=('Arial', 10))
        self.entrada_senha.insert(0, self.placeholder_senha)
        self.entrada_senha.bind("<FocusIn>", self.on_focus_in_senha)
        self.entrada_senha.bind("<FocusOut>", self.on_focus_out_senha)
        self.entrada_senha.pack()

        botao_extrair = tk.Button(self.janela, text="Extrair Chave Pública", command=self.extrair_chave_publica, font=('Arial', 10), relief='flat')
        botao_extrair.pack(pady=(10,10))

        # Botão Analisar Certificado (agora visível desde o início)
        self.btn_analisar = tk.Button(self.janela, text="Analisar Certificado", command=self.analisar_certificado, font=('Arial', 10), relief='flat')

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

    def selecionar_arquivo(self, event):
        caminho_arquivo = filedialog.askopenfilename()
        if caminho_arquivo:  # Verifica se um arquivo foi selecionado
            self.entrada_caminho_arquivo.delete(0, tk.END)
            self.entrada_caminho_arquivo.insert(0, caminho_arquivo)
            self.entrada_caminho_arquivo.config(fg='black')

    def extrair_chave_publica(self):
        caminho_arquivo = self.entrada_caminho_arquivo.get()
        senha = self.entrada_senha.get()
        try:
            chave_publica = extrator.extrair_chave_publica(caminho_arquivo, senha)
            self.chave_publica = chave_publica
            messagebox.showinfo("Extração de chave pública", "Chave pública extraída com sucesso!")
            self.btn_analisar.pack(side=tk.TOP, pady=(0, 10))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def analisar_certificado(self):
        # Supondo que a chave pública esteja armazenada em self.chave_publica
        try:
            if hasattr(self, 'chave_publica'):
                resultado_analise = analisar_certificado.iniciar_programa(self.chave_publica)
                messagebox.showinfo("Análise de certificado", resultado_analise)
        except Exception as e:      
            messagebox.showerror("Erro", str(e))


if __name__ == "__main__":
    app = InterfaceExtrator()
    app.iniciar_interface()