# arquivo: automacao_andamentos.py
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from playwright.sync_api import Page, TimeoutError

# --- CONSTANTES ---
DB_ARQUIVO_ANDAMENTOS = "dados_andamento_publicacao.db"

# --- FUNÇÕES DE BANCO DE DADOS ---
def salvar_texto_publicacao(npj: str, texto_publicacao: str, nome_banco: str = DB_ARQUIVO_ANDAMENTOS) -> None:
    """Atualiza a tabela de andamentos com o texto completo da publicação para um NPJ específico."""
    if not texto_publicacao:
        print("    - Nenhum texto para salvar.")
        return
    conn = None
    try:
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()
        try:
            cursor.execute("ALTER TABLE andamento_publicacao ADD COLUMN texto_publicacao TEXT")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise
        cursor.execute("INSERT OR IGNORE INTO andamento_publicacao (NPJ) VALUES (?)", (npj,))
        query = "UPDATE andamento_publicacao SET texto_publicacao = ? WHERE NPJ = ?"
        cursor.execute(query, (texto_publicacao.strip(), npj))
        conn.commit()
        print(f"    - ✅ Texto da publicação salvo para o NPJ {npj}.")
    except sqlite3.Error as e:
        print(f"\n    - ❌ ERRO ao salvar o texto da publicação no banco de dados: {e}")
    finally:
        if conn:
            conn.close()

# --- FUNÇÕES DE TESTE E AUTOMAÇÃO ---
def ler_npjs_para_teste(nome_banco: str = "dados_andamento_publicacao.db", limite: int = 10) -> list[str]:
    """Lê uma quantidade limitada de NPJs do próprio banco de 'andamentos' para fins de teste."""
    print(f"\n[MODO DE TESTE] Lendo {limite} NPJs do banco de dados '{nome_banco}'...")
    try:
        if not Path(nome_banco).exists():
            print(f"    - [MODO DE TESTE] Arquivo de banco de dados para teste '{nome_banco}' não encontrado.")
            return []
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()
        cursor.execute(f"SELECT NPJ FROM andamento_publicacao LIMIT {limite}")
        npjs = [item[0] for item in cursor.fetchall()]
        conn.close()
        print(f"    - [MODO DE TESTE] {len(npjs)} NPJs de teste encontrados.")
        return npjs
    except sqlite3.Error as e:
        print(f"    - [MODO DE TESTE] ERRO ao ler o banco de dados: {e}")
        return []

def clicar_no_menu_andamentos(page: Page) -> None:
    """Na página de detalhes, clica no menu 'Andamentos'."""
    try:
        print("    - Procurando pelo menu 'Andamentos'...")
        menu_andamentos = page.locator("li:has-text('Andamentos')")
        menu_andamentos.wait_for(state="visible", timeout=10000)
        print("    - Clicando em 'Andamentos'...")
        menu_andamentos.click()
        page.wait_for_load_state("networkidle", timeout=20000)
        print("    - ✅ Seção 'Andamentos' carregada.")
    except Exception as e:
        raise Exception(f"Não foi possível clicar no menu 'Andamentos': {e}")

def detalhar_e_extrair_publicacao(page: Page, npj: str, data_publicacao: str = None) -> None:
    """
    Encontra a publicação correta, abre o modal, clica em 'Leia mais', 
    extrai o texto e salva no banco.
    """
    linha_alvo = None
    if data_publicacao:
        print(f"    - Procurando pela publicação com a data: {data_publicacao}...")
        linha_alvo = page.locator(f"tr:has-text('PUBLICACAO DJ/DO'):has-text('{data_publicacao}')").first
    else:
        print("    - [MODO DE TESTE] Procurando pela primeira 'PUBLICACAO DJ/DO' disponível...")
        linha_alvo = page.locator("tr:has-text('PUBLICACAO DJ/DO')").first

    try:
        linha_alvo.wait_for(state="visible", timeout=15000)
        print("    - Linha da publicação correta encontrada.")
        
        botao_detalhar_publicacao = linha_alvo.locator('a[bb-tooltip="Detalhar publicação"]')
        if botao_detalhar_publicacao.count() == 0:
            print("    - ⚠️ Aviso: 'PUBLICACAO DJ/DO' encontrada, mas não possui botão para detalhar. Pulando.")
            return

        botao_detalhar_publicacao.click()

        modal = page.locator("div.modal__content")
        modal.wait_for(state="visible", timeout=10000)
        print("    - Modal de detalhes da publicação aberto.")

        componente_texto = modal.locator("texto-grande-detalhar")
        
        try:
            leia_mais_botao = componente_texto.get_by_role("button", name="Leia mais")
            leia_mais_botao.wait_for(state="visible", timeout=2000)
            print("    - Botão 'Leia mais' encontrado. Clicando para expandir o texto...")
            leia_mais_botao.click()
            modal.locator("button:has-text('Leia menos')").wait_for(state="visible", timeout=3000)
            print("    - Texto expandido.")
        except TimeoutError:
            print("    - Botão 'Leia mais' não encontrado no tempo previsto, o texto já deve estar completo.")

        texto_container = componente_texto.locator("p.ng-binding")
        texto_container.wait_for(state="visible", timeout=5000)
        texto_extraido = texto_container.inner_text()
        
        if texto_extraido:
            if data_publicacao is None:
                texto_extraido = "[CONTEÚDO OBTIDO EM MODO DE TESTE]\n\n" + texto_extraido
            salvar_texto_publicacao(npj, texto_extraido)
        
        print("    - Fechando o modal...")
        page.locator("div.modal__close").click()
        modal.wait_for(state="hidden", timeout=5000)

    except TimeoutError:
        mensagem = f"com a data '{data_publicacao}'" if data_publicacao else "disponível"
        print(f"    - ⚠️ AVISO: Nenhuma 'PUBLICACAO DJ/DO' {mensagem} foi encontrada para este NPJ. Pulando para o próximo.")
        if page.locator("div.modal__close").count() > 0:
            page.locator("div.modal__close").click()
        return
    except Exception as e:
        raise Exception(f"Erro ao tentar detalhar a publicação: {e}")

