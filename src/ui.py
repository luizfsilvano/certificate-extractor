import tkinter as tk
from tkinter import filedialog, messagebox
import extrator
import analisar_certificado

class InterfaceExtrator:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Extrator de Chave Pública")

        frame = tk.Frame(self.janela)
        frame.pack(padx=10, pady=10)

        self.placeholder_text = "Selecione um arquivo..."
        self.entrada_caminho_arquivo = tk.Entry(frame, width=30)
        self.entrada_caminho_arquivo.pack(side=tk.LEFT, padx=(0,10))
        self.entrada_caminho_arquivo.insert(0, self.placeholder_text)
        self.entrada_caminho_arquivo.bind("<FocusIn>", self.remover_placeholder)
        self.entrada_caminho_arquivo.bind("<FocusOut>", self.adicionar_placeholder)
        self.entrada_caminho_arquivo.bind("<Button-1>", self.selecionar_arquivo)

        # Configuração do campo de senha
        self.placeholder_senha = "Digite sua senha..."
        self.entrada_senha = tk.Entry(self.janela, width=20)
        self.entrada_senha.insert(0, self.placeholder_senha)
        self.entrada_senha.bind("<FocusIn>", self.on_focus_in_senha)
        self.entrada_senha.bind("<FocusOut>", self.on_focus_out_senha)
        self.entrada_senha.pack()

        botao_extrair = tk.Button(self.janela, text="Extrair Chave Pública", command=self.extrair_chave_publica)
        botao_extrair.pack(pady=(10,0))

        # Botão Analisar Certificado (inicialmente não visível)
        self.btn_analisar = tk.Button(self.janela, text="Analisar Certificado", command=self.analisar_certificado)
        # O botão não é exibido imediatamente (não chame pack, grid ou place aqui)

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
            extrator.extrair_chave_publica(caminho_arquivo, senha)
            messagebox.showinfo("Extração de chave pública", "Chave pública extraída com sucesso!")
            sucesso = True  # Substitua isso pela sua lógica de sucesso real
            if sucesso:
                self.btn_analisar.pack(side=tk.LEFT)  # Exibe o botão ao lado do botão Extrair
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def analisar_certificado(self):
        # Aqui vai a lógica para analisar o certificado
        print("Analisando o certificado...")


if __name__ == "__main__":
    app = InterfaceExtrator()
    app.iniciar_interface()