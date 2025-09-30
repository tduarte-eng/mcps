from fastmcp import FastMCP
#from ddgs import DDGS

servidor_mcp_mathfunctions = FastMCP(name="Servidor de Assistente de Funções Matemáticas",
    instructions="""
        Esse servidor de ferramentas de funções matemáticas.
        Chame calcular_media() para calcular a média de uma lista de números.
    """,
)

#@servidor_mcp.tool()
#async def dar_bom_dia(nome_usuario: str, id_usuario: int) -> str: 
#    return f"Bom dia, {nome_usuario}! Seu ID é {id_usuario}."

@servidor_mcp_mathfunctions.tool()
async def calcular_media(numeros: list[int | float | str]) -> dict:
    """
    Calcula a média de uma lista de números com tratamento robusto de dados.
    
    Args:
        numeros: Lista que pode conter números, strings numéricas ou valores mistos
        
    Returns:
        dict: Resultado com média, estatísticas e avisos
    """
    if not numeros:
        return {
            "sucesso": False,
            "erro": "Lista vazia fornecida",
            "media": None
        }
    
    numeros_validos = []
    valores_ignorados = []
    
    for i, num in enumerate(numeros):
        try:
            # Tentar converter para float
            if isinstance(num, str):
                # Limpar string (remover espaços, vírgulas como separador decimal)
                num_limpo = num.strip().replace(',', '.')
                valor_convertido = float(num_limpo)
            else:
                valor_convertido = float(num)
            
            numeros_validos.append(valor_convertido)
            
        except (ValueError, TypeError):
            valores_ignorados.append({"posicao": i, "valor": num})
    
    if not numeros_validos:
        return {
            "sucesso": False,
            "erro": "Nenhum valor numérico válido encontrado",
            "media": None,
            "valores_ignorados": valores_ignorados
        }
    
    media = sum(numeros_validos) / len(numeros_validos)
    
    return {
        "sucesso": True,
        "media": round(media, 2),
        "total_valores": len(numeros_validos),
        "valores_ignorados": valores_ignorados,
        "valores_processados": numeros_validos
    }


if __name__ == "__main__":
    servidor_mcp_mathfunctions.run(transport="sse", port=8081)

