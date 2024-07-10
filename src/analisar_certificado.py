import tkinter as tk
from tkinter import filedialog
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def formatar_cnpj(cnpj):
    cnpj_formatado = "".join(filter(str.isdigit, cnpj))
    cnpj_formatado = f"{cnpj_formatado[:2]}.{cnpj_formatado[2:5]}.{cnpj_formatado[5:8]}/{cnpj_formatado[8:12]}-{cnpj_formatado[12:]}"
    return cnpj_formatado

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
        cnpj = cn[cnpj_posicao:].strip()
        text_output.insert(tk.END, f"CNPJ encontrado: {formatar_cnpj(cnpj)}\n")
    else:
        text_output.insert(tk.END, "CNPJ não encontrado no CN.\n")

    data_criacao_formatada = certificado.not_valid_before_utc.strftime('%Y-%m-%d')
    data_expiracao_formatada = certificado.not_valid_after_utc.strftime('%Y-%m-%d')
    text_output.insert(tk.END, f"Data de criação: {data_criacao_formatada}\n")
    text_output.insert(tk.END, f"Data de expiração: {data_expiracao_formatada}\n")

def iniciar_programa(chave_publica):
    window = tk.Tk()
    window.title("Analisar Certificado")

    text_output = tk.Text(window, height=5, width=75)
    text_output.pack()

    # Chama a função analisar_certificado após a criação do text_output
    analisar_certificado(certificado_caminho=chave_publica, text_output=text_output)

    window.mainloop()