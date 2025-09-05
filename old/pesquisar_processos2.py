# arquivo: pesquisar_processos.py
import time
import sqlite3
# Note: Não precisamos mais de playwright ou autologin aqui

# --- MÓDULO DE PESQUISA ---

def ler_npjs_para_pesquisa(nome_banco="dados_inclusao_docs.db"):
    """Lê todos os NPJs do banco de dados especificado e retorna uma lista."""
    print(f"\nLendo NPJs do banco de dados '{nome_banco}'...")
    try:
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inclusao_documentos'")
        if cursor.fetchone() is None:
            print(f"    - Tabela 'inclusao_documentos' não encontrada no banco de dados.")
            return []
            
        cursor.execute("SELECT NPJ FROM inclusao_documentos")
        npjs = [item[0] for item in cursor.fetchall()]
        conn.close()
        print(f"    - {len(npjs)} NPJs encontrados.")
        return npjs
    except sqlite3.Error as e:
        print(f"    - ERRO ao ler o banco de dados: {e}")
        return []

def pesquisar_processos_v2(page, lista_de_npjs):
    """Navega para a URL de consulta e pesquisa cada NPJ da lista."""
    print("\nIniciando módulo de pesquisa de processos (método URL direta)...")
    
    url_base = "https://juridico.bb.com.br/paj/juridico/v2?app=processoConsultaRapidoApp"

    for npj in lista_de_npjs:
        try:
            print(f"    - Pesquisando NPJ: {npj}")
            
            # Quebra o NPJ no formato "ANO/NUMERO-VARIACAO"
            ano, resto = npj.split('/')
            numero, variacao = resto.split('-')

            # Constrói a URL final com os parâmetros
            url_pesquisa_direta = f"{url_base}&anoProcesso={ano}&numeroProcesso={numero}&variacaoProcesso={variacao}"
            
            print(f"    - Navegando para: {url_pesquisa_direta}")
            page.goto(url_pesquisa_direta)

            page.wait_for_load_state("networkidle", timeout=30000)
            print("    - Página de resultados do processo carregada.")
            
            # ETAPA DE DETALHAMENTO (CORRIGIDA)
            print("\n    - Procurando o botão 'Detalhar' na tabela de resultados...")

            # Seletor mais específico que mira no <span> com a dica de ferramenta "Detalhar"
            botao_detalhar = page.locator('span[bb-tooltip="Detalhar"]')
            
            # Espera o botão estar visível, garantindo que a tabela carregou
            botao_detalhar.wait_for(state="visible", timeout=15000)
            print("    - Botão 'Detalhar' encontrado.")
            
            botao_detalhar.click()
            print("    - Clicando para ver os detalhes do processo...")
            
            page.wait_for_load_state("networkidle", timeout=30000)
            print("    - Página de detalhamento final carregada com sucesso.")

            time.sleep(3)

        except Exception as e:
            print(f"    - ERRO ao pesquisar o NPJ {npj}: {e}")
            continue

