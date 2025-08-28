# arquivo: main_juridico.py
import time
import subprocess
import json
import sqlite3
import sys
from playwright.sync_api import sync_playwright, TimeoutError 
from autologin import realizar_login_automatico

# --- FUNÇÕES DE BANCO DE DADOS ---

def salvar_dados_inclusao_docs(dados, nome_banco="dados_inclusao_docs.db"):
    """Salva os dados de 'Inclusão de Documentos' em um banco SQLite."""
    if not dados: return
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    # Tabela ajustada para as colunas corretas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inclusao_documentos (
        NPJ TEXT PRIMARY KEY, 
        Adverso_Principal TEXT, 
        Numero_de_rastreamento TEXT, 
        Origem TEXT
    )''')
    registros_inseridos = 0
    for item in dados:
        cursor.execute('INSERT OR IGNORE INTO inclusao_documentos VALUES (?, ?, ?, ?)', 
                       (item.get('NPJ'), item.get('Adverso Principal'), item.get('Número de rastreamento'), item.get('Origem')))
        registros_inseridos += cursor.rowcount
    conn.commit()
    conn.close()
    print(f"\n✅ {registros_inseridos} novos registros de Inclusão de Documentos salvos em '{nome_banco}'.")

def salvar_dados_doc_externo(dados, nome_banco="dados_doc_externo.db"):
    """Salva os dados de 'Doc. anexado por empresa externa' em um banco SQLite."""
    if not dados: return
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS doc_externo (NPJ TEXT PRIMARY KEY, Adverso_Principal TEXT, Gerada_em TEXT)')
    registros_inseridos = 0
    for item in dados:
        cursor.execute('INSERT OR IGNORE INTO doc_externo VALUES (?, ?, ?)', (item.get('NPJ'), item.get('Adverso Principal'), item.get('Gerada em')))
        registros_inseridos += cursor.rowcount
    conn.commit()
    conn.close()
    print(f"\n✅ {registros_inseridos} novos registros de Documento Externo salvos em '{nome_banco}'.")

def salvar_dados_andamento_publicacao(dados, nome_banco="dados_andamento_publicacao.db"):
    """Salva os dados de 'Andamento de publicação' em um banco SQLite."""
    if not dados: return
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS andamento_publicacao (NPJ TEXT PRIMARY KEY, Adverso_Principal TEXT, Gerada_em TEXT)')
    registros_inseridos = 0
    for item in dados:
        cursor.execute('INSERT OR IGNORE INTO andamento_publicacao VALUES (?, ?, ?)', (item.get('NPJ'), item.get('Adverso Principal'), item.get('Gerada em')))
        registros_inseridos += cursor.rowcount
    conn.commit()
    conn.close()
    print(f"\n✅ {registros_inseridos} novos registros de Andamento de Publicação salvos em '{nome_banco}'.")

# --- FUNÇÃO DE EXTRAÇÃO GENÉRICA ---

def extrair_dados_com_paginacao(page, id_tabela, colunas_desejadas, limite_registros):
    dados_extraidos = []
    tabela = page.locator(f'[id="{id_tabela}"]')
    corpo_da_tabela = tabela.locator('tbody[id$=":tb"]')
    
    print("    - Aguardando dados da tabela...")
    corpo_da_tabela.locator("tr").first.wait_for(state="visible", timeout=20000)
    print("    - Tabela encontrada.")

    indices_colunas = {}
    headers = tabela.locator("thead th")
    for i in range(headers.count()):
        header_text = headers.nth(i).inner_text().strip()
        if header_text in colunas_desejadas:
            indices_colunas[header_text] = i
    print(f"    - Mapeamento de colunas: {indices_colunas}")

    pagina_atual = 1
    while True:
        print(f"\n--- Extraindo dados da página {pagina_atual} ---")
        corpo_da_tabela.wait_for(state="visible")
        
        for linha in corpo_da_tabela.locator("tr").all():
            item = {}
            for nome_coluna, indice in indices_colunas.items():
                item[nome_coluna] = linha.locator("td").nth(indice).inner_text().strip()
            dados_extraidos.append(item)
            
            if len(dados_extraidos) >= limite_registros:
                print(f"    - Limite de {limite_registros} registros atingido. Encerrando extração.")
                return dados_extraidos

        print(f"    - {len(dados_extraidos)} de {limite_registros} registros extraídos.")

        paginador = tabela.locator("tfoot")
        if paginador.count() == 0:
            print("\n--- Fim da extração. Nenhuma paginação encontrada. ---")
            break

        botao_proxima = paginador.locator('td.rich-datascr-button[onclick*="fastforward"]')
        
        if not botao_proxima.is_visible() or "dsbld" in (botao_proxima.get_attribute("class") or ""):
            print("\n--- Fim da paginação. Última página alcançada. ---")
            break
        
        print("\n    - Clicando em 'Próxima Página'...")
        botao_proxima.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        pagina_atual += 1
    
    return dados_extraidos

# --- MÓDULO DE PESQUISA (DENTRO DO MAIN) ---

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
    """Navega diretamente para a URL de consulta de cada NPJ da lista."""
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

            # Espera a página de resultados carregar
            page.wait_for_load_state("networkidle", timeout=30000)
            print("    - Página de resultados do processo carregada com sucesso.")
            
            time.sleep(3) # Pausa para observar o resultado

        except Exception as e:
            print(f"    - ERRO ao pesquisar o NPJ {npj}: {e}")
            continue

# --- FUNÇÃO PRINCIPAL ---

def main():
    browser_process = None
    with sync_playwright() as playwright:
        try:
            browser, context, browser_process = realizar_login_automatico(playwright)
            page = context.new_page()
            page.goto("https://juridico.bb.com.br/paj/juridico")
            page.locator("#aPaginaInicial").wait_for(state="visible", timeout=30000)
            print("✅ Verificação de login OK.")
            
            url_central_notificacoes = "https://juridico.bb.com.br/paj/app/paj-central-notificacoes/spas/central-notificacoes/central-notificacoes.app.html"
            page.goto(url_central_notificacoes)
            page.wait_for_load_state("networkidle", timeout=60000)
            print("✅ Central de Notificações carregada.")
            
            terceiro_card = page.locator("div.box-body").locator("div.pendencias-card").nth(2)
            botao_detalhes_card = terceiro_card.locator("a.mi--forward")
            botao_detalhes_card.click()
            page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ Página de detalhes (lista de notificações) carregada com sucesso.")
            
            url_lista_tarefas = page.url
            print(f"✅ URL da lista de tarefas capturada: {url_lista_tarefas}")
            
            TAREFAS = [
                {
                    "nome": "Inclusão de Documentos no NPJ",
                    "id_tabela": "notificacoesNaoLidasForm:notificacoesNaoLidasDetalhamentoForm:dataTabletableNotificacoesNaoLidas",
                    "colunas": ["NPJ", "Adverso Principal", "Número de rastreamento", "Origem"],
                    "funcao_salvar": salvar_dados_inclusao_docs,
                    "tipo_contagem": "notificacao"
                },
                # ... outras tarefas podem ser adicionadas aqui ...
            ]

            for tarefa in TAREFAS:
                print(f"\n{'='*20}\nPROCESSANDO TAREFA: {tarefa['nome']}\n{'='*20}")
                
                linha_alvo = page.locator(f"tr:has-text('{tarefa['nome']}')")
                
                if linha_alvo.count() > 0:
                    coluna_idx = 2 if tarefa['tipo_contagem'] == 'notificacao' else 3
                    contagem_texto = linha_alvo.locator("td").nth(coluna_idx).inner_text().strip()
                    
                    try:
                        contagem_numero = int(contagem_texto)
                    except ValueError:
                        contagem_numero = 0

                    if contagem_numero > 0:
                        print(f"    - {contagem_numero} itens encontrados. Detalhando...")
                        botao_detalhar = linha_alvo.get_by_title("Detalhar notificações e pendências do subtipo")
                        botao_detalhar.click()
                        page.wait_for_load_state("networkidle", timeout=30000)

                        dados_da_tarefa = extrair_dados_com_paginacao(page, tarefa["id_tabela"], tarefa["colunas"], limite_registros=contagem_numero)
                        
                        if dados_da_tarefa:
                            tarefa["funcao_salvar"](dados_da_tarefa)
                        
                        print("\n    - Retornando para a lista de notificações...")
                        page.goto(url_lista_tarefas)
                        page.wait_for_load_state("networkidle", timeout=30000)
                    else:
                        print(f"    - Nenhum item para processar. Pulando.")
                else:
                    print(f"    - Tipo de notificação não encontrado. Pulando.")
            
            # ETAPA 6: CHAMAR O MÓDULO DE PESQUISA
            print("\n✅ Extrações finalizadas. Iniciando módulo de pesquisa de NPJs.")
            
            npjs_para_pesquisar = ler_npjs_para_pesquisa()
            if npjs_para_pesquisar:
                # Passamos a 'page' já logada para a função de pesquisa
                # Para testar, pesquisamos apenas o primeiro NPJ da lista
                pesquisar_processos_v2(page, [npjs_para_pesquisar[0]])
            else:
                print("    - Nenhum NPJ encontrado para pesquisar.")

        except Exception as e:
            print(f"\nOcorreu uma falha na automação: {e}")
        finally:
            if browser_process:
                input("\n... Pressione Enter para fechar o navegador e encerrar a RPA ...")
                subprocess.run(f"TASKKILL /F /PID {browser_process.pid} /T", shell=True, capture_output=True)
                print("🏁 Navegador fechado. Fim da execução.")

if __name__ == "__main__":
    main()
