# 🔗 Encurtador de URLs com Estatísticas de Acesso

Uma API REST desenvolvida em **Python** com **FastAPI** e **SQLAlchemy**, projetada para encurtamento rápido de URLs, redirecionamento temporário inteligente e rastreamento em tempo real de estatísticas de acessos (cliques).

---

## 🎯 Funcionalidades

- **RF1 - Encurtamento de URL:** Recebe uma URL longa e gera um código curto exclusivo de 6 caracteres alfanuméricos.
- **RF2 - Redirecionamento HTTP:** Redireciona o usuário para o destino original utilizando o código `HTTP 307 (Temporary Redirect)`.
- **RF3 - Registro de Cliques:** Cada redirecionamento armazena o evento de clique com registro temporal (timestamp em UTC).
- **RF4 - Estatísticas de Acesso:** Endpoint para consulta de total de cliques acumulados e data do último acesso registrado.
- **RF5 - Validação de Entrada:** Aceita estritamente protocolos seguros (`http://` ou `https://`), bloqueia URLs maliciosas (`javascript:`, `file:`) e rejeita tentativas de auto-encurtamento.
- **RF6 - Tratamento de Erros:** Respostas padronizadas em formato JSON para links não encontrados (`404 Not Found`) e dados inválidos (`422 Unprocessable Entity`).

---

## 💡 Decisões Técnicas de Engenharia

| Decisão | Escolha | Motivação |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | Validação robusta de esquemas com **Pydantic v2**, alta performance assíncrona e documentação OpenAPI/Swagger interativa gerada automaticamente. |
| **Banco de Dados** | **SQLite** | Zero atrito para inicialização local e execução rápida em testes em memória. |
| **Acesso a Dados** | **SQLAlchemy 2.0** | ORM padrão da indústria; separa lógica de negócio do banco e permite migrar para PostgreSQL trocando apenas a string de conexão. |
| **Status Code** | **HTTP 307 (Temporary)** | Redirecionamentos permanentes (`301`) são armazenados em cache local pelo navegador, o que impediria o registro de novos cliques. O código 307 garante que toda requisição passe pelo servidor. |
| **Modelagem de Cliques** | **Tabela `clicks` 1:N** | Em vez de um simples contador, cada clique é persistido individualmente com timestamp, viabilizando métricas temporais detalhadas. |
| **Geração de Códigos** | **Alfanumérico Aleatório (Base62)** | Uso de `secrets.choice` com 6 caracteres, evitando ataques de enumeração sequencial de links comuns em abordagens puramente baseadas em ID. |

---

## 📁 Estrutura do Projeto

```text
url-shortener/
├── app/
│   ├── core/
│   │   ├── config.py       # Configurações e variáveis de ambiente
│   │   └── database.py     # Conexão e sessão do SQLAlchemy
│   ├── models/
│   │   ├── link.py         # Modelo da tabela de links
│   │   └── click.py        # Modelo da tabela de cliques
│   ├── schemas/
│   │   └── link.py         # Schemas de validação e resposta Pydantic
│   ├── services/
│   │   └── shortener.py    # Lógica de negócio (geração de código e métricas)
│   ├── routers/
│   │   ├── links.py        # Rotas /links (criação e estatísticas)
│   │   └── redirect.py     # Rota /{code} (redirecionamento)
│   └── main.py             # Inicialização da aplicação FastAPI
├── tests/
│   ├── conftest.py         # Fixtures de banco em memória para testes
│   ├── test_health.py      # Teste do healthcheck
│   ├── test_database.py    # Teste de persistência e relacionamentos
│   ├── test_create_link.py # Testes de criação e validação
│   ├── test_redirect.py    # Testes de redirecionamento e 404
│   └── test_stats.py       # Testes de métricas e contagem de cliques
├── Dockerfile              # Imagem para containerização
├── requirements.txt        # Dependências do projeto
├── MEMORY.md               # Registro de contexto e histórico de decisões
└── README.md
```

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Python 3.12+ instalado (ou Docker)

### 1. Clonar o repositório
```bash
git clone https://github.com/rodrigokk1975/url-shortener.git
cd url-shortener
```

### 2. Criar e ativar o ambiente virtual
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o servidor
```bash
uvicorn app.main:app --reload
```
A API estará disponível em: `http://localhost:8000`  
Documentação Swagger interativa: `http://localhost:8000/docs`

---

## 🧪 Como Executar os Testes

A suíte de testes utiliza o `pytest` com banco de dados SQLite isolado em memória:

```bash
pytest
```

---

## 🐳 Executando com Docker

Se preferir rodar via container:

```bash
# Construir a imagem
docker build -t url-shortener .

# Iniciar o container
docker run -d -p 8000:8000 --name url-shortener-app url-shortener
```

---

## 📖 Documentação da API

### 1. Criar Link Curto
- **Método:** `POST`
- **Rota:** `/links`
- **Payload:**
```json
{
  "url": "https://fastapi.tiangolo.com"
}
```
- **Exemplo de chamada com `curl`:**
```bash
curl -X POST "http://localhost:8000/links" \
     -H "Content-Type: application/json" \
     -d "{\"url\": \"https://fastapi.tiangolo.com\"}"
```
- **Resposta (`201 Created`):**
```json
{
  "id": 1,
  "short_code": "aK9zQ1",
  "original_url": "https://fastapi.tiangolo.com",
  "short_url": "http://localhost:8000/aK9zQ1",
  "created_at": "2026-11-11T17:00:00Z"
}
```

---

### 2. Redirecionar para URL Original
- **Método:** `GET`
- **Rota:** `/{codigo}`
- **Comportamento:** Retorna `307 Temporary Redirect` com o cabeçalho `Location` apontando para a URL original e contabiliza +1 clique.
```bash
curl -i "http://localhost:8000/aK9zQ1"
```

---

### 3. Consultar Estatísticas
- **Método:** `GET`
- **Rota:** `/links/{codigo}/stats`
- **Exemplo de chamada com `curl`:**
```bash
curl -X GET "http://localhost:8000/links/aK9zQ1/stats"
```
- **Resposta (`200 OK`):**
```json
{
  "id": 1,
  "short_code": "aK9zQ1",
  "original_url": "https://fastapi.tiangolo.com",
  "short_url": "http://localhost:8000/aK9zQ1",
  "created_at": "2026-11-11T17:00:00Z",
  "total_clicks": 3,
  "last_clicked_at": "2026-11-11T17:05:42Z"
}
```

---

### 4. Health Check
- **Método:** `GET`
- **Rota:** `/health`
- **Resposta (`200 OK`):**
```json
{
  "status": "ok",
  "project": "URL Shortener API",
  "version": "1.0.0"
}
```
