"""
Servidor MCP para Geração de Gráficos com Matplotlib

Este servidor oferece ferramentas para criar visualizações de dados de modernidade tecnológica.
"""

from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import matplotlib
matplotlib.use('Agg')  # Backend sem GUI
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np
from datetime import datetime

servidor_mcp_graficos = FastMCP(
    name="Servidor de Gráficos",
    instructions="""
        Servidor especializado em geração de visualizações de dados usando Matplotlib.
        
        Ferramentas disponíveis:
        - gerar_grafico_barras(): cria gráfico de barras vertical
        - gerar_grafico_barras_horizontal(): cria gráfico de barras horizontal
        - gerar_grafico_pizza(): cria gráfico de pizza
        - gerar_grafico_radar(): cria gráfico radar (spider chart)
        - gerar_grafico_linha(): cria gráfico de linha
        - gerar_grafico_maturidade(): gráfico específico para matriz de maturidade
        - gerar_dashboard_completo(): cria dashboard com múltiplos gráficos
    """,
)


def _get_output_path(nome_arquivo: str) -> Path:
    """Retorna o path completo para salvar gráficos."""
    # Path correto: /home/bnb-admin/DEV/projectiam/outputs/graficos/
    output_dir = Path("/home/bnb-admin/DEV/projectiam/outputs/graficos")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return output_dir / f"{nome_arquivo}_{timestamp}.png"


@servidor_mcp_graficos.tool()
async def gerar_grafico_barras(
    categorias: List[str],
    valores: List[float],
    titulo: str = "Gráfico de Barras",
    xlabel: str = "Categorias",
    ylabel: str = "Valores",
    cor: str = "steelblue"
) -> Dict[str, Any]:
    """
    Gera um gráfico de barras vertical.
    
    Args:
        categorias: Lista de nomes das categorias
        valores: Lista de valores numéricos
        titulo: Título do gráfico
        xlabel: Label do eixo X
        ylabel: Label do eixo Y
        cor: Cor das barras (nome ou hex)
    """
    try:
        if len(categorias) != len(valores):
            return {"sucesso": False, "erro": "Categorias e valores devem ter o mesmo tamanho"}
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Criar barras
        bars = ax.bar(categorias, valores, color=cor, alpha=0.8, edgecolor='black')
        
        # Adicionar valores no topo das barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Salvar
        output_path = _get_output_path("grafico_barras")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "sucesso": True,
            "caminho": str(output_path),
            "tipo": "barras_vertical",
            "categorias_count": len(categorias)
        }
    
    except Exception as e:
        plt.close('all')
        return {"sucesso": False, "erro": str(e)}


@servidor_mcp_graficos.tool()
async def gerar_grafico_barras_horizontal(
    categorias: List[str],
    valores: List[float],
    titulo: str = "Gráfico de Barras Horizontal",
    xlabel: str = "Valores",
    ylabel: str = "Categorias",
    cor: str = "#2E86AB"
) -> Dict[str, Any]:
    """
    Gera um gráfico de barras horizontal (ideal para muitas categorias).
    """
    try:
        if len(categorias) != len(valores):
            return {"sucesso": False, "erro": "Categorias e valores devem ter o mesmo tamanho"}
        
        fig, ax = plt.subplots(figsize=(10, max(6, len(categorias) * 0.5)))
        
        # Criar barras horizontais
        bars = ax.barh(categorias, valores, color=cor, alpha=0.8, edgecolor='black')
        
        # Adicionar valores no final das barras
        for i, (bar, valor) in enumerate(zip(bars, valores)):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f' {valor:.1f}',
                   ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        # Salvar
        output_path = _get_output_path("grafico_barras_horizontal")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "sucesso": True,
            "caminho": str(output_path),
            "tipo": "barras_horizontal",
            "categorias_count": len(categorias)
        }
    
    except Exception as e:
        plt.close('all')
        return {"sucesso": False, "erro": str(e)}


@servidor_mcp_graficos.tool()
async def gerar_grafico_pizza(
    categorias: List[str],
    valores: List[float],
    titulo: str = "Distribuição por Categoria",
    mostrar_percentual: bool = True
) -> Dict[str, Any]:
    """
    Gera um gráfico de pizza.
    """
    try:
        if len(categorias) != len(valores):
            return {"sucesso": False, "erro": "Categorias e valores devem ter o mesmo tamanho"}
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Cores vibrantes
        colors = plt.cm.Set3(np.linspace(0, 1, len(categorias)))
        
        # Criar pizza
        if mostrar_percentual:
            autopct = '%1.1f%%'
        else:
            autopct = lambda p: f'{p * sum(valores) / 100:.1f}'
        
        wedges, texts, autotexts = ax.pie(
            valores,
            labels=categorias,
            autopct=autopct,
            colors=colors,
            startangle=90,
            pctdistance=0.85,
            explode=[0.05] * len(categorias)  # Separar fatias levemente
        )
        
        # Melhorar aparência dos textos
        for text in texts:
            text.set_fontsize(11)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Salvar
        output_path = _get_output_path("grafico_pizza")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "sucesso": True,
            "caminho": str(output_path),
            "tipo": "pizza",
            "categorias_count": len(categorias)
        }
    
    except Exception as e:
        plt.close('all')
        return {"sucesso": False, "erro": str(e)}


