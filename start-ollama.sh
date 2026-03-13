#!/bin/bash

echo "Iniciando Ollama..."

ollama serve &

sleep 5

echo "Baixando modelo inicial..."
ollama pull qwen2.5:3b

echo "Modelo pronto."

wait