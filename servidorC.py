from fastmcp import FastMCP
import psycopg2

# Configuração da conexão com o banco
conn = psycopg2.connect(
    dbname="mcpdb",
    user="postgres",
    password="3mQ0XXMi{5-G",
    host="localhost",
    port="5432"
)

servidor_mcp_postgres = FastMCP(name="Servidor de Assistente de Consulta ao Banco de Dados PostgreSQL",
    instructions="""
        Esse servidor implementa funções SOMENTE de CONSULTA em banco de dados Postgres.
        Chame get_user_account() para trazer o salário de uma lista de usuários.
        Chame get_names() para trazer uma lista de nomes disponíveis no banco.
    """,
)

#@servidor_mcp.tool()
#async def dar_bom_dia(nome_usuario: str, id_usuario: int) -> str: 
#    return f"Bom dia, {nome_usuario}! Seu ID é {id_usuario}."

@servidor_mcp_postgres.tool()
async def get_user_account(names: list[str]) -> str:
    """
    Recebe uma lista de nomes e retorna o salário de cada usuário.
    
    Args:
        numeros: Lista de nomes para consultar no BD
        
    Returns:
        str: Resultado com salários ou mensagens de erro
    """
    if not names:
        return "Lista vazia fornecida"
    
    resultados = []
    try:
        with conn.cursor() as cur:
            for name in names:
                cur.execute("SELECT salary FROM pessoas WHERE name = %s", (name,))
                salario = cur.fetchone()
                if salario:
                    resultados.append(f"{name}: {salario[0]}")
                else:
                    resultados.append(f"{name}: Usuário não encontrado")
    except Exception as e:
        return f"Erro ao consultar o banco: {e}"
    
    return "\n".join(resultados)


@servidor_mcp_postgres.tool()
async def get_names() -> list[str]:
    """
    Retorna uma lista de nomes do banco de dados.

    input: None

    Returns:
        list[str]: Lista de nomes encontrados na tabela 'pessoas'
    """
    nomes = []
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM pessoas")
            rows = cur.fetchall()
            nomes = [row[0] for row in rows]
    except Exception as e:
        return [f"Erro ao consultar o banco: {e}"]
    
    return nomes

if __name__ == "__main__":
    servidor_mcp_postgres.run(transport="sse", port=8082)

