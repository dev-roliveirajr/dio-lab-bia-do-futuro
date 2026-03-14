# imagem base
FROM python:3.11-slim

# evita arquivos .pyc e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# diretório da aplicação
WORKDIR /app

# copiar apenas dependências primeiro (para usar cache)
COPY requirements.txt .

# instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# copiar o restante do projeto
COPY . .

# porta do streamlit
EXPOSE ${APP_PORT}

# iniciar aplicação
CMD ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=${APP_PORT}"]