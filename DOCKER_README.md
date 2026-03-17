# Docker Setup - Luma Agent

Este documento contém todas as instruções necessárias para rodar a aplicação usando Docker com um container exclusivo para o Ollama e um container para a aplicação.

## Pré-requisitos

- Docker instalado e rodando
- Docker Compose (opcional, mas recomendado)
- Aproximadamente 8GB de memória disponível no Docker (para Ollama)

## Arquitetura

A aplicação utiliza dois containers:

1. **Container Ollama**: Serviço de LLM rodando isoladamente com o carregamento automático do modelo qwen2.5:3b
2. **Container Application**: Aplicação Streamlit que se conecta ao Ollama

## Opção 1: Usando Docker Compose (Recomendado)

### 1. Criar arquivo `docker-compose.yml`

Se ainda não existir um arquivo `docker-compose.yml`, crie-o na raiz do projeto:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-service
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    volumes:
      - ollama-data:/root/.ollama
      - ./start-ollama.sh:/start-ollama.sh
    entrypoint: ["/bin/bash", "/start-ollama.sh"]
    restart: unless-stopped

  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: luma-agent-app
    ports:
      - "8501:8501"
    depends_on:
      - ollama
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    volumes:
      - .:/app
    working_dir: /app
    command: bash -c "streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    restart: unless-stopped

volumes:
  ollama-data:
```

### 2. Iniciar os containers

Antes de iniciar, torne o script executável:

```bash
chmod +x start-ollama.sh
```

```bash
# Construir e iniciar os containers
docker-compose up -d --build

# Verificar os logs
docker-compose logs -f

# Acessar a aplicação
# Abra seu navegador em: http://localhost:8501
```

### 3. Parar os containers

```bash
docker-compose down
```

### 4. Remover dados do Ollama (reiniciar do zero)

```bash
docker-compose down -v
```

---

## Opção 2: Usando Docker Commands (Manual)

### 1. Iniciar o container do Ollama

```bash
docker run -d \
  --name ollama-service \
  -p 11434:11434 \
  -e OLLAMA_HOST=0.0.0.0:11434 \
  -v ollama-data:/root/.ollama \
  --restart unless-stopped \
  ollama/ollama:latest
```

### 2. Construir a imagem da aplicação

```bash
docker build -t luma-agent .
```

### 3. Rodar a aplicação

```bash
docker run -it \
  --rm \
  -p 8501:8501 \
  --workdir /app \
  --add-host=host.docker.internal:host-gateway \
  -v "$(pwd)":/app \
  --link ollama-service:ollama \
  -e OLLAMA_BASE_URL=http://ollama:11434 \
  luma-agent \
  bash -c "streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0"
```

### 4. Acessar a aplicação

Abra seu navegador em: `http://localhost:8501`

### 5. Parar e remover os containers

```bash
# Parar o container da aplicação
# (automático com --rm)

# Parar o container do Ollama
docker stop ollama-service

# Remover o container do Ollama
docker rm ollama-service

# Remover o volume de dados do Ollama (se desejar)
docker volume rm ollama-data
```

---

## Configuração do Ollama

### Instalar um modelo (após Ollama estar rodando)

```bash
# Se estiver usando Docker Compose
docker exec ollama-service ollama pull llama2

# ou

# Se estiver rodando o container manualmente
docker exec ollama-service ollama pull llama2
```

### Modelos disponíveis (exemplos)

- `llama2`: 7B, rápido e compacto
- `neural-chat`: Otimizado para chat
- `mistral`: Modelo de alta performance
- `vicuna`: Alternativa code-friendly

Para listar modelos disponíveis, visite: https://ollama.ai/library

---

## Testando o Serviço do Ollama

Após instalar um modelo, você pode testar o serviço do Ollama usando requisições HTTP.

### 1. Teste básico - Verificar modelos instalados

```bash
curl http://localhost:11434/api/tags
```

**Resposta esperada**: Lista de modelos instalados em JSON

### 2. Teste de geração - Enviar uma requisição ao modelo

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:3b",
  "prompt": "Explique inflação em uma frase",
  "stream": false
}'
```

**Resposta esperada**: JSON com o resultado gerado pelo modelo

```json
{
  "model": "qwen2.5:3b",
  "created_at": "2026-03-12T10:30:45.123456789Z",
  "response": "Inflação é o aumento contínuo e generalizado dos preços de bens e serviços em uma economia...",
  "done": true,
  "context": [...],
  "total_duration": 5000000000,
  "load_duration": 1000000000,
  "prompt_eval_count": 15,
  "eval_count": 45,
  "eval_duration": 4000000000
}
```

### 3. Teste com streaming (resposta em tempo real)

Para receber a resposta em partes enquanto o modelo está gerando:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:3b",
  "prompt": "Qual é a capital do Brasil?",
  "stream": true
}'
```

Cada linha da resposta será um JSON separado contendo parte da resposta.

### 4. Sistema de prompts customizados

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:3b",
  "prompt": "Você é um analista financeiro. Explique o que é um fundo de investimento.",
  "stream": false,
  "system": "Você é um especialista em finanças com 10 anos de experiência."
}'
```

### 5. Testar desde dentro do container da aplicação

Se estiver usando Docker Compose:

```bash
# Acessar o container da aplicação
docker-compose exec app bash

