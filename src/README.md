# Código da Aplicação

Esta pasta contém o código do agente financeiro em um protótipo Streamlit que consome dados do Ollama.

## Estrutura Atual

```
src/
├── app.py            # Aplicação principal (Streamlit)
├── agent.py          # Lógica de atendimento e chamadas ao LLM
├── config.py         # Parâmetros de ambiente e configuração de geração
├── README.md         # Documentação da pasta src
└── ...
```

## Arquivos Importantes

- `app.py`: Inicializa o Streamlit, interface, histórico de mensagens e chamadas para o agente.
- `agent.py`: Contém a lógica de criação de prompts, contexto e requisição para o Ollama.
- `config.py`: Carrega variáveis de ambiente com `dotenv` e define constantes de geração (`TEMPERATURE`, `TOP_P`, `NUM_PREDICT`, `REPEAT_PENALTY`, etc.).

## Variáveis de ambiente usadas

O projeto usa variáveis no `.env` para configurar o serviço Ollama e o modelo:

- `OLLAMA_SERVICE_HOST` (ex: `http://ollama` ou `http://localhost`)
- `OLLAMA_SERVICE_PORT` (ex: `11434`)
- `OLLAMA_MODEL_NAME` (ex: `qwen2.5:3b`)
- `STREAMLIT_SERVER_PORT` (ex: `8501`)
- `STREAMLIT_SERVER_ADDRESS` (ex: `0.0.0.0`)

Exemplo mínimo de `.env`:

```ini
OLLAMA_SERVICE_HOST=http://ollama
OLLAMA_SERVICE_PORT=11434
OLLAMA_MODEL_NAME=qwen2.5:3b
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## Como executar localmente

```bash
# Instalar dependências (no venv)
pip install -r requirements.txt

# Iniciar o app Streamlit
streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
```

Abra `http://localhost:8501` no navegador.

## Como executar em Docker Compose

1. Tenha Ollama rodando via Docker Compose (`docker-compose.yml`).
2. Start com:

```bash
docker compose up -d --build
```

3. Acesse `http://localhost:8501`.

## Modo Debug (VS Code + Docker)

Use `docker-compose.debug.yml` e `launch.json` para anexar o depurador Python no container (porta `5678`).

```bash
export APP_PORT=8501
docker compose -f docker-compose.yml -f docker-compose.debug.yml up --build
```

No VS Code, inicie a configuração `Attach Docker Luma Agent` para depurar.

## Dicas de ajuste de geração

Os parâmetros do `config.py` controlam a geração do LLM:

- `ENVIAR_PARAMETROS_OPCIONAIS`: habilita envio de parâmetros de geração.
- `TEMPERATURE`: 0.0–1.0, controla diversidade criativa.
- `TOP_P`: 0.1–1.0, controla corte de probabilidade.
- `NUM_PREDICT`: tokens máximos de resposta.
- `REPEAT_PENALTY`: >1.0 reduz repetições.

Ajuste esses valores conforme qualidade desejada do texto.