@servidor_mcp_graficos.tool()
async def gerar_grafico_radar(
    categorias: List[str],
    valores: List[float],
    titulo: str = "Gráfico Radar",
    valor_maximo: float = 10.0
) -> Dict[str, Any]:
    """
    Gera um gráfico radar (spider chart) para visualizar múltiplas dimensões.
    Ideal para mostrar perfil de maturidade.
    """
    try:
        if len(categorias) != len(valores):
            return {"sucesso": False, "erro": "Categorias e valores devem ter o mesmo tamanho"}
        
        # Número de variáveis
        num_vars = len(categorias)
        
        # Calcular ângulos
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        valores_plot = valores + [valores[0]]  # Fechar o círculo
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Desenhar o gráfico
        ax.plot(angles, valores_plot, 'o-', linewidth=2, color='#2E86AB', label='Pontuação')
        ax.fill(angles, valores_plot, alpha=0.25, color='#2E86AB')
        
        # Configurar labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categorias, fontsize=11, fontweight='bold')
        
        # Configurar escala radial
        ax.set_ylim(0, valor_maximo)
        ax.set_yticks(np.linspace(0, valor_maximo, 5))
        ax.set_yticklabels([f'{v:.1f}' for v in np.linspace(0, valor_maximo, 5)], fontsize=9)
        
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=30)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        plt.tight_layout()
        
        # Salvar
        output_path = _get_output_path("grafico_radar")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "sucesso": True,
            "caminho": str(output_path),
            "tipo": "radar",
            "categorias_count": len(categorias)
        }
    
    except Exception as e:
        plt.close('all')
        return {"sucesso": False, "erro": str(e)}


