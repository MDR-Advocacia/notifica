# arquivo: processamento_detalhado.py
from playwright.sync_api import Page, TimeoutError
from datetime import datetime, timedelta
from pathlib import Path
import database
import re

def extrair_andamentos_na_janela(page: Page, datas_alvo: set[str]) -> list[dict]:
    """
    Na seção 'Andamentos', varre a tabela, captura qualquer andamento
    dentro da janela de datas e extrai o texto detalhado se for uma publicação.
    """
    andamentos_encontrados = []
    try:
        page.locator("li:has-text('Andamentos')").click()
        page.wait_for_load_state("networkidle", timeout=20000)
        print("    - Seção 'Andamentos' carregada.")

        page.locator('table[bb-expandable-table]').first.wait_for(state="visible", timeout=15000)
        linhas = page.locator('tr[ng-repeat-start="item in grupoMes.itens"]').all()
        print(f"    - Verificando {len(linhas)} andamentos na tela...")

        for linha in linhas:
            try:
                data_encontrada = linha.locator("td").nth(4).inner_text().strip()
                if data_encontrada not in datas_alvo:
                    continue

                tipo_andamento = linha.locator("td").nth(1).inner_text().strip()
                print(f"    - Encontrado andamento na data alvo: {data_encontrada} | Tipo: {tipo_andamento}")

                andamento_info = {"data": data_encontrada, "tipo": tipo_andamento, "texto": None}

                if "PUBLICACAO DJ/DO" in tipo_andamento.upper():
                    botao_detalhar = linha.locator('a[bb-tooltip="Detalhar publicação"]')
                    if botao_detalhar.count() > 0:
                        print("      - Botão 'Detalhar publicação' encontrado. Abrindo modal...")
                        botao_detalhar.click()
                        
                        modal = page.locator("div.modal__content")
                        modal.wait_for(state="visible", timeout=10000)
                        
                        # --- LÓGICA CORRIGIDA E RESTAURADA ---
                        try:
                            componente_texto = modal.locator("texto-grande-detalhar")
                            leia_mais_botao = componente_texto.get_by_role("button", name="Leia mais")
                            
                            # Espera o botão "Leia mais" estar visível antes de clicar
                            leia_mais_botao.wait_for(state="visible", timeout=3000)
                            leia_mais_botao.click()
                            
                            # Aguarda o botão "Leia menos" aparecer como confirmação da expansão
                            modal.get_by_role("button", name="Leia menos").wait_for(state="visible", timeout=5000)
                            print("      - Texto expandido com sucesso ('Leia menos' visível).")

                        except TimeoutError:
                            print("      - Botão 'Leia mais' não encontrado ou não foi necessário (texto já completo).")

                        # Após garantir a expansão, captura o texto do parágrafo
                        texto_completo = modal.locator("texto-grande-detalhar p[align='justify']").inner_text()
                        andamento_info["texto"] = texto_completo.strip() if texto_completo else "Texto não extraído."
                        print("      - ✅ Texto completo capturado do modal.")
                        
                        modal.locator("div.modal__close").click()
                        modal.wait_for(state="hidden", timeout=5000)
                else:
                    # Se for outro tipo de andamento, pega a descrição curta
                    try:
                        trigger_id = linha.get_attribute("bb-expandable-trigger")
                        if trigger_id:
                            clean_id = trigger_id.lstrip('#')
                            linha_expansivel = page.locator(f"tr#{clean_id}")
                            descricao_curta = linha_expansivel.locator("div.col-xs-24.ta-left > span.ng-binding").first.inner_text()
                            andamento_info["texto"] = descricao_curta.strip()
                    except Exception:
                        pass # Não há descrição curta, só o título já basta

                andamentos_encontrados.append(andamento_info)
            except Exception as e_linha:
                print(f"      - ⚠️ Erro ao processar uma linha de andamento: {e_linha}")
                continue

    except Exception as e:
        print(f"    - ⚠️ Aviso geral durante a extração de andamentos: {e}")
    
    return andamentos_encontrados