def navegar_para_detalhes_e_processar(page: Page, lista_de_andamentos: list[dict]) -> None:
    """Navega para a página de detalhes de cada NPJ (modo normal)."""
    print("\nIniciando módulo de navegação e processamento detalhado de andamentos...")
    url_base = "https://juridico.bb.com.br/paj/app/paj-cadastro/spas/processo/consulta/processo-consulta.app.html#/editar/"

    for andamento in lista_de_andamentos:
        npj = andamento.get('NPJ')
        data_gerada_completa = andamento.get('Gerada em')
        if not npj or not data_gerada_completa:
            continue
        data_apenas = data_gerada_completa.split(" ")[0]
        
        try:
            print(f"    - Processando NPJ de andamento: {npj}")
            ano, resto = npj.split('/')
            numero, variacao_str = resto.split('-')
            url_final = f"{url_base}{ano + numero}/{int(variacao_str)}/1"
            
            page.goto(url_final)
            page.wait_for_load_state("networkidle", timeout=30000)
            page.locator("i.ci.ci--barcode").first.wait_for(state="visible", timeout=15000)
            print("    - ✅ Página de detalhes carregada com sucesso!")
            
            clicar_no_menu_andamentos(page)
            detalhar_e_extrair_publicacao(page, npj, data_apenas)

        except Exception as e:
            print(f"    - ❌ ERRO no processamento do NPJ {npj}: {e}")
            page.screenshot(path=f"erro_processo_andamento_{npj.replace('/', '-')}.png")
            continue

def iniciar_processamento_de_andamentos(page: Page, lista_de_andamentos: list[dict]) -> None:
    """Função principal que orquestra o processamento dos andamentos."""
    print("\n" + "="*20)
    print("INICIANDO PROCESSAMENTO DE ANDAMENTOS DE PUBLICAÇÃO")
    print("="*20)
    
    lista_unica = []
    npjs_vistos = set()
    for andamento in lista_de_andamentos:
        npj = andamento.get('NPJ')
        if npj and npj not in npjs_vistos:
            lista_unica.append(andamento)
            npjs_vistos.add(npj)
    
    if lista_unica:
        print(f"    - {len(lista_de_andamentos)} andamento(s) foram coletados. {len(lista_unica)} são únicos e serão processados.")
        navegar_para_detalhes_e_processar(page, lista_unica)
    else:
        print("\n    - Nenhum andamento real encontrado. Ativando MODO DE TESTE.")
        npjs_de_teste = ler_npjs_para_teste()

        if not npjs_de_teste:
            print("    - [MODO DE TESTE] Nenhum NPJ encontrado no banco de dados de teste para processar.")
            return

        url_base = "https://juridico.bb.com.br/paj/app/paj-cadastro/spas/processo/consulta/processo-consulta.app.html#/editar/"
        for npj in npjs_de_teste:
            try:
                print(f"    - [MODO DE TESTE] Processando NPJ: {npj}")
                ano, resto = npj.split('/')
                numero, variacao_str = resto.split('-')
                url_final = f"{url_base}{ano + numero}/{int(variacao_str)}/1"

                page.goto(url_final)
                page.locator("i.ci.ci--barcode").first.wait_for(state="visible", timeout=15000)
                print("    - ✅ [MODO DE TESTE] Página de detalhes carregada.")

                clicar_no_menu_andamentos(page)
                detalhar_e_extrair_publicacao(page, npj)

            except Exception as e:
                print(f"    - ❌ [MODO DE TESTE] ERRO no processamento do NPJ {npj}: {e}")
                continue