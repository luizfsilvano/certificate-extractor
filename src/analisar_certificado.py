import tkinter as tk
from tkinter import filedialog
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
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

def formatar_cnpj(cnpj):
    cnpj_formatado = "".join(filter(str.isdigit, cnpj))
    cnpj_formatado = f"{cnpj_formatado[:2]}.{cnpj_formatado[2:5]}.{cnpj_formatado[5:8]}/{cnpj_formatado[8:12]}-{cnpj_formatado[12:]}"
    return cnpj_formatado

def formatar_cpf(cpf):
    cpf_formatado = "".join(filter(str.isdigit, cpf))
    cpf_formatado = f"{cpf_formatado[:3]}.{cpf_formatado[3:6]}.{cpf_formatado[6:9]}-{cpf_formatado[9:]}"
    return cpf_formatado


def analisar_certificado(certificado_caminho, text_output):
    with open(certificado_caminho, 'rb') as cert_file:
        certificado_dados = cert_file.read()
        certificado = x509.load_pem_x509_certificate(certificado_dados, default_backend())

    text_output.delete(1.0, tk.END)

    for extension in certificado.extensions:
        if extension.oid._name == "certificatePolicies":
            for policy in extension.value:
                if "2.16.76.1.2.1" in policy.policy_identifier.dotted_string:
                    text_output.insert(tk.END, "O certificado é ICP Brasil\n")
                    break
            else:
                text_output.insert(tk.END, "O certificado não é ICP Brasil\n")
            break

    subject = certificado.subject
    cn = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    text_output.insert(tk.END, f"Valor do CN encontrado: {cn}\n")

    cnpj_posicao = cn.find(":") + 1
    if cnpj_posicao > 0:
        identificador = cn[cnpj_posicao:].strip()
        if len(identificador) == 14:
            text_output.insert(tk.END, f"CNPJ encontrado: {formatar_cnpj(identificador)}\n")
        elif len(identificador) == 11:
            text_output.insert(tk.END, f"CPF encontrado: {formatar_cpf(identificador)}\n")
        else:
            text_output.insert(tk.END, "Identificador não reconhecido.\n")
    else:
        text_output.insert(tk.END, "CNPJ ou CPF não encontrado no CN.\n")

    data_criacao_formatada = certificado.not_valid_before_utc.strftime('%Y-%m-%d')
    data_expiracao_formatada = certificado.not_valid_after_utc.strftime('%Y-%m-%d')
    text_output.insert(tk.END, f"Data de criação: {data_criacao_formatada}\n")
    text_output.insert(tk.END, f"Data de expiração: {data_expiracao_formatada}\n")

def iniciar_programa(chave_publica):
    window = tk.Tk()
    window.title("Analisar Certificado")
    window.iconbitmap(resource_path('icon.ico'))

    window.resizable(False, False)

    text_output = tk.Text(window, height=5, width=75, font=("Arial", 10))
    text_output.pack()

    # Chama a função analisar_certificado após a criação do text_output
    analisar_certificado(certificado_caminho=chave_publica, text_output=text_output)

    window.mainloop()