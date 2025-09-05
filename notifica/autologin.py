# arquivo: autologin.py
import time
import subprocess
from pathlib import Path
# Removido o import do sync_playwright daqui, pois não é mais necessário

# --- CONFIGURAÇÕES DO MÓDULO ---
BAT_FILE_PATH = Path(__file__).resolve().parent / "abrir_chrome.bat"
CDP_ENDPOINT = "http://localhost:9222"
EXTENSION_URL = "chrome-extension://lnidijeaekolpfeckelhkomndglcglhh/index.html"

# A FUNÇÃO AGORA RECEBE O OBJETO 'playwright' COMO PARÂMETRO
def realizar_login_automatico(playwright):
    """
    Executa o .bat, conecta-se ao Chrome e realiza o login automático via extensão.
    Recebe a instância do Playwright como argumento.
    """
    print("--- MÓDULO DE LOGIN AUTOMÁTICO ---")
    
    print(f"▶️  Executando o script: {BAT_FILE_PATH}")
    browser_process = subprocess.Popen(
        str(BAT_FILE_PATH), 
        shell=True, 
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )
    
    # NÃO HÁ MAIS 'with sync_playwright() ...' AQUI
    
    browser = None
    for attempt in range(15):
        time.sleep(2)
        print(f"    Tentativa de conexão nº {attempt + 1}...")
        try:
            # Usamos a instância 'playwright' que recebemos
            browser = playwright.chromium.connect_over_cdp(CDP_ENDPOINT)
            print("✅ Conectado com sucesso ao navegador!")
            break 
        except Exception:
            continue
    
    if not browser:
        raise ConnectionError("Não foi possível conectar ao navegador.")

    context = browser.contexts[0]
    
    print(f"🚀 Navegando para a URL da extensão...")
    extension_page = context.new_page()
    extension_page.goto(EXTENSION_URL)
    extension_page.wait_for_load_state("domcontentloaded")

    search_input = extension_page.get_by_placeholder("Digite ou selecione um sistema pra acessar")
    search_input.wait_for(state="visible", timeout=5000)
    search_input.fill("banco do")

    login_button = extension_page.locator(
        'div[role="menuitem"]:not([disabled])', 
        has_text="Banco do Brasil - Intranet"
    ).first
    login_button.click(timeout=10000)

    extension_page.get_by_role("button", name="ACESSAR").click(timeout=5000)
    
    print("✔️  Login via extensão confirmado!")
    time.sleep(5)
    extension_page.close()
    
    print("--- FIM DO MÓDULO DE LOGIN ---")
    return browser, context, browser_process

# O bloco if __name__ == "__main__" precisa ser ajustado para criar sua própria instância
# apenas quando executado diretamente para teste.
if __name__ == "__main__":
    # Importamos aqui dentro para não afetar o escopo global
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as playwright:
            browser, context, browser_process = realizar_login_automatico(playwright)
            print("\nLogin realizado (teste de módulo). O navegador permanecerá aberto.")
            input("Pressione Enter para fechar...")
    finally:
        if 'browser_process' in locals() and browser_process:
            subprocess.run(f"TASKKILL /F /PID {browser_process.pid} /T", shell=True, capture_output=True)