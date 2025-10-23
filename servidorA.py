from fastmcp import FastMCP
from ddgs import DDGS
import json

servidor_mcp_websearch = FastMCP(name="Servidor de Assistente de Busca na Web",
    instructions="""
        Esse servidor provê ferramentas de busca na Web.
        Chame duckduckgo_search() para realizar uma busca na web e obter respostas.
    """,
)

@servidor_mcp_websearch.tool()
async def duckduckgo_search(query: str) -> str:
    """
    Realiza uma busca na web usando DuckDuckGo.
    Aceita:
      - Texto livre
      - JSON como: {"categoria": "Linguagem", "artefato": "Java 8"}
    Se JSON, constrói uma query para avaliar modernidade / estado atual.
    """
    def normalizar_categoria(categoria: str) -> str:
        """Normaliza nomes de categoria para padrões aceitos"""
        mapeamento_categorias = {
            "linguagem de programação": "Linguagem de Programação",
            "linguagem": "Linguagem de Programação", 
            "programming language": "Linguagem de Programação",
            "arquitetura": "Arquitetura de Sistemas",
            "sistemas": "Arquitetura de Sistemas",
            "infraestrutura": "Infraestrutura",
            "banco de dados": "Banco de Dados",
            "database": "Banco de Dados",
            "devsecops": "DevSecOps / Governança",
            "governança": "DevSecOps / Governança"
        }
        return mapeamento_categorias.get(categoria.lower(), categoria)

    def montar_query(q) -> str:
        # Se já for um dict, usa diretamente
        if isinstance(q, dict):
            data = q
        elif isinstance(q, str):
            try:
                # Primeiro, tenta decodificar unicode escapado
                if '\\u' in q:
                    q = q.encode().decode('unicode_escape')
                data = json.loads(q)
            except Exception:
                return q.strip()
        else:
            return str(q).strip()
        
        if isinstance(data, dict):
            valores = []
            for k, v in data.items():
                if k.lower() == "categoria" and isinstance(v, str):
                    # Normaliza a categoria
                    v = normalizar_categoria(v)
                
                if isinstance(v, str):
                    valores.append(v.strip())
                elif isinstance(v, (list, tuple)):
                    valores.extend([str(x).strip() for x in v])
            
            base = " ".join(v for v in valores if v)
            # Termos para capturar discussões sobre modernidade / relevância
            extras = "estado atual modernidade atualização roadmap ainda vale a pena obsoleto 2025"
            return f"{base} {extras}".strip()
        
        return str(q).strip()

    # Log da entrada para debug
    print(f"DEBUG: Query recebida: {query}")
    
    consulta = montar_query(query)
    print(f"DEBUG: Query processada: {consulta}")
    
    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(consulta, max_results=3)
            if not resultados:
                return f"Nenhum resultado encontrado para: {consulta}"

            saida_formatada = []
            for i, r in enumerate(resultados, 1):
                resultado_texto = f"""
{i}. **{r.get('title','(Sem título)')}**
Query: {consulta}
URL: {r.get('href','(Sem URL)')}
Conteúdo: {r.get('body', 'Sem conteúdo disponível')}
"""
                saida_formatada.append(resultado_texto.strip())

            return "\n\n".join(saida_formatada)
    
    except Exception as e:
        return f"Erro na busca: {str(e)} | Query: {consulta}"

if __name__ == "__main__":
    servidor_mcp_websearch.run(transport="sse", port=8081)

