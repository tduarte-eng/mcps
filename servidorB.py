"""
Servidor MCP para Avaliação de Modernidade Tecnológica

Este servidor oferece ferramentas objetivas para mensurar o grau de modernidade de artefatos tecnológicos,
integrando análises de agentes especialistas LLM com uma base de conhecimento estática.

## Metodologia de Avaliação

### Dimensões de Modernidade (com pesos):
1. **Suporte e Ciclo de Vida** (35%): Status oficial de suporte, versões LTS, EoL
2. **Atualidade Relativa** (20%): Gap entre versão utilizada e última disponível
3. **Práticas Modernas** (20%): CI/CD, containers, segurança, ecossistema ativo
4. **Risco de Legado** (15%): Tecnologias obsoletas, arquiteturas monolíticas rígidas
5. **Cloud & Escalabilidade** (10%): Capacidade cloud-native, scaling horizontal

### Faixas de Classificação:
- **85-100**: Moderno (tecnologias atuais, práticas avançadas)
- **70-84**: Em Evolução (bom estado, melhorias pontuais)
- **50-69**: Moderado / Alvo de Modernização (necessita atenção)
- **30-49**: Legado Crítico (modernização urgente)
- **0-29**: Alto Risco Tecnológico (substituição necessária)

## Integração com Agentes LLM

O servidor recebe análises detalhadas dos agentes especialistas através da tool `receber_analise_agente()`,
que extrai insights qualitativos e os converte em scores quantitativos, combinando com a base estática
(70% peso agente, 30% base estática).

## Formato de Saída

### Estrutura do Relatório Completo:
```json
{
    "sucesso": true,
    "indice_global": 73.4,
    "classificacao_global": "Em Evolução", 
    "total_artefatos": 12,
    "estatisticas_por_classificacao": {"Moderno": 4, "Legado Crítico": 3, ...},
    "artefatos_detalhados": [
        {
            "nome_original": "Java 8",
            "base": "Java", 
            "versao": "8",
            "categoria": "Linguagem de Programação",
            "dimensoes": {
                "suporte_ciclo_vida": 40,
                "atualidade_relativa": 30, 
                "praticas_modernas": 70,
                "risco_legado": 40,
                "cloud_scalability": 60
            },
            "indice": 45.3,
            "classificacao": "Legado Crítico",
            "sugestoes": ["Migrar para Java 17 LTS", ...],
            "fonte_analise": "Agente Especialista + Base Estática"
        }
    ],
    "top_5_prioridades": [...],
    "analises_agentes_incorporadas": [...],
}
```
"""

from fastmcp import FastMCP
from typing import List, Dict, Any
import re

servidor_mcp_mathfunctions = FastMCP(name="Servidor de Modernidade e Funções Matemáticas",
    instructions="""
        Servidor com ferramentas de cálculo e avaliação de modernidade tecnológica TOTALMENTE INTEGRADO aos agentes LLM.
        
        🚨 IMPORTANTE: A base de conhecimento inicia VAZIA e é populada 100% pelos agentes!
        
        FLUXO OBRIGATÓRIO:
        1. inicializar_base_vazia() → Preparar estrutura
        2. Agentes do teste.py categorizam artefatos → tabela markdown  
        3. Agentes especialistas analisam cada categoria → receber_analise_agente()
        4. Agentes populam a base → atualizar_base_conhecimento() [ESSENCIAL]
        5. Gerar relatório final → gerar_relatorio_modernidade_completo()
        
        🎯 SEM AGENTES = SEM AVALIAÇÃO: O sistema depende 90% das análises dos agentes.
        
        Ferramentas disponíveis:
        - calcular_media(): função matemática auxiliar
        - calcular_soma(): função matemática auxiliar
    """,
)


###############################
# Tool: calcular_media (existente)
###############################
@servidor_mcp_mathfunctions.tool()
async def calcular_media(numeros: List[int | float | str]) -> Dict[str, Any]:
    """Calcula a média de uma lista de números com tratamento robusto de dados."""
    if not numeros:
        return {"sucesso": False, "erro": "Lista vazia fornecida", "media": None}
    numeros_validos: List[float] = []
    valores_ignorados: List[Dict[str, Any]] = []
    for i, num in enumerate(numeros):
        try:
            if isinstance(num, str):
                num_limpo = num.strip().replace(',', '.')
                valor_convertido = float(num_limpo)
            else:
                valor_convertido = float(num)
            numeros_validos.append(valor_convertido)
        except (ValueError, TypeError):
            valores_ignorados.append({"posicao": i, "valor": num})
    if not numeros_validos:
        return {"sucesso": False, "erro": "Nenhum valor numérico válido encontrado", "media": None, "valores_ignorados": valores_ignorados}
    media = sum(numeros_validos) / len(numeros_validos)
    return {"sucesso": True, "media": round(media, 1), "total_valores": len(numeros_validos), "valores_ignorados": valores_ignorados, "valores_processados": numeros_validos}

###############################
# Tool: calcular_soma (existente)
###############################
@servidor_mcp_mathfunctions.tool()
async def calcular_soma(numeros: List[int | float | str]) -> Dict[str, Any]:
    """Calcula a soma de uma lista de números com tratamento robusto de dados."""
    if not numeros:
        return {"sucesso": False, "erro": "Lista vazia fornecida", "media": None}
    numeros_validos: List[float] = []
    valores_ignorados: List[Dict[str, Any]] = []
    for i, num in enumerate(numeros):
        try:
            if isinstance(num, str):
                num_limpo = num.strip().replace(',', '.')
                valor_convertido = float(num_limpo)
            else:
                valor_convertido = float(num)
            numeros_validos.append(valor_convertido)
        except (ValueError, TypeError):
            valores_ignorados.append({"posicao": i, "valor": num})
    if not numeros_validos:
        return {"sucesso": False, "erro": "Nenhum valor numérico válido encontrado", "media": None, "valores_ignorados": valores_ignorados}
    soma = sum(numeros_validos) 
    return {"sucesso": True, "soma": soma, "total_valores": len(numeros_validos), "valores_ignorados": valores_ignorados, "valores_processados": numeros_validos}


###############################
if __name__ == "__main__":
    servidor_mcp_mathfunctions.run(transport="sse", port=8082)

