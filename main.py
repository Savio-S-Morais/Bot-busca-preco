# Obtenção do preço do produto
import json
import time
import os
from configs import functions


# Acessando arquivo JSON com os dados do email origem
def variaveis_json(caminho_arquivo='dados.json'):
    with open(caminho_arquivo, 'r') as file:
        valores_json = json.load(file)
    return valores_json

dados_origem = variaveis_json()
    
email_origem = dados_origem['email_origem']
senha_origem = dados_origem['senha_origem']
email_destino = dados_origem['email_destino']

# Função para adicionar link e preço desejado ao JSON
def adicionar_itens_json(caminho_arquivo='lista_de_compras.json'):
    # Recebe links e preços desejados via input
    links = input("Digite os links dos produtos separados por vírgula: ").strip().split(',')
    precos_desejados = input("Digite os preços desejados, na mesma ordem, separados por vírgula: ").strip().split(',')

    if len(links) != len(precos_desejados):
        print("O número de links e preços desejados não corresponde.")
        return

    # Converte os preços desejados para float
    precos_desejados = [float(preco.strip()) for preco in precos_desejados]

    # Carrega o JSON existente ou cria um novo dicionário
    if os.path.exists(caminho_arquivo) and os.path.getsize(caminho_arquivo) > 0:
        with open(caminho_arquivo, 'r') as file:
            dados = json.load(file)
    else:
        dados = {}

    # Garante que a chave "itens" exista no dicionário
    if "itens" not in dados:
        dados["itens"] = []

    # Adiciona cada link e preço desejado como um novo item
    for link, preco_desejado in zip(links, precos_desejados):
        novo_item = {
            "url": link.strip(),
            "preco_desejado": preco_desejado,
            "email_origem": email_origem,
            "senha_origem": senha_origem,
            "email_destino": email_destino
        }
        dados["itens"].append(novo_item)

    # Salva de volta no arquivo JSON
    with open(caminho_arquivo, 'w') as file:
        json.dump(dados, file, indent=4)
    print(f"{len(links)} itens adicionados ao arquivo JSON.")

    

    
# Função para monitorar preços dos links no JSON
def monitorar_precos(caminho_arquivo='dados.json'):
    # Carrega os itens do JSON
    with open(caminho_arquivo, 'r') as file:
        dados = json.load(file)

    itens = dados.get("itens", [])

    # Loop while para monitorar os preços dos links
    while True:
        for item in itens:
            link = item["url"]
            preco_desejado = item["preco_desejado"]

            # Obtém o preço atual do link usando função importada
            preco_atual = functions.obter_preco(link)
            nome_produto = functions.obter_nome(link)
            
            #functions.salvar_preco_planilha(item[preco_atual],link, nome_arquivo='historico_preco.xlsx')

            # Verifica se o preço desejado foi atingido e envia alerta
            if preco_atual <= preco_desejado:
                functions.enviar_alerta_email(preco_atual, link, item["email_destino"], item["email_origem"], item["senha_origem"])
                print(f"Alerta enviado para {link} - Preço atual: {preco_atual}")
                
            print(f"Preço atual do produto '{nome_produto}' é de: R${preco_atual:.2f}")            
            
            # Espera um tempo antes de verificar o próximo link
            time.sleep(5)
        
# Exeçução do programa
if __name__ == "__main__":
    
    # Pergunta se o usuário deseja iniciar o monitoramento
    iniciar_monitoramento = input("Deseja iniciar o monitoramento de preços agora? (s/n): ").lower()
    
    while iniciar_monitoramento == 'n':
        adicionar_itens_json()
        iniciar_monitoramento = input("Deseja iniciar o monitoramento de preços agora? (s/n): ").lower()
    else: 
        monitorar_precos()
    
    #functions.monitorar_preco(url_produto, preco_desejado, email_destino, email_origem, senha_origem)