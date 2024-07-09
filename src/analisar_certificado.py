import tkinter as tk
from tkinter import filedialog
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def formatar_cnpj(cnpj):
    # Remove caracteres não numéricos do CNPJ
    cnpj_formatado = "".join(filter(str.isdigit, cnpj))

    # Adiciona pontos e barras ao CNPJ
    cnpj_formatado = f"{cnpj_formatado[:2]}.{cnpj_formatado[2:5]}.{cnpj_formatado[5:8]}/{cnpj_formatado[8:12]}-{cnpj_formatado[12:]}"
    return cnpj_formatado

def analisar_certificado():
    # Obtém o caminho do certificado PEM selecionado pelo usuário
    certificado_caminho = filedialog.askopenfilename(filetypes=[("Certificado PEM", "*.pem")])

    # Carrega o certificado
    with open(certificado_caminho, 'rb') as cert_file:
        certificado_dados = cert_file.read()
        certificado = x509.load_pem_x509_certificate(certificado_dados, default_backend())

    # Limpa a saída anterior
    text_output.delete(1.0, tk.END)

    # Verifica se o certificado é ICP-Brasil e tenta extrair o CNPJ
    cnpj = None
    for extension in certificado.extensions:
        if extension.oid._name == "certificatePolicies":
            for policy in extension.value:
                if "2.16.76.1.2.1" in policy.policy_identifier.dotted_string:
                    text_output.insert(tk.END, "O certificado é ICP Brasil\n")
                    # Extrai o CNPJ do certificado, se disponível
                    # O CNPJ está em uma extensão específica para certificados ICP-Brasil
                    # Esta é uma simplificação, a lógica exata depende da estrutura do certificado
                    break
            else:
                text_output.insert(tk.END, "O certificado não é ICP Brasil\n")
            break

    # Obtém o valor do CN (Common Name)
    subject = certificado.subject
    cn = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    text_output.insert(tk.END, f"Valor do CN encontrado: {cn}\n")

    # Extrai o CNPJ do valor do CN, assumindo que o CNPJ está após o ":"
    cnpj_posicao = cn.find(":") + 1  # Encontra a posição do ":" e adiciona 1 para começar após o ":"
    if cnpj_posicao > 0:  # Verifica se o ":" foi encontrado
        cnpj = cn[cnpj_posicao:].strip()  # Extrai o CNPJ e remove espaços em branco
        text_output.insert(tk.END, f"CNPJ encontrado: {formatar_cnpj(cnpj)}\n")
    else:
        text_output.insert(tk.END, "CNPJ não encontrado no CN.\n")

    # Exibe as datas de criação e expiração do certificado, sem os horários
    data_criacao_formatada = certificado.not_valid_before_utc.strftime('%Y-%m-%d')
    data_expiracao_formatada = certificado.not_valid_after_utc.strftime('%Y-%m-%d')
    text_output.insert(tk.END, f"Data de criação: {data_criacao_formatada}\n")
    text_output.insert(tk.END, f"Data de expiração: {data_expiracao_formatada}\n")

# Cria a janela principal
window = tk.Tk()
window.title("Analisar Certificado")

# Configurações da janela e widgets seguem como no código original

# Cria um botão para selecionar o arquivo de certificado, atualizando o comando para analisar_certificado
btn_selecionar = tk.Button(window, text="Selecionar Certificado", command=analisar_certificado)
btn_selecionar.pack(pady=10)


# Cria um widget de texto para exibir a saída do comando
text_output = tk.Text(window, height=5, width=75)
text_output.pack()

# Inicia o loop de eventos da janela

window.mainloop()