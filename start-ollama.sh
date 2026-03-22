#!/bin/bash
set -e

echo "Iniciando start-ollama.sh..."

ollama serve &

sleep 5

echo "Verificando se o modelo $OLLAMA_MODEL_NAME já existe..."

if ollama list | grep -q "$OLLAMA_MODEL_NAME"; then
    echo "Modelo já instalado."
else
    echo "Baixando modelo $OLLAMA_MODEL_NAME..."
    ollama pull "$OLLAMA_MODEL_NAME"
fi

echo "Terminando start-ollama.sh..."

wait