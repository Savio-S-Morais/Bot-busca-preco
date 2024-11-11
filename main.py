# Obtenção do preço do produto
import smtplib
import pandas as pd
import requests
import json
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Acessando arquivo JSON com os dados do email origem
def variaveis_json(caminho_arquivo='dados.json'):
    with open(caminho_arquivo, 'r') as file:
        valores_json = json.load(file)
    return valores_json

import requests
from bs4 import BeautifulSoup

def obter_preco(url):
    # Fazer a requisição HTTP para o site
    response = requests.get(url)
    response.raise_for_status()  # Verifica se a requisição foi bem sucedida
    
    # Parsear o conteúdo HTML
    soup = BeautifulSoup(response.text, "lxml")
    
    elemento_preco = soup.find('p', {'class':'sc-dcJsrY eLxcFM sc-jdkBTo etFOes'})
    
    if elemento_preco:
        # Extrair o texto, removendo 'ou' e espaços adicionais
        preco_texto = elemento_preco.text.strip().replace('R$', '').replace('\xa0', ' ')
        
        # Usar uma expressão regular para capturar apenas números e a vírgula
        preco_formatado = re.sub(r'[^0-9,]', '', preco_texto)  # Remove qualquer coisa que não seja número ou vírgula
        
        # Substituir a vírgula por ponto para o formato de float
        preco_formatado = preco_formatado.replace(',', '.')
        
        try:
            # Tentar converter o valor para float
            return float(preco_formatado)
        except ValueError:
            raise ValueError(f"Não foi possível converter o preço '{preco_formatado}' para float.")
    else:
        raise ValueError("Preço não encontrado na página")

    
# Salvar o preço em uma planilha
def salvar_preco_planilha(preco, url, nome_arquivo='historico_preco.xlsx'):
    # Criar ou abrir um arquivo Excel existente
    try:
        df = pd.read_excel(nome_arquivo)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Data', 'Preço', 'URL'])
    
    # Adicionar nova linha com data e preço
    nova_linha = pd.DataFrame({
        'Data': [datetime.now().strftime('%d/%m/%Y')],
        'Preço': [preco],
        'URL': [url]
    })
    
    # Usar pd.concat() para adicionar a nova linha
    df = pd.concat([df, nova_linha], ignore_index=True)
    
    # Salvar o DataFrame no arquivo Excel
    df.to_excel(nome_arquivo, index=False)



# Enviar e-mail de alerta
def enviar_alerta_email(preco, url, email_destino, email_origem, senha_origem):
    assunto = "Alerta de Preço Atingido"
    corpo = f"O preco do produto {url} atingiu R${preco:.2f}.\n\nVerifique o site."
    
    # Configuração do servidor SMTP
    servidor = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    servidor.login(email_origem, senha_origem)
    
    # Criar o e-mail
    mensagem = MIMEMultipart()
    mensagem['From'] = email_origem
    mensagem['To'] = email_destino
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))
    
    # Enviar e-mail
    servidor.sendmail(email_origem, email_destino, mensagem.as_string())
    servidor.quit()
    
    
# Lógica de verificação de preço
def monitorar_preco(url, preco_desejado, email_destino, email_origem, senha_origem):
    while True:
        try:
            preco_atual = obter_preco(url)
            print(f"Preço atual: R${preco_atual:.2f}")
            
            # Salvar o preço na planilha
            salvar_preco_planilha(preco_atual, url)
            
            # Verificar se o preço atingiu o valor desejado
            if preco_atual <= preco_desejado:
                print(f"Preço atingiu o valor desejado! Enviando e-mail...")
                enviar_alerta_email(preco_atual, url, email_destino, email_origem, senha_origem)
                break
        except Exception as e:
            print(f"Erro ao obter preço: {e}")
            
        # Intervalo de tempo para verificar o preço novamente
        time.sleep(3600) # 3600 sec = 1h
        
# Exeçução do programa
if __name__ == "__main__":
    
    dados_origem = variaveis_json()
    
    url_produto = dados_origem['url']
    preco_desejado = 300
    email_origem = dados_origem['email_origem']
    senha_origem = dados_origem['senha_origem']
    email_destino = dados_origem['email_destino']
    
    monitorar_preco(url_produto, preco_desejado, email_destino, email_origem, senha_origem)