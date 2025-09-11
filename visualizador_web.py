import sqlite3
import json
import os
import webbrowser
from threading import Timer
from flask import Flask, render_template_string, send_from_directory, request, redirect, url_for

# --- CONFIGURAÇÃO ---
ITENS_POR_PAGINA = 15
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'rpa.db')
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')
LOGO_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASIAAACuCAYAAAB8CV3AAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARTSURBVHhe7d3/S9t3fcfx9Z0aUhAFRRBFEAQV0V1RFF0UWVhcLItcFtdFtry2/gJbLHuLrbHWv6DD+gt0XRRdlF21KIti14WLolB0UVDU4eD/4PzT5A0kpLkk581534/n45LzfvD53u+53A/JvU/IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-!"

app = Flask(__name__)

# --- FUNÇÕES AUXILIARES ---
def formatar_duracao(segundos):
    """Formata segundos em uma string legível (minutos e segundos)."""
    try:
        # Garante que segundos seja um número
        segundos = float(segundos)
    except (ValueError, TypeError):
        return "0 segundos"

    if segundos < 0: return "0 segundos"
    if segundos < 60:
        return f"{segundos:.1f} segundos"
    minutos, seg = divmod(segundos, 60)
    return f"{int(minutos)} minuto(s) e {int(seg)} segundo(s)"

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria e atualiza as tabelas do banco de dados se necessário."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Cria a tabela de notificações se ela não existir.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notificacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        NPJ TEXT,
        tipo_notificacao TEXT,
        adverso_principal TEXT,
        data_notificacao TEXT,
        data_criacao TEXT,
        status TEXT DEFAULT 'Pendente',
        andamentos TEXT,
        documentos TEXT
    );
    """)

    # 2. LÓGICA DE MIGRAÇÃO: Verifica e adiciona a coluna 'data_criacao'
    cursor.execute("PRAGMA table_info(notificacoes)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'data_criacao' not in columns:
        print("INFO: Atualizando o esquema do banco de dados... Adicionando a coluna 'data_criacao'.")
        cursor.execute("ALTER TABLE notificacoes ADD COLUMN data_criacao TEXT")
        conn.commit()

    # 3. Cria a tabela de logs se ela não existir.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs_execucao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        duracao_total REAL,
        tempo_medio_npj REAL,
        notificacoes_salvas INTEGER,
        andamentos_capturados INTEGER,
        documentos_baixados INTEGER,
        npjs_sucesso INTEGER,
        npjs_falha INTEGER
    );
    """)
    
    conn.commit()
    conn.close()

