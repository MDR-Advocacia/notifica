# arquivo: automacao_documentos.py
import sqlite3
import os
from pathlib import Path
from datetime import datetime, timedelta
from playwright.sync_api import Page

# Define o nome do banco de dados de onde os NPJs serão lidos
DB_ARQUIVO_DOCUMENTOS = "dados_inclusao_docs.db"

# ATUALIZADO: A função agora lê também a quantidade de dias para o cálculo da data
def ler_dados_de_inclusao_docs(nome_banco: str = DB_ARQUIVO_DOCUMENTOS) -> list[dict]:
    """Lê NPJ e Qtd Dias Gerada da tabela 'inclusao_documentos'."""
    print(f"\nLendo dados do banco '{nome_banco}'...")
    try:
        if not Path(nome_banco).exists():
            print(f"    - Arquivo de banco de dados '{nome_banco}' não encontrado.")
            return []
        conn = sqlite3.connect(nome_banco)
        # Retorna os resultados como dicionários
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inclusao_documentos'")
        if cursor.fetchone() is None:
            print(f"    - Tabela 'inclusao_documentos' não encontrada.")
            return []
            
        cursor.execute("SELECT NPJ, Qtd_Dias_Gerada FROM inclusao_documentos")
        # Converte o resultado para uma lista de dicionários padrão
        dados = [dict(row) for row in cursor.fetchall()]
        conn.close()
        print(f"    - {len(dados)} registros de inclusão de docs encontrados.")
        return dados
    except sqlite3.Error as e:
        print(f"    - ERRO ao ler o banco de dados: {e}")
        return []

def clicar_acordeao_documentos(page: Page) -> None:
    """Na página de detalhes do processo, localiza e clica no acordeão 'Documentos'."""
    try:
        print("    - Procurando pelo menu 'Documentos'...")
        acordeao_documentos = page.get_by_role("button", name="Documentos", exact=True)
        acordeao_documentos.wait_for(state="visible", timeout=10000)
        
        print("    - Clicando em 'Documentos' para expandir...")
        acordeao_documentos.click()
        
        page.wait_for_load_state("networkidle", timeout=20000)
        print("    - ✅ Seção 'Documentos' expandida.")
        
    except Exception as e:
        raise Exception(f"Não foi possível clicar no menu 'Documentos': {e}")

# --- NOVA FUNÇÃO PARA BAIXAR OS ARQUIVOS ---
def baixar_documentos_por_data(page: Page, data_alvo: str, npj: str) -> None:
    """
    Encontra as linhas na tabela de documentos que correspondem à data_alvo e baixa os arquivos.
    """
    print(f"    - Procurando por documentos com a data: {data_alvo}...")
    
    # Localiza todas as linhas da tabela que contêm a data formatada
    linhas_da_data = page.locator(f"tbody tr:has-text('{data_alvo}')")
    
    count = linhas_da_data.count()
    if count == 0:
        print(f"    - ⚠️ Nenhum documento encontrado para a data {data_alvo}.")
        return

    print(f"    - {count} documento(s) encontrado(s) para a data. Iniciando downloads...")

    # Cria a pasta de downloads se não existir
    pasta_base = "downloads"
    # Sanitiza o NPJ para usar como nome de pasta (substitui / e - por _)
    pasta_npj = npj.replace("/", "_").replace("-", "_")
    caminho_completo = Path(pasta_base) / pasta_npj
    caminho_completo.mkdir(parents=True, exist_ok=True)

    # Itera sobre cada linha encontrada
    for i in range(count):
        linha = linhas_da_data.nth(i)
        
        # Encontra o link de download dentro da linha
        link_download = linha.locator("a[href*='/download/']")
        
        if link_download.count() > 0:
            try:
                # Espera pelo evento de download que será iniciado pelo clique
                with page.expect_download() as download_info:
                    link_download.click()
                
                download = download_info.value
                
                # Define o caminho para salvar o arquivo
                nome_arquivo = download.suggested_filename
                caminho_salvar = caminho_completo / nome_arquivo
                
                # Salva o arquivo
                download.save_as(caminho_salvar)
                print(f"    - ✅ Download concluído: {caminho_salvar}")
                
            except Exception as e:
                print(f"    - ❌ ERRO ao tentar baixar o arquivo da linha {i+1}: {e}")
        else:
            print(f"    - ⚠️ Linha {i+1} encontrada para a data, mas não continha um link de download.")


def navegar_para_detalhes_e_baixar_documentos(page: Page, lista_de_documentos: list[dict]) -> None:
    """Navega para a página de detalhes, calcula a data e chama a função de download."""
    url_base = "https://juridico.bb.com.br/paj/app/paj-cadastro/spas/processo/consulta/processo-consulta.app.html#/editar/"

    for doc_info in lista_de_documentos:
        npj = doc_info.get('NPJ')
        qtd_dias_str = doc_info.get('Qtd_Dias_Gerada')

        if not npj or qtd_dias_str is None:
            continue
        
        try:
            # --- CÁLCULO DA DATA ---
            qtd_dias = int(qtd_dias_str)
            data_alvo = datetime.now() - timedelta(days=qtd_dias)
            data_formatada = data_alvo.strftime('%d/%m/%Y')
            
            print(f"\n    - Processando NPJ de Inclusão de Documento: {npj}")
            print(f"    - 'Gerada em: {qtd_dias}' dias. Data alvo: {data_formatada}")

            ano, resto = npj.split('/')
            numero, variacao_str = resto.split('-')
            url_final = f"{url_base}{ano + numero}/{int(variacao_str)}/1"
            
            print(f"    - Navegando para URL de detalhes: {url_final}")
            page.goto(url_final)
            page.wait_for_load_state("networkidle", timeout=30000)
            
            page.locator("i.ci.ci--barcode").first.wait_for(state="visible", timeout=15000)
            print("    - ✅ Página de detalhes carregada com sucesso!")
            
            clicar_acordeao_documentos(page)

            # Chama a nova função para baixar os arquivos
            baixar_documentos_por_data(page, data_formatada, npj)

        except Exception as e:
            print(f"    - ❌ ERRO no processamento do NPJ {npj}: {e}")
            page.screenshot(path=f"erro_processo_documento_{npj.replace('/', '-')}.png")
            continue

def iniciar_processamento_de_documentos(page: Page) -> None:
    """Função principal que orquestra a leitura e o download dos documentos."""
    print("\n" + "="*20)
    print("INICIANDO PROCESSAMENTO DE INCLUSÃO DE DOCUMENTOS")
    print("="*20)
    
    dados_para_processar = ler_dados_de_inclusao_docs()
    if dados_para_processar:
        navegar_para_detalhes_e_baixar_documentos(page, dados_para_processar)
    else:
        print("    - Nenhum NPJ da tarefa 'Inclusão de Documentos' foi encontrado para processar.")