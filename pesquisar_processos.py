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
    """Navega para a página de consulta e pesquisa cada NPJ da lista."""
    print("\nIniciando módulo de pesquisa de processos...")
    
    url_pesquisa = "https://juridico.bb.com.br/paj/juridico/v2?app=processoConsultaApp"
    print(f"    - Navegando para a página de pesquisa: {url_pesquisa}")
    page.goto(url_pesquisa)

    print("    - Aguardando a página de pesquisa carregar completamente...")
    page.locator("div.col-xs-15.ta-left").wait_for(state="visible", timeout=20000)
    print("    - Página de pesquisa pronta.")

    for npj in lista_de_npjs:
        try:
            print(f"    - Pesquisando NPJ: {npj}")
            
            campo_pesquisa = page.locator("#focus1")
            campo_pesquisa.fill(npj)
            print(f"    - NPJ '{npj}' inserido no campo.")

            botao_buscar = page.locator("#buscar")
            print("    - Clicando no botão 'Buscar'...")
            botao_buscar.click()

            page.wait_for_load_state("networkidle", timeout=30000)
            print("    - Pesquisa realizada com sucesso.")
            
            time.sleep(3)

        except Exception as e:
            print(f"    - ERRO ao pesquisar o NPJ {npj}: {e}")
            continue
