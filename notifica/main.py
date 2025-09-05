# arquivo: main.py
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
from autologin import realizar_login_automatico
import database
import extracao_notificacoes
import processamento_detalhado

def formatar_duracao(segundos):
    """Formata segundos em uma string legível (minutos e segundos)."""
    if segundos < 0: return "0 segundos"
    if segundos < 60:
        return f"{segundos:.2f} segundos"
    minutos, seg = divmod(segundos, 60)
    return f"{int(minutos)} minuto(s) e {int(seg)} segundo(s)"

def main():
    database.inicializar_banco()
    start_time = time.time()
    
    stats_extracao = {"notificacoes": 0}
    stats_processamento = {"sucesso": 0, "falha": 0, "andamentos": 0, "documentos": 0}

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
            terceiro_card.locator("a.mi--forward").click()
            page.wait_for_load_state("networkidle", timeout=30000)
            url_lista_tarefas = page.url
            print(f"✅ URL da lista de tarefas capturada: {url_lista_tarefas}")

            stats_extracao["notificacoes"] = extracao_notificacoes.extrair_novas_notificacoes(page, url_lista_tarefas)
            stats_processamento = processamento_detalhado.processar_detalhes_pendentes(page)

        except Exception as e:
            print(f"\n❌ Ocorreu uma falha crítica na automação: {e}")
            stats_processamento["falha"] = "Crítico"
        finally:
            end_time = time.time()
            duracao_total = end_time - start_time
            
            # --- Monta o dicionário de log ---
            total_npjs_processados = stats_processamento.get("sucesso", 0) + (1 if stats_processamento.get("falha") == "Crítico" else stats_processamento.get("falha", 0))
            tempo_medio = duracao_total / total_npjs_processados if total_npjs_processados > 0 else 0

            log_data = {
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "duracao_total": formatar_duracao(duracao_total),
                "tempo_medio_npj": formatar_duracao(tempo_medio),
                "notificacoes_salvas": stats_extracao.get("notificacoes", 0),
                "andamentos_capturados": stats_processamento.get("andamentos", 0),
                "documentos_baixados": stats_processamento.get("documentos", 0),
                "npjs_sucesso": stats_processamento.get("sucesso", 0),
                "npjs_falha": stats_processamento.get("falha", 0)
            }
            
            # Salva o log no banco de dados
            database.salvar_log_execucao(log_data)

            # --- Imprime o resumo no terminal ---
            resumo = f"""
============================================================
📊 RESUMO DA EXECUÇÃO DA RPA ({log_data['timestamp']})
============================================================
- Tempo Total de Execução: {log_data['duracao_total']}
- Média por NPJ Processado: {log_data['tempo_medio_npj']}

- Notificações Novas Salvas: {log_data['notificacoes_salvas']}
- Andamentos Capturados: {log_data['andamentos_capturados']}
- Documentos Baixados: {log_data['documentos_baixados']}

- Processos com Sucesso: {log_data['npjs_sucesso']}
- Processos com Falha: {log_data['npjs_falha']}
============================================================
"""
            print(resumo)

            if 'browser' in locals() and browser.is_connected():
                input("\n... Pressione Enter para fechar o navegador e encerrar a RPA ...")
                browser.close()
            elif browser_process:
                browser_process.kill()

if __name__ == "__main__":
    main()