@servidor_mcp_graficos.tool()
async def gerar_grafico_maturidade(
    dados_maturidade: List[Dict[str, Any]],
    titulo: str = "Matriz de Maturidade Tecnológica"
) -> Dict[str, Any]:
    """
    Gera um gráfico específico para matriz de maturidade com cores baseadas na pontuação.
    
    Args:
        dados_maturidade: Lista de dicts com keys: 'categoria', 'artefatos', 'modernidade'
    """
    try:
        if not dados_maturidade:
            return {"sucesso": False, "erro": "Dados de maturidade vazios"}
        
        categorias = [d.get('categoria', '') for d in dados_maturidade]
        valores = [float(d.get('modernidade', 0)) for d in dados_maturidade]
        
        # Definir cores baseadas na pontuação
        cores = []
        for valor in valores:
            if valor >= 8.0:
                cores.append('#27AE60')  # Verde - Excelente
            elif valor >= 6.0:
                cores.append('#F39C12')  # Laranja - Bom
            elif valor >= 4.0:
                cores.append('#E67E22')  # Laranja escuro - Regular
            else:
                cores.append('#E74C3C')  # Vermelho - Crítico
        
        fig, ax = plt.subplots(figsize=(12, max(6, len(categorias) * 0.6)))
        
        # Criar barras horizontais
        bars = ax.barh(categorias, valores, color=cores, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Adicionar valores e artefatos
        for i, (bar, valor, dado) in enumerate(zip(bars, valores, dados_maturidade)):
            width = bar.get_width()
            artefatos = dado.get('artefatos', '')
            
            # Valor da pontuação
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f' {valor:.1f}/10',
                   ha='left', va='center', fontsize=11, fontweight='bold')
            
            # Nome dos artefatos (dentro da barra)
            if width > 1.0:  # Se a barra for grande o suficiente
                ax.text(width/2, bar.get_y() + bar.get_height()/2.,
                       f'{artefatos}',
                       ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        
        ax.set_xlabel('Pontuação de Modernidade (0-10)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Categorias', fontsize=12, fontweight='bold')
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlim(0, 10)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        # Legenda de cores
        legend_elements = [
            mpatches.Patch(color='#27AE60', label='Excelente (8-10)'),
            mpatches.Patch(color='#F39C12', label='Bom (6-8)'),
            mpatches.Patch(color='#E67E22', label='Regular (4-6)'),
            mpatches.Patch(color='#E74C3C', label='Crítico (0-4)')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        plt.tight_layout()
        
        # Salvar
        output_path = _get_output_path("grafico_maturidade")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "sucesso": True,
            "caminho": str(output_path),
            "tipo": "maturidade",
            "categorias_count": len(categorias),
            "media_geral": round(sum(valores) / len(valores), 2)
        }
    
    except Exception as e:
        plt.close('all')
        return {"sucesso": False, "erro": str(e)}


@servidor_mcp_graficos.tool()
async def gerar_dashboard_completo(
    dados_maturidade: List[Dict[str, Any]],
    titulo_projeto: str = "Dashboard de Modernidade"
) -> Dict[str, Any]:
    """
    Gera um dashboard completo com múltiplos gráficos em uma única imagem.
    """
    try:
        if not dados_maturidade:
            return {"sucesso": False, "erro": "Dados vazios"}
        
        categorias = [d.get('categoria', '') for d in dados_maturidade]
        valores = [float(d.get('modernidade', 0)) for d in dados_maturidade]
        
        # Criar figura com subplots
        fig = plt.figure(figsize=(16, 10))
        
        # 1. Gráfico de Barras (principal)
        ax1 = plt.subplot(2, 2, 1)
        cores_barras = ['#27AE60' if v >= 8 else '#F39C12' if v >= 6 else '#E67E22' if v >= 4 else '#E74C3C' for v in valores]
        bars = ax1.barh(categorias, valores, color=cores_barras, alpha=0.8, edgecolor='black')
        for bar, valor in zip(bars, valores):
            width = bar.get_width()
            ax1.text(width, bar.get_y() + bar.get_height()/2., f' {valor:.1f}',
                    ha='left', va='center', fontsize=9, fontweight='bold')
        ax1.set_xlabel('Pontuação', fontsize=10, fontweight='bold')
        ax1.set_title('Pontuação por Categoria', fontsize=11, fontweight='bold')
        ax1.set_xlim(0, 10)
        ax1.grid(axis='x', alpha=0.3)
        
        # 2. Gráfico de Pizza (distribuição)
        ax2 = plt.subplot(2, 2, 2)
        colors_pizza = plt.cm.Set3(np.linspace(0, 1, len(categorias)))
        ax2.pie(valores, labels=categorias, autopct='%1.1f%%', colors=colors_pizza, startangle=90)
        ax2.set_title('Distribuição de Pontuações', fontsize=11, fontweight='bold')
        
        # 3. Gráfico Radar (perfil)
        ax3 = plt.subplot(2, 2, 3, projection='polar')
        num_vars = len(categorias)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        valores_radar = valores + [valores[0]]
        angles += angles[:1]
        ax3.plot(angles, valores_radar, 'o-', linewidth=2, color='#2E86AB')
        ax3.fill(angles, valores_radar, alpha=0.25, color='#2E86AB')
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(categorias, fontsize=8)
        ax3.set_ylim(0, 10)
        ax3.set_title('Perfil de Maturidade', fontsize=11, fontweight='bold', pad=20)
        ax3.grid(True, alpha=0.3)
        
        # 4. Estatísticas (texto)
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        
        media_geral = sum(valores) / len(valores)
        valor_max = max(valores)
        valor_min = min(valores)
        categoria_max = categorias[valores.index(valor_max)]
        categoria_min = categorias[valores.index(valor_min)]
        
        stats_text = f"""
ESTATÍSTICAS GERAIS

📊 Média Geral: {media_geral:.2f}/10

🏆 Melhor Categoria:
   {categoria_max}: {valor_max:.1f}/10

⚠️ Categoria com Menor Pontuação:
   {categoria_min}: {valor_min:.1f}/10

📈 Total de Categorias: {len(categorias)}

💡 Amplitude: {valor_max - valor_min:.1f}
        """
        
        ax4.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        # Título geral
        fig.suptitle(titulo_projeto, fontsize=16, fontweight='bold', y=0.98)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Salvar
        output_path = _get_output_path("dashboard_completo")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "sucesso": True,
            "caminho": str(output_path),
            "tipo": "dashboard",
            "categorias_count": len(categorias),
            "media_geral": round(media_geral, 2),
            "estatisticas": {
                "melhor_categoria": categoria_max,
                "melhor_pontuacao": valor_max,
                "pior_categoria": categoria_min,
                "pior_pontuacao": valor_min
            }
        }
    
    except Exception as e:
        plt.close('all')
        return {"sucesso": False, "erro": str(e)}


if __name__ == "__main__":
    servidor_mcp_graficos.run(transport="sse", port=8083)
