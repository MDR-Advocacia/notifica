# arquivo: visualizador_web.py
import sqlite3
import json
import os
import math
from flask import Flask, render_template_string, send_from_directory, request, redirect, url_for
import webbrowser
from threading import Timer
import database

# --- CONFIGURAÇÃO ---
ITENS_POR_PAGINA = 10
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')

app = Flask(__name__)

# --- TEMPLATE HTML EMBUTIDO ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Execução - RPA</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f4f7f9; color: #333; margin: 0; padding: 2em; }
        .container { max-width: 1800px; margin: auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        h1 { color: #1a2b4d; padding-bottom: 10px; }
        .tabs { border-bottom: 2px solid #dee2e6; margin-bottom: 20px; }
        .tab-button { background: none; border: none; padding: 15px 25px; font-size: 1.1em; cursor: pointer; transition: color 0.2s, border-bottom 0.2s; color: #6c757d; border-bottom: 3px solid transparent; }
        .tab-button.active { color: #007bff; border-bottom: 3px solid #007bff; font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 0.9em; table-layout: fixed; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; word-break: break-word; vertical-align: top; }
        th { background-color: #f8f9fa; font-weight: 600; }
        tr:hover { background-color: #f5f5f5; }
        
        .status-icon { height: 15px; width: 15px; border-radius: 50%; display: inline-block; vertical-align: middle; }
        .status-Pendente { background-color: #5cb85c; }
        .status-Processado { background-color: #5cb85c; }
        .status-Processado-em-Teste { background-color: #5bc0de; }
        .status-Arquivado { background-color: #6c757d; }
        .status-Erro { background-color: #d9534f; }
        
        .no-data { text-align: center; padding: 20px; color: #888; font-size: 1.1em; }
        .data-list { margin: 0; padding: 0; list-style: none; }
        .data-item details { margin-bottom: 5px; }
        .data-item summary { cursor: pointer; padding: 8px 12px; background-color: #e9ecef; border-radius: 4px; font-weight: 500; transition: background-color 0.2s; display: block; }
        .data-item summary:hover { background-color: #dee2e6; }
        .publication-text { border: 1px solid #eee; padding: 10px; margin-top: -1px; border-radius: 0 0 4px 4px; background-color: #fdfdfd; white-space: pre-wrap; font-family: "Courier New", Courier, monospace; font-size: 0.95em; max-height: 300px; overflow-y: auto; }
        .document-item, .andamento-item { padding: 8px 12px; background-color: #f8f9fa; border-radius: 4px; margin-bottom: 5px; }
        .document-item a { color: #0056b3; text-decoration: none; font-weight: 500; }
        .document-item a:hover { text-decoration: underline; }
        .no-data-cell { color: #888; font-style: italic; font-size: 0.9em; padding-top: 5px; }
        .filter-section { background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; display: flex; gap: 20px; align-items: center; }
        .filter-group { display: flex; flex-direction: column; }
        .filter-group label { margin-bottom: 5px; font-weight: 500; color: #555; }
        .filter-group select, .filter-group input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        .filter-button { padding: 10px 20px; border: none; background-color: #007bff; color: white; border-radius: 4px; cursor: pointer; align-self: flex-end; }
        .pagination { margin-top: 20px; text-align: center; }
        .pagination a { color: #007bff; padding: 8px 12px; text-decoration: none; border: 1px solid #ddd; margin: 0 2px; border-radius: 4px; }
        .pagination a.active { background-color: #007bff; color: white; border-color: #007bff; }
        .pagination a:hover:not(.active) { background-color: #f0f0f0; }
        .action-button { background: none; border: 1px solid #6c757d; color: #6c757d; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 0.9em; }
        .unarchive-button { border-color: #28a745; color: #28a745; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Dashboard de Execução da RPA</h1>
        
        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'Dashboard')">Dashboard</button>
            <button class="tab-button" onclick="openTab(event, 'Logs')">Logs de Execução</button>
        </div>

        <div id="Dashboard" class="tab-content active">
            <section class="filter-section">
                <form method="get" style="display: contents;">
                    <div class="filter-group">
                        <label for="status-filter">Filtrar por Status</label>
                        <select id="status-filter" name="status">
                            <option value="">Todos</option>
                            <option value="Pendente" {% if filtros.status == 'Pendente' %}selected{% endif %}>Novo</option>
                            <option value="Processado" {% if filtros.status == 'Processado' %}selected{% endif %}>Processado</option>
                            <option value="Processado em Teste" {% if filtros.status == 'Processado em Teste' %}selected{% endif %}>Obtido em Teste</option>
                            <option value="Arquivado" {% if filtros.status == 'Arquivado' %}selected{% endif %}>Arquivado</option>
                            <option value="Erro" {% if filtros.status == 'Erro' %}selected{% endif %}>Erro</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="tipo-filter">Filtrar por Tipo</label>
                        <select id="tipo-filter" name="tipo_notificacao">
                            <option value="">Todos</option>
                            {% for tipo in tipos_notificacao %}
                            <option value="{{ tipo }}" {% if filtros.tipo_notificacao == tipo %}selected{% endif %}>{{ tipo }}</option>
                            {% endfor %}
                        </select>
                    </div>
                     <div class="filter-group">
                        <label for="ordenar-filter">Ordenar por</label>
                        <select name="ordenar_por">
                            <option value="data_criacao" {% if filtros.ordenar_por == 'data_criacao' %}selected{% endif %}>Data (Mais Recente)</option>
                            <option value="status" {% if filtros.ordenar_por == 'status' %}selected{% endif %}>Status</option>
                        </select>
                    </div>
                    <button type="submit" class="filter-button">Filtrar</button>
                </form>
            </section>
            
            <table>
                <thead>
                    <tr>
                        <th style="width: 5%;">Status</th>
                        <th style="width: 10%;">NPJ</th>
                        <th style="width: 15%;">Adverso Principal</th>
                        <th style="width: 15%;">Tipo Notificação</th>
                        <th style="width: 8%;">Data Notificação</th>
                        <th style="width: 20%;">Andamentos</th>
                        <th style="width: 20%;">Documentos</th>
                        <th style="width: 7%;">Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {% for reg in registros %}
                    <tr>
                        <td>
                            <span class="status-icon status-{{ reg.status.replace(' ', '-') }}" title="{{ status_map.get(reg.status, reg.status) }}"></span>
                        </td>
                        <td>{{ reg.NPJ }}</td>
                        <td>{{ reg.adverso_principal if reg.adverso_principal else '<span class="no-data-cell">Falha na captura</span>'|safe }}</td>
                        <td>{{ reg.tipo_notificacao }}</td>
                        <td>{{ reg.data_notificacao }}</td>
                        <td>
                            {% if reg.andamentos %}
                                <ul class="data-list">
                                {% for andamento in reg.andamentos %}
                                    <li class="data-item">
                                        {% if andamento.texto %}
                                        <details><summary><b>{{ andamento.data }}</b> - {{ andamento.tipo }}</summary><div class="publication-text">{{ andamento.texto }}</div></details>
                                        {% else %}
                                        <div class="andamento-item"><b>{{ andamento.data }}</b> - {{ andamento.tipo }}</div>
                                        {% endif %}
                                    </li>
                                {% endfor %}
                                </ul>
                            {% elif reg.status != 'Pendente' %}
                                <div class="no-data-cell">Nenhum andamento encontrado.</div>
                            {% else %}-{% endif %}
                        </td>
                        <td>
                            {% if reg.documentos %}
                                <ul class="data-list">
                                {% for doc in reg.documentos %}
                                    <li class="document-item">
                                       <b>{{ doc.data }}</b> - <a href="/downloads/{{ doc.caminho_relativo }}" download>{{ doc.nome_arquivo }}</a>
                                    </li>
                                {% endfor %}
                                </ul>
                            {% elif reg.status != 'Pendente' %}
                                <div class="no-data-cell">Nenhum documento encontrado.</div>
                            {% else %}-{% endif %}
                        </td>
                        <td>
                            {% if reg.status in ['Processado', 'Processado em Teste'] %}
                            <form action="{{ url_for('arquivar', item_id=reg.id) }}" method="post" style="margin:0;">
                                <button type="submit" class="action-button">Arquivar</button>
                            </form>
                            {% elif reg.status == 'Arquivado' %}
                            <form action="{{ url_for('desarquivar', item_id=reg.id) }}" method="post" style="margin:0;">
                                <button type="submit" class="action-button unarchive-button">Desarquivar</button>
                            </form>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <div class="pagination">
                {% if paginas > 1 %}
                    {% for p in range(1, paginas + 1) %}
                        <a href="{{ url_for('index', page=p, **filtros) }}" class="{{ 'active' if p == pagina_atual else '' }}">{{ p }}</a>
                    {% endfor %}
                {% endif %}
            </div>

        </div>

        <div id="Logs" class="tab-content">
             <table>
                <thead>
                    <tr>
                        <th>Data e Hora</th><th>Duração Total</th><th>Média por NPJ</th><th>Notificações</th>
                        <th>Andamentos</th><th>Documentos</th><th>Sucesso</th><th>Falha</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ log.timestamp }}</td><td>{{ log.duracao_total }}</td><td>{{ log.tempo_medio_npj }}</td>
                        <td>{{ log.notificacoes_salvas }}</td><td>{{ log.andamentos_capturados }}</td>
                        <td>{{ log.documentos_baixados }}</td><td>{{ log.npjs_sucesso }}</td><td>{{ log.npjs_falha }}</td>
                    </tr>
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
            for (i = 0; i < tablinks.length; i++) { tablinks[i].className = tablinks[i].className.replace(" active", "");}
            document.getElementById(tabName).style.display = "block";
            evt.currentTarget.className += " active";
        }
        document.addEventListener("DOMContentLoaded", function() {
            const activeTab = new URLSearchParams(window.location.search).get('tab') || 'Dashboard';
            document.querySelector(`.tab-button[onclick*="'${activeTab}'"]`).click();
        });
    </script>
</body>
</html>
"""

def get_db_table_data(table_name):
    # ... (código existente sem alterações)
    try:
        conn = sqlite3.connect(database.DB_NOME)
        conn.row_factory = sqlite3.Row
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

@app.route('/')
def index():
    # ... (código existente sem alterações)
    status_map = {
        "Pendente": "Novo",
        "Processado": "Processado",
        "Processado em Teste": "Obtido em Teste",
        "Arquivado": "Arquivado",
        "Erro": "Erro"
    }

    pagina_atual = request.args.get('page', 1, type=int)
    filtros = {
        'status': request.args.get('status', ''),
        'tipo_notificacao': request.args.get('tipo_notificacao', ''),
        'ordenar_por': request.args.get('ordenar_por', 'data_criacao'),
    }

    registros_processos = database.obter_notificacoes_paginadas(filtros, pagina_atual, ITENS_POR_PAGINA)
    total_registros = database.contar_notificacoes(filtros)
    tipos_notificacao = database.obter_tipos_notificacao_unicos()
    logs_execucao = get_db_table_data(database.TABELA_LOGS)

    for reg in registros_processos:
        for key in ['andamentos', 'documentos']:
            if reg.get(key):
                try: reg[key] = json.loads(reg[key])
                except (json.JSONDecodeError, TypeError): reg[key] = []
            else: reg[key] = []

    paginas = math.ceil(total_registros / ITENS_POR_PAGINA)

    return render_template_string(HTML_TEMPLATE, 
                                  registros=registros_processos, 
                                  logs=logs_execucao,
                                  tipos_notificacao=tipos_notificacao,
                                  paginas=paginas,
                                  pagina_atual=pagina_atual,
                                  filtros=filtros,
                                  status_map=status_map)

@app.route('/arquivar/<int:item_id>', methods=['POST'])
def arquivar(item_id):
    # ... (código existente sem alterações)
    database.arquivar_notificacao(item_id)
    return redirect(url_for('index', **request.args))

@app.route('/desarquivar/<int:item_id>', methods=['POST'])
def desarquivar(item_id):
    """Rota para desarquivar uma notificação."""
    database.desarquivar_notificacao(item_id)
    # Mantém os filtros após a ação, passando os argumentos da requisição
    return redirect(url_for('index', **request.args))


@app.route('/downloads/<path:path>')
def serve_download(path):
    # ... (código existente sem alterações)
    return send_from_directory(DOWNLOADS_DIR, path, as_attachment=True)

def abrir_navegador():
    # ... (código existente sem alterações)
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # ... (código existente sem alterações)
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

    print("="*50)
    print("Servidor web para visualização dos resultados da RPA.")
    print("Acesse em seu navegador: http://127.0.0.1:5000")
    print("Para parar o servidor, pressione CTRL+C no terminal.")
    print("="*50)
    Timer(1, abrir_navegador).start()
    app.run(port=5000, debug=False)