def baixar_documentos_na_janela(page: Page, npj: str, datas_alvo: set[str]) -> list[dict]:
    # (O código desta função permanece o mesmo)
    # ...
    documentos_baixados = []
    try:
        acordeao_documentos = page.locator('div.accordion__item[bb-item-title="Documentos"]')
        if "is-open" not in (acordeao_documentos.get_attribute("class") or ""):
            print("    - Expandindo a seção 'Documentos'...")
            acordeao_documentos.locator(".accordion__title").click()
            page.wait_for_load_state("networkidle", timeout=20000)
        else:
            print("    - Seção 'Documentos' já está expandida.")

        pasta_base = Path("downloads")
        pasta_npj_sanitizada = npj.replace("/", "_").replace("-", "_")
        caminho_completo_npj = pasta_base / pasta_npj_sanitizada
        caminho_completo_npj.mkdir(parents=True, exist_ok=True)
        
        tabela_documentos = page.locator('table[ng-table="vm.tabelaDocumento"]')
        tabela_documentos.locator("tbody tr").first.wait_for(state="visible", timeout=15000)
        
        linhas = tabela_documentos.locator("tbody tr").all()
        print(f"    - Verificando {len(linhas)} documentos na tabela...")

        for linha in linhas:
            celulas = linha.locator("td").all()
            if len(celulas) < 5: continue
            
            data_documento = celulas[-2].inner_text().strip()

            if data_documento in datas_alvo:
                link_download = linha.locator("a[href*='/download/']")
                if link_download.count() > 0:
                    nome_arquivo = link_download.inner_text().strip()
                    print(f"      - Encontrado documento na data alvo: {data_documento} | Arquivo: {nome_arquivo}")

                    try:
                        with page.expect_download(timeout=60000) as download_info:
                            link_download.click()
                        download = download_info.value
                        
                        caminho_salvar = caminho_completo_npj / download.suggested_filename
                        download.save_as(caminho_salvar)
                        
                        caminho_relativo = f"{pasta_npj_sanitizada}/{download.suggested_filename}"
                        documentos_baixados.append({
                            "data": data_documento,
                            "nome_arquivo": download.suggested_filename,
                            "caminho_relativo": caminho_relativo
                        })
                        print(f"      - ✅ Download concluído: {caminho_salvar}")
                    except Exception as e_download:
                        print(f"      - ❌ ERRO ao tentar baixar o arquivo '{nome_arquivo}': {e_download}")

    except Exception as e:
        print(f"    - ⚠️ Aviso durante o processo de download de documentos: {e}")
        
    return documentos_baixados

def processar_detalhes_pendentes(page: Page):
    """
    Processa NPJs e retorna um dicionário com as estatísticas da execução.
    """
    print("\n" + "="*20)
    print("INICIANDO MÓDULO DE PROCESSAMENTO DETALHADO")
    print("="*20)

    stats = {"sucesso": 0, "falha": 0, "andamentos": 0, "documentos": 0}
    npjs_para_processar = database.obter_npjs_pendentes()
    is_test_mode = False

    if not npjs_para_processar:
        is_test_mode = True
        npjs_para_processar = database.obter_npjs_para_teste(limite=5)

    if not npjs_para_processar:
        print("Nenhum item pendente ou de teste para processar.")
        return stats

    url_base = "https://juridico.bb.com.br/paj/app/paj-cadastro/spas/processo/consulta/processo-consulta.app.html#/editar/"

    for item in npjs_para_processar:
        npj = item['NPJ']
        datas_notificacao_str = item['datas_notificacao']
        print(f"\n--- Processando NPJ: {npj} {'(MODO DE TESTE)' if is_test_mode else ''} ---")
        
        try:
            datas_alvo = set()
            for data_str in datas_notificacao_str.split(','):
                data_base = datetime.strptime(data_str, '%d/%m/%Y')
                for i in range(3): # D, D-1, D-2
                    datas_alvo.add((data_base - timedelta(days=i)).strftime('%d/%m/%Y'))
            
            print(f"    - Janela de datas para busca: {sorted(list(datas_alvo))}")

            ano, resto = npj.split('/')
            numero, variacao_str = resto.split('-')
            url_final = f"{url_base}{ano + numero}/{int(variacao_str)}/1"
            
            page.goto(url_final)
            page.locator("i.ci.ci--barcode").first.wait_for(state="visible", timeout=15000)
            print("    - Página de detalhes do NPJ carregada.")

            andamentos_coletados = extrair_andamentos_na_janela(page, datas_alvo)
            stats["andamentos"] += len(andamentos_coletados)

            print("    - Navegando para 'Dados do Processo'...")
            page.get_by_text("Dados do Processo", exact=True).click()
            page.wait_for_load_state("networkidle", timeout=20000)

            documentos_coletados = baixar_documentos_na_janela(page, npj, datas_alvo)
            stats["documentos"] += len(documentos_coletados)

            database.atualizar_registro_processado(npj, andamentos_coletados, documentos_coletados, is_test=is_test_mode)
            stats["sucesso"] += 1

        except Exception as e:
            print(f"    - ❌ ERRO GERAL no processamento do NPJ {npj}: {e}")
            page.screenshot(path=f"erro_processo_detalhado_{npj.replace('/', '-')}.png")
            if not is_test_mode:
                database.marcar_como_erro(npj)
            stats["falha"] += 1
            continue
    
    return stats

