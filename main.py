import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI(
    title="API Brasileirão Segura",
    description="API com proteção por login e senha",
    version="1.2.0"
)

security = HTTPBasic()

# Função que valida se o login e senha estão corretos
def validar_credenciais(credentials: HTTPBasicCredentials = Depends(security)):
    user_env = os.getenv("API_USER")
    pass_env = os.getenv("API_PASSWORD")
    
    if credentials.username != user_env or credentials.password != pass_env:
        raise HTTPException(
            status_code=401,
            detail="Login ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Função para carregar os dados do JSON
def carregar_dados():
    with open("tabela.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def home():
    return {"mensagem": "API Brasileirão Ativa!", "documentacao": "/docs"}

class TimeInput(BaseModel):
    time: str
    pontos: int
    gols_feitos: int
    gols_sofridos: int

# Função para salvar e ordenar os dados
def salvar_dados(dados):
    # Ordena por: Pontos (maior), depois Saldo de Gols (maior), depois Gols Pro (maior)
    dados_ordenados = sorted(
        dados, 
        key=lambda x: (x['pontos'], x['saldo_gols'], x['gols_feitos']), 
        reverse=True
    )
    
    # Recalcula as posições
    for i, item in enumerate(dados_ordenados, 1):
        item['posicao'] = i
        
    with open("tabela.json", "w", encoding="utf-8") as f:
        json.dump(dados_ordenados, f, indent=4, ensure_ascii=False)

# Endpoint para cadastrar ou atualizar um time
@app.post("/atualizar")
def atualizar_time(time_input: TimeInput, usuario: str = Depends(validar_credenciais)):
    dados = carregar_dados()
    encontrado = False
    
    # Calcula o saldo automaticamente
    saldo = time_input.gols_feitos - time_input.gols_sofridos
    
    for item in dados:
        if item["time"].lower() == time_input.time.lower():
            item["pontos"] = time_input.pontos
            item["gols_feitos"] = time_input.gols_feitos
            item["gols_sofridos"] = time_input.gols_sofridos
            item["saldo_gols"] = saldo
            encontrado = True
            break
            
    if not encontrado:
        novo_time = {
            "posicao": 0, # Será recalculado na função salvar_dados
            "time": time_input.time,
            "pontos": time_input.pontos,
            "gols_feitos": time_input.gols_feitos,
            "gols_sofridos": time_input.gols_sofridos,
            "saldo_gols": saldo
        }
        dados.append(novo_time)
        
    salvar_dados(dados)
    return {"status": "sucesso", "mensagem": f"Time {time_input.time} atualizado!"}

# Endpoint para ver a tabela completa
@app.get("/tabela")
def ver_tabela(usuario: str = Depends(validar_credenciais)):
    return carregar_dados()

# Endpoint para buscar um time específico pelo nome
@app.get("/time/{nome_time}")
def buscar_time(nome_time: str, usuario: str = Depends(validar_credenciais)):
    dados = carregar_dados()
    for item in dados:
        if item["time"].lower() == nome_time.lower():
            return item
    raise HTTPException(status_code=404, detail="Time não encontrado")

# Endpoint para buscar um time específico pela posição            
@app.get("/posicao/{posicao_time}")
def buscar_time_posicao(posicao_time: int, usuario: str = Depends(validar_credenciais)):
    dados = carregar_dados()
    for item in dados:
        if item["posicao"] == posicao_time:
            return item
    raise HTTPException(status_code=404, detail="Posição não encontrada")            

if __name__ == "__main__":
    import uvicorn
    import os
    # O Render nos dá a porta na variável de ambiente 'PORT'
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=porta)
            
   
