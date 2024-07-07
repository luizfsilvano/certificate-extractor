import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

def extrair_chave_publica(caminho_certificado, senha):
    if not os.path.exists(caminho_certificado):
        raise FileNotFoundError(f"O arquivo {caminho_certificado} não foi encontrado.")
    
    with open(caminho_certificado, "rb") as f:
        certificado_pfx = f.read()

    try:
        chave_privada, certificado, cadeia_certificados = pkcs12.load_key_and_certificates(
            certificado_pfx, senha.encode(), default_backend()
        )
    except ValueError as e:
        raise ValueError("Senha incorreta ou arquivo de certificado inválido.")
    
    if certificado is None:
        raise ValueError("Não foi possível extrair o certificado do arquivo PKCS#12.")
    
    certificado_pem = certificado.public_bytes(
        encoding=serialization.Encoding.PEM
    )

    caminho_certificado_pem = os.path.splitext(caminho_certificado)[0] + "_public.pem"

    with open(caminho_certificado_pem, 'wb') as f:
        f.write(certificado_pem)

    return caminho_certificado_pem