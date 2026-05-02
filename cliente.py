import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Carrega as credenciais do .env para o cliente também
load_dotenv()

URL_BASE = "http://127.0.0.1:8000"
USUARIO = os.getenv("API_USER")
SENHA = os.getenv("API_PASSWORD")

def menu():
    print("\n" + "="*30)
    print("  CLIENTE API BRASILEIRÃO")
    print("="*30)
    print("1. Ver Tabela Completa")
    print("2. Buscar Time por Nome")
    print("3. Sair")
    return input("\nEscolha uma opção: ")

def ver_tabela():
    try:
        # Fazendo o GET com autenticação básica
        response = requests.get(
            f"{URL_BASE}/tabela", 
            auth=HTTPBasicAuth(USUARIO, SENHA)
        )
        
        if response.status_code == 200:
            dados = response.json()
            print("\nPOS | TIME          | PTS | SALDO")
            print("-" * 35)
            for item in dados:
                print(f"{item['posicao']:3} | {item['time']:13} | {item['pontos']:3} | {item['saldo_gols']:3}")
        else:
            print(f"\nErro: {response.status_code} - {response.json().get('detail')}")
            
    except Exception as e:
        print(f"Erro de conexão: {e}")

def buscar_time():
    nome = input("Digite o nome do time: ")
    try:
        response = requests.get(
            f"{URL_BASE}/time/{nome}", 
            auth=HTTPBasicAuth(USUARIO, SENHA)
        )
        
        if response.status_code == 200:
            t = response.json()
            print(f"\n--- {t['time'].upper()} ---")
            print(f"Posição: {t['posicao']}º")
            print(f"Pontos:  {t['pontos']}")
            print(f"Gols:    {t['gols_feitos']} pro / {t['gols_sofridos']} contra")
            print(f"Saldo:   {t['saldo_gols']}")
        else:
            print(f"\nErro: {t.get('detail', 'Não encontrado')}")
            
    except Exception as e:
        print(f"Erro ao buscar: {e}")

# Loop principal do programa
if __name__ == "__main__":
    if not USUARIO or not SENHA:
        print("Erro: Credenciais não encontradas no arquivo .env!")
    else:
        while True:
            opcao = menu()
            if opcao == "1":
                ver_tabela()
            elif opcao == "2":
                buscar_time()
            elif opcao == "3":
                print("Encerrando cliente...")
                break
            else:
                print("Opção inválida!")
