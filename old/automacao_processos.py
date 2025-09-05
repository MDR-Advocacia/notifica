# arquivo: automacao_processos.py
from playwright.sync_api import Page

# A função 'ler_npjs_para_pesquisa' foi removida, pois não é mais necessária.

def clicar_no_menu_andamentos(page: Page) -> None:
    # (Esta função permanece inalterada)
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

def navegar_para_detalhes_do_processo(page: Page, lista_de_npjs: list[str]) -> None:
    # (Esta função permanece inalterada)
    print("\nIniciando módulo de navegação e interação com detalhes do processo...")
    url_base = "https://juridico.bb.com.br/paj/app/paj-cadastro/spas/processo/consulta/processo-consulta.app.html#/editar/"
    for npj in lista_de_npjs:
        try:
            print(f"    - Processando NPJ: {npj}")
            ano, resto = npj.split('/')
            numero, variacao_str = resto.split('-')
            parte_npj_principal = ano + numero
            parte_variacao = int(variacao_str)
            url_final = f"{url_base}{parte_npj_principal}/{parte_variacao}/1"
            print(f"    - Navegando para URL de detalhes: {url_final}")
            page.goto(url_final)
            page.wait_for_load_state("networkidle", timeout=30000)
            print("    - Verificando se a página de detalhes carregou (aguardando o primeiro ícone de barras)...")
            primeiro_icone_confirmacao = page.locator("i.ci.ci--barcode").first
            primeiro_icone_confirmacao.wait_for(state="visible", timeout=15000)
            print("    - ✅ Página de detalhes carregada com sucesso!")
            clicar_no_menu_andamentos(page)
        except Exception as e:
            print(f"    - ❌ ERRO no processamento do NPJ {npj}: {e}")
            screenshot_path = f"erro_processo_{npj.replace('/', '-')}.png"
            page.screenshot(path=screenshot_path)
            print(f"    - Screenshot salvo em: {screenshot_path}")
            continue

# --- ATUALIZADO: A função agora recebe a lista de NPJs diretamente ---
def iniciar_processamento_de_npjs(page: Page, lista_de_npjs: list[str]) -> None:
    """
    Função principal que orquestra a navegação dos processos a partir de uma lista recebida.
    """
    print("\n✅ Extrações finalizadas. Iniciando navegação para os detalhes dos NPJs.")
    
    if lista_de_npjs:
        print(f"    - {len(lista_de_npjs)} NPJ(s) foram coletados para processamento.")
        navegar_para_detalhes_do_processo(page, lista_de_npjs)
    else:
        print("    - Nenhum NPJ da tarefa 'Inclusão de Documentos' foi encontrado para processar.")