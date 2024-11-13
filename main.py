# Obtenção do preço do produto
import json
from configs import functions

# Acessando arquivo JSON com os dados do email origem
def variaveis_json(caminho_arquivo='dados.json'):
    with open(caminho_arquivo, 'r') as file:
        valores_json = json.load(file)
    return valores_json
        
# Exeçução do programa
if __name__ == "__main__":
    
    dados_origem = variaveis_json()
    
    url_produto = dados_origem['url']
    preco_desejado = 300
    email_origem = dados_origem['email_origem']
    senha_origem = dados_origem['senha_origem']
    email_destino = dados_origem['email_destino']
    
    functions.monitorar_preco(url_produto, preco_desejado, email_destino, email_origem, senha_origem)