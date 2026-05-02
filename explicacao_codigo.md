# 🔍 Desvendando o Código da API

Vamos analisar cada parte do seu arquivo `main.py` para você entender como o FastAPI funciona.

---

## 1. As Importações (Os Motores)
```python
import json
from fastapi import FastAPI, HTTPException
```
*   **`import json`**: Usado para ler arquivos `.json`. APIs e JSON são melhores amigos.
*   **`FastAPI`**: É o coração de tudo. Ele que cria o servidor web.
*   **`HTTPException`**: Uma ferramenta para enviar erros (como o 404 Not Found) de volta para o usuário.

---

## 2. Configurando a API
```python
app = FastAPI(
    title="API Brasileirão",
    description="Busca de posições e estatísticas dos times",
    version="1.1.0"
)
```
*   Aqui nós batizamos a nossa API. Essas informações aparecem lá na página `/docs` (Swagger). É a identidade do seu projeto.

---

## 3. Lendo o "Banco de Dados"
```python
def carregar_dados():
    with open("tabela.json", "r", encoding="utf-8") as f:
        return json.load(f)
```
*   Como ainda não estamos usando um banco de dados real (SQL), criamos esta função para abrir o arquivo `tabela.json`, ler o conteúdo e transformá-lo em uma lista do Python.
*   **`encoding="utf-8"`**: Importante para que nomes com acentos (como Atlético) não fiquem bugados.

---

## 4. As Rotas (Endpoints)

### A Rota Principal (Home)
```python
@app.get("/")
def home():
    return {"mensagem": "API Brasileirão Ativa!"}
```
*   **`@app.get("/")`**: Diz que quando alguém acessar o endereço puro da API, essa função será executada.
*   O `return` envia um **Dicionário Python**, que o FastAPI converte automaticamente para **JSON**.

### A Tabela Completa
```python
@app.get("/tabela")
def ver_tabela():
    return carregar_dados()
```
*   Simplesmente chama a função que lê o arquivo e cospe os dados na tela.

### O Buscador Inteligente
```python
@app.get("/time/{nome_time}")
def buscar_time(nome_time: str):
    dados = carregar_dados()
    
    for item in dados:
        if item["time"].lower() == nome_time.lower():
            return item
            
    raise HTTPException(status_code=404, detail="Time não encontrado")
```
1.  **`{nome_time}`**: Isso é um **Path Parameter**. O que o usuário digitar na URL vira o valor da variável `nome_time`.
2.  **`for item in dados`**: Ele percorre time por time da sua tabela.
3.  **`.lower()`**: Transforma tudo em minúsculo. Assim, se o usuário buscar "PALMEIRAS" ou "palmeiras", ele vai encontrar o time "Palmeiras".
4.  **`raise HTTPException`**: Se o loop terminar e não encontrar nada, ele "levanta" um erro 404, parando a execução e avisando ao usuário.

---

## 🚀 Resumo do Fluxo
Usuário digita URL ➡️ FastAPI identifica a Rota ➡️ Executa a Função ➡️ Lê o JSON ➡️ Processa a busca ➡️ Devolve o JSON pro Navegador.