def get_db_table_data(table_name):
    """Busca todos os dados de uma tabela específica."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} ORDER BY id DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"ERRO de banco de dados ao buscar dados da tabela {table_name}: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# --- TEMPLATE HTML EMBUTIDO ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OneNotify - Dashboard</title>
    <style>
        :root {
            --bg-color: #1a1a2e; --primary-color: #16213e; --secondary-color: #0f3460;
            --accent-color: #e94560; --text-color: #dcdcdc; --header-color: #ffffff;
            --border-color: #2a2a4a; --hover-color: #2d2d5a; --tab-inactive: #a0a0c0;
        }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: var(--bg-color); color: var(--text-color); margin: 0; padding: 2em; }
        .container { max-width: 1800px; margin: auto; background: var(--primary-color); padding: 2em; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
        .header { display: flex; align-items: center; justify-content: space-between; padding-bottom: 1.5em; }
        .logo-container { display: flex; align-items: center; gap: 15px; }
        .logo { height: 50px; }
        h1 { color: var(--header-color); font-size: 2.2em; margin: 0; font-weight: 600; }
        
        .tabs { border-bottom: 2px solid var(--border-color); margin-bottom: 1.5em; }
        .tab-button { background: none; border: none; padding: 15px 25px; font-size: 1.1em; cursor: pointer; transition: color 0.2s, border-bottom 0.2s; color: var(--tab-inactive); border-bottom: 3px solid transparent; }
        .tab-button.active { color: var(--accent-color); border-bottom-color: var(--accent-color); font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .filter-section, .log-section { background-color: var(--secondary-color); padding: 1.5em; border-radius: 8px; margin-bottom: 20px; }
        .filter-section { display: flex; gap: 20px; align-items: center; flex-wrap: wrap; }
        .filter-group label { margin-bottom: 8px; font-weight: 500; color: var(--text-color); }
        select { padding: 10px 15px; border: 1px solid var(--border-color); border-radius: 6px; background-color: var(--primary-color); color: var(--text-color); font-size: 1em; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9em; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid var(--border-color); word-break: break-word; vertical-align: middle; }
        th { background-color: var(--secondary-color); font-weight: 600; color: var(--header-color); }
        tr:hover { background-color: var(--hover-color); }
        
        .status { padding: 5px 10px; border-radius: 15px; color: #fff; font-weight: 500; text-align: center; display: inline-block; min-width: 80px; }
        .status-Pendente { background-color: #28a745; }
        .status-Processado, .status-Processado-em-Teste { background-color: #007bff; }
        .status-Arquivado { background-color: #6c757d; }
        .status-Erro { background-color: #dc3545; }
        
        .action-button { background: none; border: 1px solid #6c757d; color: #6c757d; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 0.9em; transition: all 0.2s; }
        .action-button:hover { background-color: #6c757d; color: #fff; }
        
        .pagination { margin-top: 20px; text-align: center; }
        .pagination a { color: var(--accent-color); padding: 8px 14px; text-decoration: none; border: 1px solid var(--border-color); margin: 0 4px; border-radius: 4px; transition: all 0.2s; }
        .pagination a.active, .pagination a:hover:not(.active) { background-color: var(--accent-color); color: white; border-color: var(--accent-color); }

        .log-section { margin-top: 30px; }
        h2 { color: var(--header-color); margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
        .log-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .info-item { background-color: var(--primary-color); padding: 15px; border-radius: 6px; }
        .info-item .label { display: block; font-size: 0.9em; color: var(--tab-inactive); margin-bottom: 5px; }
        .info-item .value { font-size: 1.2em; font-weight: 600; color: var(--header-color); }
        
        details summary { cursor: pointer; font-weight: 500; padding: 5px; border-radius: 4px; }
        details summary:hover { background-color: var(--hover-color); }
        .publication-text { white-space: pre-wrap; background-color: #111; padding: 10px; margin-top: 5px; border-radius: 4px; font-family: monospace; max-height: 250px; overflow-y: auto; }
        a { color: #8ab4f8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo-container">
                <img src="{{ logo }}" alt="Logo OneNotify" class="logo">
                <h1>OneNotify</h1>
            </div>
        </header>

        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'Dashboard')">Dashboard Principal</button>
            <button class="tab-button" onclick="openTab(event, 'Logs')">Histórico de Execuções</button>
        </div>

        <div id="Dashboard" class="tab-content active">
            <section class="filter-section">
                <!-- Filtros -->
                <form method="get" style="display: contents;">
                    <div class="filter-group">
                        <label for="status-filter">Status</label>
                        <select id="status-filter" name="status" onchange="this.form.submit()">
                            <option value="">Todos</option>
                            <option value="Pendente" {% if filtros.status == 'Pendente' %}selected{% endif %}>Novo</option>
                            <option value="Processado" {% if filtros.status == 'Processado' %}selected{% endif %}>Processado</option>
                            <option value="Arquivado" {% if filtros.status == 'Arquivado' %}selected{% endif %}>Arquivado</option>
                            <option value="Erro" {% if filtros.status == 'Erro' %}selected{% endif %}>Erro</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="tipo-filter">Tipo</label>
                        <select id="tipo-filter" name="tipo_notificacao" onchange="this.form.submit()">
                            <option value="">Todos</option>
                            {% for tipo in tipos_notificacao %}<option value="{{ tipo }}" {% if filtros.tipo_notificacao == tipo %}selected{% endif %}>{{ tipo }}</option>{% endfor %}
                        </select>
                    </div>
                </form>
            </section>
            
            <!-- Tabela Principal -->
            <table>
                <thead>
                    <tr>
                        <th style="width: 12%;">NPJ</th> <th style="width: 15%;">Tipo</th> <th style="width: 10%;">Data</th>
                        <th style="width: 10%;">Status</th> <th style="width: 23%;">Andamentos</th> <th style="width: 23%;">Documentos</th>
                        <th style="width: 7%;">Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for reg in registros %}
                    <tr>
                        <td>{{ reg.NPJ }}</td> <td>{{ reg.tipo_notificacao }}</td> <td>{{ reg.data_notificacao }}</td>
                        <td><span class="status status-{{ reg.status.replace(' ', '-') }}">{{ status_map.get(reg.status, reg.status) }}</span></td>
                        <td>
                            {% if reg.andamentos %}
                                {% for andamento in reg.andamentos %}
                                    {% if andamento.texto %}<details><summary>{{ andamento.data }} - {{ andamento.tipo }}</summary><div class="publication-text">{{ andamento.texto }}</div></details>
                                    {% else %}<div>{{ andamento.data }} - {{ andamento.tipo }}</div>{% endif %}
                                {% endfor %}
                            {% else %}-{% endif %}
                        </td>
                        <td>
                            {% if reg.documentos %}
                                {% for doc in reg.documentos %}<div><a href="/downloads/{{ doc.caminho_relativo }}" download>{{ doc.nome_arquivo }}</a></div>{% endfor %}
                            {% else %}-{% endif %}
                        </td>
                        <td>
                            {% if reg.status in ['Processado', 'Processado em Teste'] %}<form action="{{ url_for('arquivar', item_id=reg.id) }}" method="post" style="margin:0;"><button type="submit" class="action-button">Arquivar</button></form>
                            {% elif reg.status == 'Arquivado' %}<form action="{{ url_for('desarquivar', item_id=reg.id) }}" method="post" style="margin:0;"><button type="submit" class="action-button">Desarquivar</button></form>{% endif %}
                        </td>
                    </tr>
                    {% else %}
                    <tr><td colspan="7" style="text-align:center; padding: 20px;">Nenhuma notificação encontrada.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="pagination">
                {% if paginas > 1 %}{% for p in range(1, paginas + 1) %}<a href="{{ url_for('index', page=p, **filtros) }}" class="{{ 'active' if p == pagina_atual else '' }}">{{ p }}</a>{% endfor %}{% endif %}
            </div>
        </div>

        <div id="Logs" class="tab-content">
            <h2>Histórico Completo de Execuções da RPA</h2>
            <table>
                <thead>
                    <tr>
                        <th>Data e Hora</th><th>Duração</th><th>Notificações Novas</th>
                        <th>Andamentos Capturados</th><th>Documentos Baixados</th>
                        <th>Sucessos</th><th>Falhas</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ log.timestamp }}</td>
                        <td>{{ log.duracao_formatada }}</td>
                        <td>{{ log.notificacoes_salvas }}</td>
                        <td>{{ log.andamentos_capturados }}</td>
                        <td>{{ log.documentos_baixados }}</td>
                        <td style="color: #28a745;">{{ log.npjs_sucesso }}</td>
                        <td style="color: #dc3545;">{{ log.npjs_falha }}</td>
                    </tr>
                    {% else %}
                    <tr><td colspan="7" style="text-align:center; padding: 20px;">Nenhum log de execução encontrado.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
    </div>

    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) { tabcontent[i].style.display = "none"; }
            tablinks = document.getElementsByClassName("tab-button");
            for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", ""); }
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
    </script>
</body>
</html>
"""

