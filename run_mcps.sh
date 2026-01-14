#!/bin/bash

# Ativa o ambiente virtual
source .venv/bin/activate

# Inicia servidorB.py (porta 8082)
nohup python3 ./servidorB.py > servidorB.log 2>&1 &

# Inicia servidorD_graficos.py (porta 8083)
nohup python3 ./servidorD_graficos.py > servidorD_graficos.log 2>&1 &

# Exibe os processos MCP em execução
echo "Servidores MCP iniciados:"
ps aux | grep servidor | grep -v grep
