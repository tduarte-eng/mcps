from fastmcp import FastMCP
from ddgs import DDGS

servidor_mcp_websearch = FastMCP(name="Servidor de Assistente de Busca na Web",
    instructions="""
        Esse servidor prove ferramentas de busca na Web.
        Chame duckduckgo_search() para realizar uma busca na web.
    """,
)

#@servidor_mcp.tool()
#async def dar_bom_dia(nome_usuario: str, id_usuario: int) -> str: 
#    return f"Bom dia, {nome_usuario}! Seu ID é {id_usuario}."

@servidor_mcp_websearch.tool()
async def duckduckgo_search(query: str) -> str:
    """
    Realiza uma busca na web usando DuckDuckGo e retorna os principais resultados.
    """
    with DDGS() as ddgs:
        resultados = ddgs.text(query, max_results=5)
        if not resultados:
            return "Nenhum resultado encontrado."
        
        # Formata os resultados como texto
        saida = "\n".join([f"- {r['title']}: {r['href']}" for r in resultados])
        return saida


if __name__ == "__main__":
    servidor_mcp_websearch.run(transport="sse", port=8080)

