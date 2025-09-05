import time
import random # Importamos a biblioteca 'random' para pausas aleatórias
from playwright.sync_api import sync_playwright
import os

def executar_rpa_ninja(playwright):
    user_data_dir = os.path.join(os.getcwd(), 'chrome_user_data')
    
    # Carregar o conteúdo do nosso script de camuflagem
    with open('stealth.min.js', 'r') as f:
        stealth_script = f.read()

    context = playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        slow_mo=25, # Reduzimos um pouco o slow_mo geral
        channel="chrome",
        viewport={'width': 1920, 'height': 1080}
    )
    
    page = context.new_page()
    
    # --- MUDANÇA 1: INJETANDO O SCRIPT DE CAMUFLAGEM ---
    # Usamos page.add_init_script() para executar nosso script ANTES de qualquer
    # outro script na página do Google. Isso apaga nossos rastros.
    page.add_init_script(stealth_script)
    
    try:
        print(">>> Acessando https://www.google.com... (modo ninja)")
        page.goto("https://www.google.com/")
        
        # Pausa para simular tempo de leitura/decisão
        time.sleep(random.uniform(1.5, 2.5))

        print(">>> Localizando a barra de pesquisa...")
        barra_de_pesquisa = page.get_by_title("Pesquisar")
        
        # --- MUDANÇA 2: SIMULANDO COMPORTAMENTO HUMANO ---
        print(">>> Movendo o mouse para a barra de pesquisa...")
        # 1. Mover o mouse sobre o elemento antes de interagir
        barra_de_pesquisa.hover()
        
        # 2. Clicar explicitamente para ganhar foco
        barra_de_pesquisa.click()

        termo_pesquisado = "agora sim, não tem como saber"
        print(f">>> Digitando '{termo_pesquisado}' de forma natural...")
        barra_de_pesquisa.type(termo_pesquisado, delay=random.randint(80, 150)) # Delay aleatório
        
        # Pausa antes de pressionar Enter
        time.sleep(random.uniform(0.5, 1.0))

        print(">>> Pressionando a tecla Enter...")
        barra_de_pesquisa.press("Enter")
        
        print(">>> Aguardando a página de resultados carregar...")
        page.wait_for_selector(f"h3:has-text('{termo_pesquisado.split()[0]}')")
        
        print(">>> Pesquisa realizada com sucesso no modo ninja!")
        
        caminho_screenshot = "evidencia_pesquisa_ninja.png"
        page.screenshot(path=caminho_screenshot)
        print(f">>> Screenshot salvo em: '{caminho_screenshot}'")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    finally:
        print(">>> Automação finalizada. O navegador fechará em 5 segundos.")
        time.sleep(5)
        context.close()

# --- Bloco de execução ---
with sync_playwright() as playwright:
    executar_rpa_ninja(playwright)