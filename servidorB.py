"""
Servidor MCP para Funções Matemáticas de Avaliação de Modernidade

Este servidor oferece apenas ferramentas matemáticas para cálculos de modernidade tecnológica.
"""

from fastmcp import FastMCP
from typing import List, Dict, Any

servidor_mcp_mathfunctions = FastMCP(
    name="Servidor de Funções Matemáticas",
    instructions="""
        Servidor especializado em cálculos matemáticos para avaliação de modernidade tecnológica.
        
        Ferramentas disponíveis:
        - calcular_media(): calcula média de números
        - calcular_soma(): calcula soma de números  
        - calcular_pontuacao_artefato(): calcula pontuação total baseada nos 4 critérios
        - calcular_media_categoria(): calcula média de uma categoria de artefatos
        - validar_pontuacao(): valida se uma nota está no range correto
        - calcular_percentual(): calcula percentual de uma pontuação
    """,
)


@servidor_mcp_mathfunctions.tool()
async def calcular_media(numeros: List[float]) -> Dict[str, Any]:
    """Calcula a média de uma lista de números."""
    if not numeros:
        return {"sucesso": False, "erro": "Lista vazia", "media": 0}
    
    media = sum(numeros) / len(numeros)
    return {
        "sucesso": True,
        "media": round(media, 2),
        "total_valores": len(numeros)
    }


@servidor_mcp_mathfunctions.tool()
async def calcular_soma(numeros: List[float]) -> Dict[str, Any]:
    """Calcula a soma de uma lista de números."""
    if not numeros:
        return {"sucesso": False, "erro": "Lista vazia", "soma": 0}
    
    soma = sum(numeros)
    return {
        "sucesso": True,
        "soma": round(soma, 2),
        "total_valores": len(numeros)
    }


@servidor_mcp_mathfunctions.tool()
async def calcular_pontuacao_artefato(
    nota_versao_lts: float,
    nota_ecossistema: float,
    nota_ferramentas_teste: float,
    nota_modernidade: float
) -> Dict[str, Any]:
    """
    Calcula a pontuação total de um artefato baseado nos 4 critérios.
    
    Fórmula: Total = (versao_lts * 0.8) + (ecossistema * 0.1) + (ferramentas_teste * 0.05) + (modernidade * 0.05)
    """
    # Validações
    if not (0 <= nota_versao_lts <= 8.0):
        return {"sucesso": False, "erro": "nota_versao_lts deve estar entre 0 e 8.0"}
    if not (0 <= nota_ecossistema <= 1.0):
        return {"sucesso": False, "erro": "nota_ecossistema deve estar entre 0 e 1.0"}
    if not (0 <= nota_ferramentas_teste <= 0.5):
        return {"sucesso": False, "erro": "nota_ferramentas_teste deve estar entre 0 e 0.5"}
    if not (0 <= nota_modernidade <= 0.5):
        return {"sucesso": False, "erro": "nota_modernidade deve estar entre 0 e 0.5"}
    
    # Cálculo com pesos
    total = (nota_versao_lts * 0.8) + (nota_ecossistema * 0.1) + (nota_ferramentas_teste * 0.05) + (nota_modernidade * 0.05)
    percentual = (total / 10.0) * 100
    
    return {
        "sucesso": True,
        "total": round(total, 2),
        "percentual": round(percentual, 1),
        "componentes": {
            "versao_lts": round(nota_versao_lts * 0.8, 2),
            "ecossistema": round(nota_ecossistema * 0.1, 2),
            "ferramentas_teste": round(nota_ferramentas_teste * 0.05, 2),
            "modernidade": round(nota_modernidade * 0.05, 2)
        }
    }


@servidor_mcp_mathfunctions.tool()
async def calcular_media_categoria(pontuacoes: List[float]) -> Dict[str, Any]:
    """Calcula a média das pontuações de uma categoria."""
    if not pontuacoes:
        return {
            "sucesso": True,
            "media": 0.0,
            "total_itens": 0
        }
    
    # Filtrar valores válidos (0-10)
    pontuacoes_validas = [p for p in pontuacoes if 0 <= p <= 10]
    
    if not pontuacoes_validas:
        return {"sucesso": False, "erro": "Nenhuma pontuação válida (0-10)"}
    
    media = sum(pontuacoes_validas) / len(pontuacoes_validas)
    minima = min(pontuacoes_validas)
    maxima = max(pontuacoes_validas)
    
    return {
        "sucesso": True,
        "media": round(media, 2),
        "total_itens": len(pontuacoes_validas),
        "minima": round(minima, 2),
        "maxima": round(maxima, 2),
        "amplitude": round(maxima - minima, 2)
    }


@servidor_mcp_mathfunctions.tool()
async def validar_pontuacao(criterio: str, nota: float) -> Dict[str, Any]:
    """Valida se uma pontuação está dentro do range permitido."""
    ranges = {
        "versao_lts": {"min": 0, "max": 8.0},
        "ecossistema": {"min": 0, "max": 1.0},
        "ferramentas_teste": {"min": 0, "max": 0.5},
        "modernidade": {"min": 0, "max": 0.5}
    }
    
    if criterio not in ranges:
        return {"sucesso": False, "erro": f"Critério inválido: {criterio}"}
    
    r = ranges[criterio]
    valido = r["min"] <= nota <= r["max"]
    
    return {
        "sucesso": True,
        "valido": valido,
        "nota": nota,
        "range_min": r["min"],
        "range_max": r["max"]
    }


@servidor_mcp_mathfunctions.tool()
async def calcular_percentual(valor: float, total: float) -> Dict[str, Any]:
    """Calcula o percentual de um valor em relação ao total."""
    if total == 0:
        return {"sucesso": False, "erro": "Total não pode ser zero"}
    
    percentual = (valor / total) * 100
    
    return {
        "sucesso": True,
        "percentual": round(percentual, 2),
        "valor": valor,
        "total": total
    }


if __name__ == "__main__":
    servidor_mcp_mathfunctions.run(transport="sse", port=8082)