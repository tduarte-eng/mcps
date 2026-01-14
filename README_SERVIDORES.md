# 🖥️ Servidores MCP - ProjectIAM

## Servidores Disponíveis

### 1. **Servidor B - Funções Matemáticas** 📐
- **Arquivo:** `servidorB.py`
- **Porta:** 8082
- **URL:** http://127.0.0.1:8082/sse
- **Descrição:** Cálculos matemáticos para avaliação de modernidade

**Ferramentas:**
```python
- calcular_media()                    # Média de números
- calcular_soma()                     # Soma de números
- calcular_pontuacao_artefato()       # Pontuação com pesos
- calcular_media_categoria()          # Média por categoria
- validar_pontuacao()                 # Validação de ranges
- calcular_percentual()               # Cálculo percentual
```

**Iniciar:**
```bash
cd /home/bnb-admin/DEV/MCPs
python servidorB.py
```

---

### 2. **Servidor D - Gráficos (Matplotlib)** 📊
- **Arquivo:** `servidorD_graficos.py`
- **Porta:** 8083
- **URL:** http://127.0.0.1:8083/sse
- **Descrição:** Geração de visualizações de dados

**Ferramentas:**
```python
- gerar_grafico_barras()              # Barras verticais
- gerar_grafico_barras_horizontal()   # Barras horizontais
- gerar_grafico_pizza()               # Gráfico de pizza
- gerar_grafico_radar()               # Spider chart
- gerar_grafico_maturidade()          # Matriz com cores
- gerar_dashboard_completo()          # Dashboard integrado
```

**Iniciar:**
```bash
cd /home/bnb-admin/DEV/MCPs
/home/bnb-admin/DEV/projectiam/.venv/bin/python3 servidorD_graficos.py
```

---

### 3. **Servidor C - PostgreSQL** 🗄️
- **Arquivo:** `servidorC.py`
- **Porta:** 5432 (PostgreSQL)
- **Descrição:** Consultas ao banco de dados (DESABILITADO NO PROJECTIAM)

**Nota:** Este servidor não está sendo usado no flow atual.

---

## 🚀 Inicialização Rápida

### Comando Único (ambos servidores):
```bash
# Terminal 1 - Servidor de Matemática
cd /home/bnb-admin/DEV/MCPs && python servidorB.py &

# Terminal 2 - Servidor de Gráficos  
cd /home/bnb-admin/DEV/MCPs && /home/bnb-admin/DEV/projectiam/.venv/bin/python3 servidorD_graficos.py &
```

### Verificar Status:
```bash
# Verificar processos
ps aux | grep "servidor"

# Verificar portas
netstat -tuln | grep -E "8082|8083"
```

### Parar Servidores:
```bash
pkill -f "servidorB.py"
pkill -f "servidorD_graficos.py"
```

---

## 🔧 Integração no ProjectIAM

### `main_flow.py` - Configuração:
```python
server_params_list = [
    {"url": "http://127.0.0.1:8082/sse", "transport": "sse"},  # Math
    {"url": "http://127.0.0.1:8083/sse", "transport": "sse"}   # Gráficos
]

mcp_adapter = MCPServerAdapter(server_params_list)
aggregated_tools = list(mcp_adapter)
# ✅ Ferramentas MCP disponíveis para todos os crews
```

### Uso nos Crews:
```python
# Exemplo: VisualizacaoCrew
self.mcp_adapter = MCPServerAdapter("http://127.0.0.1:8083/sse")
self.mcp_tools = self.mcp_adapter.get_tools()

agente = Agent(
    config=self.agents_config,
    tools=self.mcp_tools,  # ← Ferramentas MCP disponíveis
    verbose=True
)
```

---

## 📊 Output dos Gráficos

**Diretório de Saída:**
```
/home/bnb-admin/DEV/projectiam/outputs/graficos/
```

**Formato dos Arquivos:**
```
dashboard_completo_20241112_165530.png
grafico_maturidade_20241112_165531.png
grafico_radar_20241112_165532.png
grafico_barras_20241112_165533.png
grafico_pizza_20241112_165534.png
```

---

## 🎯 Status Atual

| Servidor | Porta | Status | PID | Uso no ProjectIAM |
|----------|-------|--------|-----|-------------------|
| servidorB.py | 8082 | ✅ Ativo | - | ✅ Sim (Math) |
| servidorD_graficos.py | 8083 | ✅ Ativo | 877833 | ✅ Sim (Visualização) |
| servidorC.py | 5432 | ⚠️ Não usado | - | ❌ Não |

---

## 🐛 Logs

### Servidor B (Matemática):
```bash
# Sem log dedicado (output no terminal)
```

### Servidor D (Gráficos):
```bash
tail -f /home/bnb-admin/DEV/MCPs/servidor_graficos.log
```

---

## 📚 Dependências

### Servidor B:
```
- fastmcp
```

### Servidor D:
```
- fastmcp
- matplotlib==3.10.7
- numpy
- pillow (para salvar PNG)
```

### Servidor C:
```
- fastmcp
- psycopg2
```

---

## ✅ Checklist de Saúde

```bash
# 1. Verificar processos
ps aux | grep "servidor[BD]"

# 2. Verificar portas
netstat -tuln | grep -E "808[23]"

# 3. Testar conectividade
curl http://127.0.0.1:8082/health 2>/dev/null || echo "Servidor 8082 offline"
curl http://127.0.0.1:8083/health 2>/dev/null || echo "Servidor 8083 offline"

# 4. Verificar logs
tail -20 /home/bnb-admin/DEV/MCPs/servidor_graficos.log
```

---

## 🎉 Pronto!

Ambos servidores MCP estão configurados e funcionando! 🚀
