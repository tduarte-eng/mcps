# Integração Agentes de Análise (teste.py) ↔ Servidor de Modernidade (servidorB.py)

## Visão Geral

O `servidorB.py` oferece **ferramentas objetivas de mensuração de modernidade** que podem ser integradas aos agentes especialistas do `teste.py` através do MCP (Model Context Protocol).

## Fluxo de Integração Recomendado

### 1. Preparação (teste.py)
```python
# No teste.py, os agentes já categorizam os artefatos em uma tabela:
# | Categoria | Artefatos |
# | Linguagem de Programação | Java 8, Spring Boot 2.3 |
# | Banco de Dados | MySQL 5.7, PostgreSQL 14 |
# | Infraestrutura | Docker, Kubernetes |
# | DevSecOps / Governança | (Nenhum) |
```

### 2. Análise Especializada + Integração (teste.py)
Cada agente especialista (linguagem, sistema, infra, banco, devsecops) deve:

```python
# Após gerar sua análise detalhada, chamar a tool do servidorB:
tools=aggregated_tools  # Já configurado no teste.py

# Exemplo no agente de linguagem:
resultado_analise = crew.kickoff(...)
analise_texto = resultado_analise.raw

# Chamar tool do servidorB para incorporar a análise
await receber_analise_agente(
    categoria="Linguagem de Programação",
    artefatos=["Java 8", "Spring Boot 2.3"],
    analise_detalhada=analise_texto,
    classificacao_modernidade="Legado Crítico"  # Baseado na análise
)
```

### 3. Geração do Relatório Final (teste.py)
```python
# Após todos os agentes terminarem suas análises:
relatorio_final = await gerar_relatorio_modernidade_completo(
    tabela_markdown=tabela_categorizacao_resultado
)

print(f"Índice Global de Modernidade: {relatorio_final['indice_global']}")
print(f"Classificação: {relatorio_final['classificacao_global']}")
print(f"Top 5 Prioridades: {relatorio_final['top_5_prioridades']}")
```

## Tools Disponíveis no servidorB.py

### 1. `listar_regras_modernidade()`
Retorna critérios, pesos e faixas de classificação.

### 2. `receber_analise_agente(categoria, artefatos, analise_detalhada, classificacao_modernidade)`
- **Entrada**: Análise textual completa do agente especialista
- **Processamento**: Extrai insights (✅❌⚠️💡), sugestões, scores heurísticos
- **Saída**: Confirmação e score calculado

### 3. `gerar_relatorio_modernidade_completo(tabela_markdown)`
- **Entrada**: Tabela de categorização (markdown)
- **Processamento**: Combina análises dos agentes (70%) + base estática (30%)
- **Saída**: Relatório JSON completo com métricas objetivas

### 4. `avaliar_modernidade_tabela(tabela_markdown)` *(fallback)*
Versão simplificada que funciona apenas com base estática (sem agentes).

## Exemplo de Implementação no teste.py

```python
# No método agente_artefatos_tecnologia(), após executar as tasks:
async def agente_artefatos_tecnologia(self) -> Dict[str, Any]:
    # ... código existente de categorização ...
    
    # Executar análises especializadas
    crew = Crew(agents=[...], tasks=[categorizar_task, linguagem_task, sistemas_task, ...])
    result = crew.kickoff(inputs={"input": self.state.input})
    
    # Integrar cada análise no servidor de modernidade
    if hasattr(result, 'linguagem_analise') and result.linguagem_analise:
        await aggregated_tools.receber_analise_agente(
            categoria="Linguagem de Programação",
            artefatos=extrair_artefatos_da_categoria(tabela, "Linguagem de Programação"),
            analise_detalhada=result.linguagem_analise,
            classificacao_modernidade=extrair_classificacao(result.linguagem_analise)
        )
    
    # ... repetir para outras categorias ...
    
    # Gerar relatório final integrado
    relatorio_modernidade = await aggregated_tools.gerar_relatorio_modernidade_completo(
        tabela_markdown=result.tabela_categorizacao
    )
    
    return {
        **result,
        "modernidade_objetiva": relatorio_modernidade
    }
```

## Interpretação dos Resultados

### Índice Global (0-100):
- **85-100**: Moderno → Tecnologias atuais, práticas avançadas
- **70-84**: Em Evolução → Bom estado, melhorias pontuais  
- **50-69**: Moderado → Alvo de modernização
- **30-49**: Legado Crítico → Modernização urgente
- **0-29**: Alto Risco → Substituição necessária

### Dimensões Detalhadas:
1. **Suporte/Ciclo de Vida (35%)**: LTS, EoL, suporte oficial
2. **Atualidade Relativa (20%)**: Gap de versões
3. **Práticas Modernas (20%)**: CI/CD, containers, segurança
4. **Risco Legado (15%)**: Tecnologias obsoletas
5. **Cloud/Escalabilidade (10%)**: Cloud-native, scaling

## Executar o Servidor

```bash
cd /home/bnb-admin/DEV/MCPs
python servidorB.py
# Servidor rodará na porta 8081 (SSE transport)
```

## Testando a Integração

```python
# Teste manual das ferramentas
import asyncio

# Simular análise do agente
await receber_analise_agente(
    categoria="Linguagem de Programação", 
    artefatos=["Java 8"],
    analise_detalhada="""
    ❌ **Java 8 - Status Crítico**:
    - Java 8 saiu de suporte público em janeiro 2019
    - Necessita migração urgente para Java 17 LTS
    💡 Sugestões: Migrar para Java 17, atualizar dependências
    """,
    classificacao_modernidade="Legado Crítico"
)

# Gerar relatório
tabela_teste = """
| Categoria | Artefatos |
|-----------|-----------|  
| Linguagem de Programação | Java 8 |
"""

relatorio = await gerar_relatorio_modernidade_completo(tabela_teste)
print(f"Índice: {relatorio['indice_global']}")
```

---

Esta integração permitirá que os agentes do `teste.py` forneçam **análises qualitativas ricas** enquanto o `servidorB.py` oferece **métricas objetivas e padronizadas** para tomada de decisão em modernização tecnológica.