# Testar a conexão com Ollama (dentro do container)
curl http://ollama:11434/api/tags
```

### Dicas para testes

- **Trocar modelo**: Substitua `"model": "qwen2.5:3b"` pelo modelo instalado
- **Ajustar temperatura**: Adicione `"temperature": 0.7` para controlar criatividade (0.0-1.0)
- **Limitar tokens**: Adicione `"num_predict": 100` para limitar comprimento da resposta
- **Timeout**: Algumas requisições podem levar tempo com modelos maiores
- **Verificar status**: Use `docker logs ollama-service` para ver o que está acontecendo

---

## Troubleshooting

### A aplicação não consegue conectar ao Ollama

**Problema**: Erro de conexão recusada ao Ollama

**Solução**:
```bash
# Verificar se o container do Ollama está rodando
docker ps

# Verificar logs do Ollama
docker logs ollama-service

# Testar conexão ao Ollama
curl http://localhost:11434/api/tags
```

### Porta 8501 já está em uso

**Solução**: Usar uma porta diferente
```bash
# Mudar para porta 8502
docker run -it \
  --rm \
  -p 8502:8501 \
  ... (resto do comando)
```

### Porta 11434 já está em uso

**Solução**: Usar uma porta diferente para Ollama
```bash
docker run -d \
  --name ollama-service \
  -p 11435:11434 \
  ... (resto do comando)
```

### Limpar containers e imagens danificadas

```bash
# Remover todos os containers parados
docker container prune

# Remover imagens não usadas
docker image prune

# Limpeza completa (cuidado!)
docker system prune -a --volumes
```

---

## Environment Variables

Configure estas variáveis para customizar o comportamento:

### Para a aplicação
- `OLLAMA_BASE_URL`: URL do serviço Ollama (padrão: http://ollama:11434)
- `STREAMLIT_SERVER_PORT`: Porta da aplicação (padrão: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Endereço do servidor (padrão: 0.0.0.0)

### Para o Ollama
- `OLLAMA_HOST`: Host e porta para o Ollama (padrão: 0.0.0.0:11434)

---

## 🔧 Modo Debug com Docker + VS Code

Para desenvolvimento com depuração (debug), use um `docker-compose.debug.yml` separado e configure o VS Code para anexar ao container.

### 1) Arquivo `docker-compose.debug.yml`

Crie (ou confirme) este arquivo na raiz:

```yaml
version: "3.8"

services:
  app:
    ports:
      - "${APP_PORT}:${APP_PORT}"
      - "5678:5678"
    command: >
      python -m debugpy
      --listen 0.0.0.0:5678
      --wait-for-client
      -m streamlit run src/app.py
      --server.port ${APP_PORT}
      --server.address 0.0.0.0
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app
    working_dir: /app
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
```

> O `--wait-for-client` pausa a aplicação até o VS Code anexar o depurador.

### 2) `launch.json` para anexar no VS Code

No `.vscode/launch.json`, adicione ou confirme esta configuração:

```json
{
 "version": "0.2.0",
 "configurations": [
  {
   "name": "Attach Docker Luma Agent",
   "type": "python",
   "request": "attach",
   "connect": {
     "host": "localhost",
     "port": 5678
   },
   "pathMappings": [
     {
       "localRoot": "${workspaceFolder}/src",
       "remoteRoot": "/app/src"
     }
   ]
  }
 ]
}
```

### 3) Iniciar em modo debug

No terminal do projeto, execute:

```bash
docker compose -f docker-compose.yml -f docker-compose.debug.yml up
```

### 4) Parar em modo debug

Sempre use o comando com os dois arquivos para evitar containers órfãos:

```bash
docker compose -f docker-compose.yml -f docker-compose.debug.yml down
```

### 5) Anexar o depurador no VS Code

1. Abra a paleta (`Ctrl+Shift+P`) e escolha `Debug: Start Debugging` ou use o painel de execução.
2. Selecione `Attach Docker Luma Agent`.
3. A execução deve continuar e você poderá colocar breakpoints no código.

> Se o VS Code falhar ao anexar, verifique se o container está rodando e se a porta `5678` está exposta corretamente.

### 6) Dicas importantes

- Use `docker compose -f docker-compose.yml -f docker-compose.debug.yml logs -f app` para ver mensagens de debug.
- Certifique-se de mapear o volume (`.:/app`) para editar código em tempo real.
- Para sair, pare com `docker compose -f docker-compose.yml -f docker-compose.debug.yml down` e execute novamente após mudanças.


---

## Performance e Recursos

### Recomendações de hardware

- **CPU**: Mínimo 2 cores (4+ recomendado)
- **RAM**: Mínimo 4GB (8GB+ recomendado para Ollama)
- **Disk**: 15-30GB de espaço livre (depende dos modelos do Ollama)

### Aumentar recursos para Docker

Se receber erros de memória:

**No Linux (systemd)**:
```bash
# Editar configuração do Docker
sudo systemctl edit docker

# Adicionar:
[Service]
MemoryLimit=8G
```

**No Docker Desktop (Windows/Mac)**:
- Abra Docker Desktop → Settings → Resources
- Aumente CPU cores, Memory, Swap, e Disk image size

---

## Dicas Úteis

### Ver logs em tempo real

```bash
# Docker Compose
docker-compose logs -f app

# Docker manual
docker logs -f luma-agent-app
```

### Acessar shell do container

```bash
# Docker Compose
docker-compose exec app bash

# Docker manual
docker exec -it luma-agent-app bash
```

### Rebuild após mudanças no código

```bash
# Docker Compose
docker-compose up -d --build

# Docker manual
docker build -t luma-agent . && docker run -it ...
```

---

## Para Desenvolvimento Local (sem Docker)

Se preferir rodar localmente sem Docker:

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar Ollama localmente
# (Download em https://ollama.ai)
ollama serve

# Em outro terminal, rodar a aplicação
streamlit run src/app.py --server.port 8501 --server.address 0.0.0.0
```

---

## Referências

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Ollama Documentation](https://ollama.ai)
- [Streamlit Documentation](https://docs.streamlit.io/)
