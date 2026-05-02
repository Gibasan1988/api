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

# Endpoint para ver a tabela completa
@app.get("/tabela")
def ver_tabela(usuario: str = Depends(validar_credenciais)):
    return carregar_dados()

# Endpoint para buscar um time específico pelo nome
@app.get("/time/{nome_time}")
def buscar_time(nome_time: str, usuario: str = Depends(validar_credenciais)):
    dados = carregar_dados()
    
    # Procuramos o time na lista (ignorando maiúsculas/minúsculas para facilitar)
    for item in dados:
        if item["time"].lower() == nome_time.lower():
            return item

# Endpoint para buscar um time específico pela posição            
@app.get("/posicao/{posicao_time}")
def buscar_time_posicao(posicao_time: int, usuario: str = Depends(validar_credenciais)):
    dados = carregar_dados()
    
    # Procuramos o time na lista (ignorando maiúsculas/minúsculas para facilitar)
    for item in dados:
        if item["posicao"] == posicao_time:
            return item
            
    # Se não encontrar, retorna erro 404
    raise HTTPException(status_code=404, detail="Time não encontrado na tabela")            

if __name__ == "__main__":
    import uvicorn
    import os
    # O Render nos dá a porta na variável de ambiente 'PORT'
    porta = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=porta)
            
   
