# arquivo: main_extracao.py
import sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright, Page
from autologin import realizar_login_automatico

# IMPORTA AS FUNÇÕES DOS NOSSOS MÓDULOS
from automacao_documentos import iniciar_processamento_de_documentos
from automacao_andamentos import iniciar_processamento_de_andamentos

# --- FUNÇÕES DE BANCO DE DADOS E EXTRAÇÃO ---
def salvar_dados_generico(dados: list[dict], nome_banco: str, nome_tabela: str, schema_tabela: str, mapeamento_colunas: dict):
    """Salva uma lista de dicionários de dados em uma tabela SQLite de forma genérica."""
    if not dados:
        print(f"    - Nenhum dado novo para salvar na tabela '{nome_tabela}'.")
        return
    conn = None
    try:
        conn = sqlite3.connect(nome_banco)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({schema_tabela})")
        colunas_db = ', '.join(mapeamento_colunas.keys())
        placeholders = ', '.join(['?'] * len(mapeamento_colunas))
        query = f"INSERT OR IGNORE INTO {nome_tabela} ({colunas_db}) VALUES ({placeholders})"
        registros_a_inserir = [tuple(item.get(key_json) for key_json in mapeamento_colunas.values()) for item in dados]
        cursor.executemany(query, registros_a_inserir)
        registros_inseridos = cursor.rowcount
        conn.commit()
        print(f"\n✅ {registros_inseridos} novos registros salvos em '{nome_banco}' na tabela '{nome_tabela}'.")
    except sqlite3.Error as e:
        print(f"\n❌ ERRO ao salvar dados no banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def extrair_dados_com_paginacao(page: Page, id_tabela: str, colunas_desejadas: list[str], limite_registros: int) -> list[dict]:
    """Extrai dados de uma tabela com paginação."""
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
            if len(dados_extraidos) >= limite_registros:
                print(f"    - Limite de {limite_registros} registros atingido. Encerrando extração.")
                return dados_extraidos
            item = {}
            for nome_coluna, indice in indices_colunas.items():
                item[nome_coluna] = linha.locator("td").nth(indice).inner_text().strip()
            dados_extraidos.append(item)
        print(f"    - {len(dados_extraidos)} de {limite_registros} registros extraídos.")
        paginador = tabela.locator("tfoot")
        if paginador.count() == 0:
            break
        botao_proxima = paginador.locator('td.rich-datascr-button[onclick*="fastforward"]')
        if botao_proxima.count() == 0:
            break
        classe_do_botao = botao_proxima.get_attribute("class") or ""
        if "dsbld" in classe_do_botao:
            break
        print("\n    - Clicando em 'Próxima Página'...")
        botao_proxima.click()
        page.wait_for_load_state("networkidle", timeout=30000)
        pagina_atual += 1
    return dados_extraidos

# --- FUNÇÃO PRINCIPAL ---
def main():
    browser = None
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
                    "nome_banco": "dados_inclusao_docs.db",
                    "id_tabela": "notificacoesNaoLidasForm:notificacoesNaoLidasDetalhamentoForm:dataTabletableNotificacoesNaoLidas",
                    "colunas_extracao": ["NPJ", "Adverso Principal", "Número de rastreamento", "Origem", "Qtd Dias Gerada"],
                    "tipo_contagem": "notificacao",
                    "db_config": {
                        "nome_tabela": "inclusao_documentos",
                        "schema_tabela": "NPJ TEXT PRIMARY KEY, Adverso_Principal TEXT, Numero_de_rastreamento TEXT, Origem TEXT, Qtd_Dias_Gerada TEXT",
                        "mapeamento_colunas": { "NPJ": "NPJ", "Adverso_Principal": "Adverso Principal", "Numero_de_rastreamento": "Número de rastreamento", "Origem": "Origem", "Qtd_Dias_Gerada": "Qtd Dias Gerada" }
                    }
                },
                {
                    "nome": "Doc. anexado por empresa externa em processo terceirizado",
                    "nome_banco": "dados_doc_externo.db",
                    "id_tabela": "notificacoesNaoLidasForm:notificacoesNaoLidasDetalhamentoForm:dataTabletableNotificacoesNaoLidas",
                    "colunas_extracao": ["NPJ", "Adverso Principal", "Gerada em"],
                    "tipo_contagem": "notificacao",
                    "db_config": {
                        "nome_tabela": "doc_externo",
                        "schema_tabela": "NPJ TEXT PRIMARY KEY, Adverso_Principal TEXT, Gerado_em TEXT",
                        "mapeamento_colunas": { "NPJ": "NPJ", "Adverso_Principal": "Adverso Principal", "Gerado_em": "Gerada em" }
                    }
                },
                {
                    "nome": "Andamento de publicação em processo de condução terceirizada",
                    "nome_banco": "dados_andamento_publicacao.db",
                    "id_tabela": "notificacoesNaoLidasForm:notificacoesNaoLidasDetalhamentoForm:dataTabletableNotificacoesNaoLidas",
                    "colunas_extracao": ["NPJ", "Adverso Principal", "Gerada em"],
                    "tipo_contagem": "notificacao",
                    "db_config": {
                        "nome_tabela": "andamento_publicacao",
                        "schema_tabela": "NPJ TEXT PRIMARY KEY, Adverso_Principal TEXT, Gerado_em TEXT",
                        "mapeamento_colunas": { "NPJ": "NPJ", "Adverso_Principal": "Adverso Principal", "Gerado_em": "Gerada em" }
                    }
                },
            ]
            
            andamentos_coletados_para_processamento = []

            for tarefa in TAREFAS:
                try:
                    print(f"\n{'='*20}\nPROCESSANDO TAREFA: {tarefa['nome']}\n{'='*20}")
                    linha_alvo = page.locator(f"tr:has-text('{tarefa['nome']}')")
                    
                    if linha_alvo.count() > 0:
                        coluna_idx = 2 if tarefa['tipo_contagem'] == 'notificacao' else 3
                        contagem_texto = linha_alvo.locator("td").nth(coluna_idx).inner_text().strip()
                        try:
                            contagem_numero = int(contagem_texto)
                        except (ValueError, TypeError):
                            contagem_numero = 0
                        
                        print(f"    - Quantidade de itens encontrados: {contagem_numero}")
                        
                        if contagem_numero > 0:
                            botao_detalhar = linha_alvo.get_by_title("Detalhar notificações e pendências do subtipo")
                            botao_detalhar.click()
                            page.wait_for_load_state("networkidle", timeout=30000)
                            dados_da_tarefa = extrair_dados_com_paginacao(page, tarefa["id_tabela"], tarefa["colunas_extracao"], limite_registros=contagem_numero)
                            
                            if dados_da_tarefa:
                                db_cfg = tarefa['db_config']
                                salvar_dados_generico(dados=dados_da_tarefa, nome_banco=tarefa['nome_banco'], nome_tabela=db_cfg['nome_tabela'], schema_tabela=db_cfg['schema_tabela'], mapeamento_colunas=db_cfg['mapeamento_colunas'])

                                if tarefa['nome'] == "Andamento de publicação em processo de condução terceirizada":
                                    print(f"    - Coletando {len(dados_da_tarefa)} Andamento(s) para processamento detalhado...")
                                    andamentos_coletados_para_processamento.extend(dados_da_tarefa)
                            
                            page.goto(url_lista_tarefas)
                            page.wait_for_load_state("networkidle", timeout=30000)
                    else:
                        print(f"    - Tarefa '{tarefa['nome']}' não encontrada na página. Pulando.")

                except Exception as e_tarefa:
                    print(f"    - ❌ Ocorreu um erro ao processar a tarefa '{tarefa['nome']}': {e_tarefa}")
                    print("    - Tentando retornar à lista de tarefas para continuar com a próxima...")
                    try:
                        page.goto(url_lista_tarefas)
                        page.wait_for_load_state("networkidle", timeout=30000)
                    except Exception as e_nav:
                        print(f"    - ❌ Falha crítica ao tentar retornar à lista de tarefas: {e_nav}. Encerrando a extração.")
                        break

            # --- ATUALIZAÇÃO: ORDEM DE EXECUÇÃO INVERTIDA ---
            
            # 1. Executa a automação para Andamentos de Publicação (usa a lista coletada)
            iniciar_processamento_de_andamentos(page, andamentos_coletados_para_processamento)

            # 2. Executa a automação para Inclusão de Documentos (lê do seu próprio DB)
            iniciar_processamento_de_documentos(page)


        except Exception as e:
            print(f"\nOcorreu uma falha na automação: {e}")
        finally:
            if 'browser' in locals() and browser.is_connected():
                input("\n... Pressione Enter para fechar o navegador e encerrar a RPA ...")
                print("🏁 Fechando o navegador...")
                browser.close()
                print("🏁 Navegador fechado. Fim da execução.")
            elif browser_process:
                browser_process.kill()

if __name__ == "__main__":
    main()