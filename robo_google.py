# --- Passo 1: Importar as bibliotecas necessárias ---

# 'time' nos permite adicionar pausas no código.
import time
# 'sync_playwright' é o coração do Playwright, que nos dá acesso às suas funcionalidades.
from playwright.sync_api import sync_playwright

# --- Passo 2: Definir a função principal do nosso robô ---

def executar_rpa(playwright):
    """
    Esta função contém toda a lógica da nossa automação.
    """
    
    # --- Configuração do Navegador ---
    
    # Lança uma instância de um navegador. Por padrão, usamos o Chromium.
    # headless=False: Significa que queremos VER a janela do navegador abrindo e as ações acontecendo.
    # slow_mo=50: Adiciona uma pequena pausa de 50 milissegundos entre cada ação do Playwright,
    #             facilitando a visualização do que o robô está fazendo.
    # DICA: Para usar seu Google Chrome, adicione o argumento: channel="chrome"
    browser = playwright.chromium.launch(headless=False, slow_mo=50)
    
    # Cria uma nova página (uma nova aba) no navegador que acabamos de abrir.
    page = browser.new_page()
    
    # --- Lógica da Automação ---
    
    try:
        # Navega para o site do Google.
        print(">>> Acessando https://www.google.com...")
        page.goto("https://www.google.com/")
        
        # O Playwright pode precisar lidar com pop-ups de consentimento de cookies.
        # Esta linha localiza um botão com o texto "Aceitar tudo" e clica nele, se ele existir.
        # O 'timeout=5000' (5s) faz com que ele não espere muito se o botão não aparecer.
        try:
            page.get_by_role("button", name="Aceitar tudo").click(timeout=5000)
            print(">>> Pop-up de cookies aceito.")
        except Exception as e:
            print(">>> Pop-up de cookies não encontrado, continuando...")

        # Encontra a barra de pesquisa. A melhor forma de fazer isso no Google é
        # buscando por um elemento que tenha o atributo 'title' igual a "Pesquisar".
        # Isso é mais resistente a mudanças do que usar nomes de classes CSS.
        print(">>> Localizando a barra de pesquisa...")
        barra_de_pesquisa = page.get_by_title("Pesquisar")
        
        # Digita o texto "funcionou" na barra de pesquisa que encontramos.
        termo_pesquisado = "funcionou"
        print(f">>> Digitando '{termo_pesquisado}'...")
        barra_de_pesquisa.fill(termo_pesquisado)
        
        # Pressiona a tecla "Enter" no teclado para submeter a pesquisa.
        print(">>> Pressionando a tecla Enter...")
        barra_de_pesquisa.press("Enter")
        
        # Boa prática: Esperar por um elemento da página de resultados para garantir que ela carregou.
        # Aqui, esperamos por um cabeçalho 'h3' que contenha o texto que pesquisamos.
        print(">>> Aguardando a página de resultados carregar...")
        page.wait_for_selector(f"h3:has-text('{termo_pesquisado}')")
        
        print(">>> Pesquisa realizada com sucesso!")
        
        # Tira uma "evidência" do sucesso, salvando uma imagem da tela.
        caminho_screenshot = "evidencia_pesquisa_google.png"
        page.screenshot(path=caminho_screenshot)
        print(f">>> Screenshot salvo em: '{caminho_screenshot}'")

    except Exception as e:
        # Se qualquer erro ocorrer durante a automação, ele será capturado aqui.
        print(f"Ocorreu um erro inesperado: {e}")

    finally:
        # --- Finalização ---
        
        # Adiciona uma pausa de 5 segundos para que possamos ver o resultado final.
        print(">>> Automação finalizada. O navegador fechará em 5 segundos.")
        time.sleep(5)
        
        # Fecha o navegador. É muito importante sempre fechar o navegador no final
        # para não deixar processos "zumbis" rodando.
        browser.close()


# --- Passo 3: Bloco de execução ---

# Este é o ponto de entrada padrão para um script Playwright.
# Ele inicializa o Playwright, chama nossa função principal e garante que tudo seja fechado corretamente.
with sync_playwright() as playwright:
    executar_rpa(playwright)