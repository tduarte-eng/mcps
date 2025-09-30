import asyncio
from pathlib import Path

from fastmcp import Client

caminho_servidor = 'http://127.0.0.1:8000/sse'

cliente = Client(caminho_servidor)

async def testar_servidor(cliente, nome_usuario: str, id_usuario: int):
    async with cliente:
        argumentos = {"nome_usuario": nome_usuario, "id_usuario": id_usuario}
        resultado = await cliente.call_tool("dar_bom_dia", arguments=argumentos)
        print(resultado)

if __name__ == "__main__":
    asyncio.run(testar_servidor(cliente, "Alice", 12345))