# --- ROTAS FLASK ---
@app.route('/')
def index():
    status_map = {
        "Pendente": "Novo", "Processado": "Processado",
        "Processado em Teste": "Obtido em Teste", "Arquivado": "Arquivado", "Erro": "Erro"
    }
    pagina_atual = request.args.get('page', 1, type=int)
    filtros = {
        'status': request.args.get('status', ''),
        'tipo_notificacao': request.args.get('tipo_notificacao', ''),
    }

    # --- Lógica de Banco de Dados ---
    conn = get_db_connection()
    # Constrói a query de notificações com filtros
    query_base = "SELECT * FROM notificacoes"
    count_query = "SELECT COUNT(id) FROM notificacoes"
    params = []
    conditions = []
    if filtros['status']:
        conditions.append("status = ?")
        params.append(filtros['status'])
    if filtros['tipo_notificacao']:
        conditions.append("tipo_notificacao = ?")
        params.append(filtros['tipo_notificacao'])
    if conditions:
        where_clause = " WHERE " + " AND ".join(conditions)
        query_base += where_clause
        count_query += where_clause
    query_base += " ORDER BY data_criacao DESC LIMIT ? OFFSET ?"
    
    total_items = conn.execute(count_query, params).fetchone()[0]
    offset = (pagina_atual - 1) * ITENS_POR_PAGINA
    registros = conn.execute(query_base, params + [ITENS_POR_PAGINA, offset]).fetchall()
    tipos_notificacao = [row['tipo_notificacao'] for row in conn.execute("SELECT DISTINCT tipo_notificacao FROM notificacoes WHERE tipo_notificacao IS NOT NULL ORDER BY tipo_notificacao").fetchall()]
    conn.close()

    # --- Processamento de Dados para o Template ---
    registros_processados = []
    for reg in registros:
        reg_dict = dict(reg)
        for key in ['andamentos', 'documentos']:
            try:
                reg_dict[key] = json.loads(reg_dict[key]) if reg_dict[key] else []
            except (json.JSONDecodeError, TypeError):
                reg_dict[key] = []
        registros_processados.append(reg_dict)
    
    paginas = (total_items + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA

    # --- Lógica de Logs ---
    logs_execucao = get_db_table_data('logs_execucao')
    # Processa a lista inteira de logs para formatação
    for log in logs_execucao:
        log['duracao_formatada'] = formatar_duracao(log.get('duracao_total'))
        try:
            log['npjs_sucesso'] = int(log.get('npjs_sucesso', 0) or 0)
        except (ValueError, TypeError):
            log['npjs_sucesso'] = 0
        try:
            falha_val = log.get('npjs_falha', 0)
            log['npjs_falha'] = 1 if str(falha_val).lower() == 'crítico' else int(falha_val or 0)
        except (ValueError, TypeError):
            log['npjs_falha'] = 0

    return render_template_string(HTML_TEMPLATE,
                                  registros=registros_processados,
                                  tipos_notificacao=tipos_notificacao,
                                  paginas=paginas,
                                  pagina_atual=pagina_atual,
                                  filtros=filtros,
                                  status_map=status_map,
                                  logo=LOGO_BASE64,
                                  logs=logs_execucao) # Passa a lista completa de logs

@app.route('/update_status/<int:item_id>/<string:status>', methods=['POST'])
def update_status(item_id, status):
    """Rota genérica para arquivar/desarquivar."""
    new_status = 'Arquivado' if status == 'arquivar' else 'Processado'
    conn = get_db_connection()
    conn.execute("UPDATE notificacoes SET status = ? WHERE id = ?", (new_status, item_id))
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for('index'))

@app.route('/arquivar/<int:item_id>', methods=['POST'])
def arquivar(item_id):
    return update_status(item_id, 'arquivar')

@app.route('/desarquivar/<int:item_id>', methods=['POST'])
def desarquivar(item_id):
    return update_status(item_id, 'desarquivar')

@app.route('/downloads/<path:path>')
def serve_download(path):
    """Serve os arquivos da pasta de downloads."""
    return send_from_directory(DOWNLOADS_DIR, path, as_attachment=True)

def abrir_navegador():
    """Abre o navegador na URL do dashboard."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)
    
    init_db() # Garante que o DB e as tabelas existam ao iniciar

    print("="*50)
    print("Servidor web OneNotify iniciado.")
    print("Acesse em seu navegador: http://127.0.0.1:5000")
    print("Para parar o servidor, pressione CTRL+C no terminal.")
    print("="*50)
    Timer(1, abrir_navegador).start()
    app.run(port=5000, debug=False, use_reloader=False)

