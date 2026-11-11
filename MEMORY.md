# MEMORY.md - Memória do Projeto

## 1. Visão Geral do Projeto
- **Nome:** Encurtador de URLs com Estatísticas de Acesso
- **Linguagem / Ecossistema:** Python 3.14+
- **Objetivo:** API REST limpa, modular e testada para encurtamento de URLs, redirecionamento HTTP com métricas de clique e consulta de estatísticas.

---

## 2. Regras e Preferências do Usuário
1. **Controle de Versão Rigoroso:**
   - Realizar um commit a **cada etapa concluída**.
   - Padrão de mensagens: **Conventional Commits** (`feat:`, `chore:`, `test:`, `docs:`, `fix:`).
   - Enviar commits para o repositório remoto (`git push`) quando disponível.
2. **Qualidade & Arquitetura:**
   - Código organizado em camadas (schemas, models, database, routers, services).
   - Sem segredos ou credenciais no repositório.
   - Tratamento explícito de erros com mensagens claras.
   - Cobertura de testes automatizados com `pytest` para todas as regras de negócio e cenários de erro.

---

## 3. Decisões Técnicas Aprovadas
| Decisão | Escolha | Justificativa |
| :--- | :--- | :--- |
| **Framework** | FastAPI | Validação nativa com Pydantic, OpenAPI/Swagger automático, alta performance. |
| **Banco de Dados** | SQLite | Zero configuração inicial, arquivo local leve, fácil para testes. |
| **Acesso a Dados** | SQLAlchemy 2.0 | ORM robusto e padrão de mercado; permite migrar para PostgreSQL se necessário. |
| **Geração de Código** | Alfanumérico aleatório seguro (6-7 chars) | Evita enumeração sequencial de links; verificação de colisão no banco. |
| **Redirecionamento** | `307 Temporary Redirect` (ou 302) | Impede que navegadores guardem cache do destino, garantindo contagem exata de cliques. |
| **Modelagem de Cliques** | Tabela dedicada `clicks` (1:N) | Salva cada evento de acesso com timestamp (`clicked_at`), atendendo ao RF3 e permitindo métricas temporais. |
| **Testes** | `pytest` + `TestClient` (`httpx`) | Padrão robusto para testes de integração de APIs FastAPI. |
| **Containerização** | `Dockerfile` | Pacote reproduzível criado na etapa final. |

---

## 4. Regras de Negócio Chave
- **RF1 (Criar Link):** Gera código curto único para URL informada.
- **RF2 (Redirecionar):** `GET /{code}` redireciona com status 307 para a URL de destino.
- **RF3 (Registrar Cliques):** Cada redirecionamento grava um novo registro na tabela `clicks`.
- **RF4 (Estatísticas):** `GET /links/{code}/stats` retorna dados do link, total de cliques e data de criação.
- **RF5 (Validação):** Apenas esquemas `http://` e `https://` são aceitos. Rejeita URLs vazias, formatos inválidos ou tentativas de auto-encurtamento.
- **RF6 (Tratamento de 404):** Códigos inexistentes retornam status 404 com payload JSON descritivo.

---

## 5. Roteiro de Progresso
- [x] **Etapa 0:** Aprovação do PRD e criação do `MEMORY.md`
- [x] **Etapa 1:** Estrutura inicial, ambiente virtual, `.gitignore` e dependências
- [x] **Etapa 2:** Configuração do banco de dados e modelos SQLAlchemy (`Link`, `Click`)
- [ ] **Etapa 3:** Criação de link curto e validação de URL (RF1 e RF5) + testes
- [ ] **Etapa 4:** Redirecionamento e tratamento 404 (RF2 e RF6) + testes
- [ ] **Etapa 5:** Registro de cliques e endpoint de estatísticas (RF3 e RF4) + testes
- [ ] **Etapa 6:** Dockerfile, `README.md` completo e testes finais integrados
