# arquivo: visualizador_web.py
import sqlite3
import json
import os
import webbrowser
from threading import Timer
from flask import Flask, render_template_string, send_from_directory, request, redirect, url_for, flash

# Importa as funções do módulo de banco de dados central
import database

# --- CONFIGURAÇÃO ---
ITENS_POR_PAGINA = 15
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, database.DB_NOME) 
DOWNLOADS_DIR = os.path.join(BASE_DIR, 'downloads')
LOGO_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASIAAACuCAYAAAB8CV3AAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARTSURBVHhe7d3/S9t3fcfx9Z0aUhAFRRBFEAQV0V1RFF0UWVhcLItcFtdFtry2/gJbLHuLrbHWv6DD+gt0XRRdlF21KIti14WLolB0UVDU4eD/4PzT5A0kpLkk581534/n45LzfvD53u+53A/JvU/IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA-!"

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-rpa-dashboard'

# --- ANTI-CACHE PARA DESENVOLVIMENTO ---
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# --- FUNÇÕES AUXILIARES ---
def formatar_duracao(segundos):
    try:
        segundos = float(segundos)
    except (ValueError, TypeError):
        return "0 segundos"
    if segundos < 0: return "0 segundos"
    if segundos < 60:
        return f"{segundos:.1f} segundos"
    minutos, seg = divmod(segundos, 60)
    return f"{int(minutos)} minuto(s) e {int(seg)} segundo(s)"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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
        
        .filter-section { background-color: var(--secondary-color); padding: 1.5em; border-radius: 8px; margin-bottom: 20px; display: flex; gap: 20px; align-items: center; flex-wrap: wrap; }
        .filter-group { display: flex; flex-direction: column; }
        .filter-group label { margin-bottom: 8px; font-size: 0.9em; font-weight: 500; color: var(--tab-inactive); }
        select, input[type="date"], button { padding: 10px 15px; border: 1px solid var(--border-color); border-radius: 6px; background-color: var(--primary-color); color: var(--text-color); font-size: 1em; cursor: pointer; }
        button { background-color: var(--accent-color); border-color: var(--accent-color); color: white; font-weight: 600; transition: background-color 0.2s; }
        button:hover { background-color: #d43a53; }
        .actions-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5em; }
        
        table { width: 100%; border-collapse: collapse; font-size: 0.9em; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid var(--border-color); word-break: break-word; vertical-align: middle; }
        th { background-color: var(--secondary-color); font-weight: 600; color: var(--header-color); }
        tr:hover { background-color: var(--hover-color); }
        input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
        
        .status { padding: 5px 10px; border-radius: 15px; color: #fff; font-weight: 500; text-align: center; display: inline-block; min-width: 80px; }
        .status-Pendente { background-color: #ffc107; color: #1a1a2e; }
        .status-Processado, .status-Processado-em-Teste { background-color: #007bff; }
        .status-Arquivado { background-color: #6c757d; }
        .status-Erro { background-color: #dc3545; }
        
        .badge { background-color: var(--accent-color); color: white; border-radius: 10px; padding: 2px 8px; font-size: 0.8em; font-weight: 600; margin-left: 8px; vertical-align: middle; }
        
        .action-button { background: none; border: 1px solid var(--border-color); color: var(--tab-inactive); padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 0.9em; transition: all 0.2s; }
        .action-button:hover { background-color: var(--hover-color); color: #fff; }
        
        .pagination { margin-top: 20px; text-align: center; }
        .pagination a, .pagination span { display: inline-block; padding: 8px 14px; margin: 0 4px; border: 1px solid var(--border-color); border-radius: 4px; transition: all 0.2s; }
        .pagination a { color: var(--accent-color); text-decoration: none; }
        .pagination a:hover, .pagination a.active { background-color: var(--accent-color); color: white; border-color: var(--accent-color); }
        .pagination span.disabled { color: #555; background-color: var(--primary-color); cursor: not-allowed; }
        .pagination span.ellipsis { border: none; padding: 8px 5px; color: var(--text-color); background: none; }

        details summary { cursor: pointer; font-weight: 500; padding: 5px; border-radius: 4px; }
        details summary:hover { background-color: var(--hover-color); }
        .publication-text { white-space: pre-wrap; background-color: var(--bg-color); padding: 10px; margin-top: 5px; border-radius: 4px; font-family: monospace; max-height: 250px; overflow-y: auto; border: 1px solid var(--border-color); }
        
        .flash-messages { margin-bottom: 1em; }
        .flash-message { padding: 1em; background-color: var(--secondary-color); border-left: 5px solid var(--accent-color); color: white; border-radius: 6px; text-align: center; font-weight: 600; }
        
        a { color: #8ab4f8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="logo-container">
                <img src="{{ logo }}" alt="Logo OneNotify" class="logo">
                <h1>Dashboard de Notificações</h1>
            </div>
        </header>

        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="flash-messages">
                    {% for message in messages %}
                        <div class="flash-message">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'Dashboard')">Dashboard Principal</button>
            <button class="tab-button" onclick="openTab(event, 'Logs')">Histórico de Execuções</button>
        </div>

        <div id="Dashboard" class="tab-content active">
            <section class="filter-section">
                <form method="get" style="display: contents;">
                    <div class="filter-group">
                        <label for="status-filter">Status:</label>
                        <select id="status-filter" name="status" onchange="this.form.submit()">
                            <option value="Todos" {% if status_selecionado == 'Todos' %}selected{% endif %}>Todos</option>
                            <option value="Pendente" {% if status_selecionado == 'Pendente' %}selected{% endif %}>Pendente</option>
                            <option value="Processado" {% if status_selecionado == 'Processado' %}selected{% endif %}>Processado</option>
                            <option value="Arquivado" {% if status_selecionado == 'Arquivado' %}selected{% endif %}>Arquivado</option>
                            <option value="Erro" {% if status_selecionado == 'Erro' %}selected{% endif %}>Erro</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="tipo-filter">Tipo:</label>
                        <select id="tipo-filter" name="tipo" onchange="this.form.submit()">
                            <option value="Todos" {% if tipo_selecionado == 'Todos' %}selected{% endif %}>Todos</option>
                            {% for tipo in tipos_notificacao %}<option value="{{ tipo }}" {% if tipo_selecionado == tipo %}selected{% endif %}>{{ tipo }}</option>{% endfor %}
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="data-inicio">Data Início:</label>
                        <input type="date" id="data-inicio" name="data_inicio" value="{{ data_inicio_filtro }}">
                    </div>
                    <div class="filter-group">
                        <label for="data-fim">Data Fim:</label>
                        <input type="date" id="data-fim" name="data_fim" value="{{ data_fim_filtro }}">
                    </div>
                    <div class="filter-group" style="justify-content: flex-end;">
                         <button type="submit">Filtrar</button>
                    </div>
                </form>
            </section>
            
            <form id="bulk-action-form" action="{{ url_for('arquivar_lote') }}" method="post">
                <div class="actions-bar">
                    <button type="submit">Arquivar Selecionados</button>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th style="width: 3%;"><input type="checkbox" id="select-all"></th>
                            <th style="width: 20%;">NPJ</th>
                            <th style="width: 15%;">Tipo(s)</th>
                            <th style="width: 12%;">Data(s)</th>
                            <th style="width: 10%;">Status</th>
                            <th style="width: 30%;">Andamentos e Documentos</th>
                            <th style="width: 10%;">Ação</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for reg in registros %}
                        <tr>
                            <td><input type="checkbox" name="selecao_npj" value="{{ reg.NPJ }}" class="row-checkbox"></td>
                            <td>{{ reg.NPJ }} {% if reg.notificacao_count > 1 %}<span class="badge" title="{{ reg.notificacao_count }} notificações para este NPJ">{{ reg.notificacao_count }}</span>{% endif %}</td>
                            <td>{{ reg.tipos_notificacao.replace(',', ', ') }}</td>
                            <td>{{ reg.datas_notificacao.replace(',', ', ') }}</td>
                            <td><span class="status status-{{ reg.status.replace(' ', '-') }}">{{ reg.status }}</span></td>
                            <td>
                                {% if reg.andamentos %}
                                    {% for andamento in reg.andamentos %}
                                        {% if andamento.texto %}<details><summary>{{ andamento.data }} - {{ andamento.tipo }}</summary><div class="publication-text">{{ andamento.texto }}</div></details>
                                        {% else %}<div>{{ andamento.data }} - {{ andamento.tipo }}</div>{% endif %}
                                    {% endfor %}
                                {% endif %}
                                {% if reg.documentos and reg.documentos is not string %}
                                    <div style="margin-top: 10px; border-top: 1px dashed var(--border-color); padding-top: 10px;">
                                    {% for doc in reg.documentos %}<div><a href="/downloads/{{ doc.caminho_relativo | replace('\\\\', '/') }}" download>{{ doc.nome_arquivo }}</a></div>{% endfor %}
                                    </div>
                                {% endif %}
                            </td>
                            <td>
                                {% if reg.status in ['Processado', 'Processado em Teste'] %}
                                    <form action="{{ url_for('arquivar', npj=reg.NPJ) }}" method="post" style="margin:0;"><button type="submit" class="action-button">Arquivar</button></form>
                                {% elif reg.status == 'Arquivado' %}
                                    <form action="{{ url_for('desarquivar', npj=reg.NPJ) }}" method="post" style="margin:0;"><button type="submit" class="action-button">Desarquivar</button></form>
                                {% endif %}
                            </td>
                        </tr>
                        {% else %}
                        <tr><td colspan="7" style="text-align:center; padding: 20px;">Nenhuma notificação encontrada para os filtros selecionados.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </form>
                
            <div class="pagination">
                {% if total_paginas > 1 %}
                    {% if pagina_atual > 1 %}<a href="{{ url_for('index', page=pagina_atual-1, status=status_selecionado, tipo=tipo_selecionado, data_inicio=data_inicio_filtro, data_fim=data_fim_filtro) }}">&laquo; Anterior</a>
                    {% else %}<span class="disabled">&laquo; Anterior</span>{% endif %}
                    {% for p in range(1, total_paginas + 1) %}
                        {% if p == 1 or p == total_paginas or (p >= pagina_atual - 2 and p <= pagina_atual + 2) %}
                            {% if p == pagina_atual %}<a class="active">{{ p }}</a>
                            {% else %}<a href="{{ url_for('index', page=p, status=status_selecionado, tipo=tipo_selecionado, data_inicio=data_inicio_filtro, data_fim=data_fim_filtro) }}">{{ p }}</a>{% endif %}
                        {% elif loop.previtem and (p > pagina_atual + 2 or p < pagina_atual - 2) %}<span class="ellipsis">...</span>{% endif %}
                    {% endfor %}
                    {% if pagina_atual < total_paginas %}<a href="{{ url_for('index', page=pagina_atual+1, status=status_selecionado, tipo=tipo_selecionado, data_inicio=data_inicio_filtro, data_fim=data_fim_filtro) }}">Próxima &raquo;</a>
                    {% else %}<span class="disabled">Próxima &raquo;</span>{% endif %}
                {% endif %}
            </div>
        </div>

        <div id="Logs" class="tab-content">
            <h2>Histórico Completo de Execuções da RPA</h2>
            <table>
                <thead>
                    <tr>
                        <th>Data e Hora</th><th>Duração Total</th><th>Notificações Salvas</th>
                        <th>Andamentos Capturados</th><th>Documentos Baixados</th><th>NPJs Sucesso</th><th>NPJs Falha</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in logs %}
                    <tr>
                        <td>{{ log.timestamp }}</td><td>{{ formatar_duracao(log.duracao_total) }}</td>
                        <td>{{ log.notificacoes_salvas }}</td><td>{{ log.andamentos_capturados }}</td>
                        <td>{{ log.documentos_baixados }}</td><td style="color: #28a745;">{{ log.npjs_sucesso }}</td>
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
        document.addEventListener('DOMContentLoaded', function() {
            const selectAllCheckbox = document.getElementById('select-all');
            const rowCheckboxes = document.querySelectorAll('.row-checkbox');
            const bulkActionForm = document.getElementById('bulk-action-form');
            if (selectAllCheckbox) {
                selectAllCheckbox.addEventListener('change', function() {
                    rowCheckboxes.forEach(checkbox => { checkbox.checked = selectAllCheckbox.checked; });
                });
            }
            if (bulkActionForm) {
                bulkActionForm.addEventListener('submit', function(e) {
                    const selectedCheckboxes = document.querySelectorAll('.row-checkbox:checked');
                    if (selectedCheckboxes.length === 0) {
                        alert('Por favor, selecione pelo menos um NPJ para arquivar.');
                        e.preventDefault(); return;
                    }
                    if (!confirm(`Tem certeza que deseja arquivar todas as notificações para os ${selectedCheckboxes.length} NPJ(s) selecionado(s)?`)) {
                        e.preventDefault();
                    }
                });
            }
        });
    </script>
</body>
</html>
"""

# --- ROTAS FLASK ---
@app.route('/')
def index():
    conn = get_db_connection()
    
    status_filtro = request.args.get('status', 'Todos')
    tipo_filtro = request.args.get('tipo', 'Todos')
    data_inicio_filtro = request.args.get('data_inicio', '')
    data_fim_filtro = request.args.get('data_fim', '')

    query_base = f"""
        SELECT
            NPJ,
            GROUP_CONCAT(DISTINCT tipo_notificacao) as tipos_notificacao,
            GROUP_CONCAT(DISTINCT data_notificacao) as datas_notificacao,
            MAX(status) as status,
            MAX(andamentos) as andamentos,
            MAX(documentos) as documentos,
            MAX(data_criacao) as data_criacao_recente,
            COUNT(id) as notificacao_count
        FROM {database.TABELA_NOTIFICACOES}
    """
    conditions = []
    params = []
    
    if status_filtro and status_filtro != 'Todos':
        conditions.append("status = ?")
        params.append(status_filtro)
    if tipo_filtro and tipo_filtro != 'Todos':
        conditions.append("tipo_notificacao = ?")
        params.append(tipo_filtro)
    if data_inicio_filtro:
        conditions.append("STRFTIME('%Y-%m-%d', SUBSTR(data_notificacao, 7, 4) || '-' || SUBSTR(data_notificacao, 4, 2) || '-' || SUBSTR(data_notificacao, 1, 2)) >= ?")
        params.append(data_inicio_filtro)
    if data_fim_filtro:
        conditions.append("STRFTIME('%Y-%m-%d', SUBSTR(data_notificacao, 7, 4) || '-' || SUBSTR(data_notificacao, 4, 2) || '-' || SUBSTR(data_notificacao, 1, 2)) <= ?")
        params.append(data_fim_filtro)
        
    if conditions:
        query_base += " WHERE " + " AND ".join(conditions)

    query_base += " GROUP BY NPJ ORDER BY data_criacao_recente DESC"

    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * ITENS_POR_PAGINA
    
    query_paginada = f"{query_base} LIMIT ? OFFSET ?"
    params_paginados = params + [ITENS_POR_PAGINA, offset]
    
    registros = conn.execute(query_paginada, params_paginados).fetchall()

    registros_processados = []
    for reg in registros:
        reg_dict = dict(reg)
        try:
            reg_dict['andamentos'] = json.loads(reg_dict['andamentos']) if reg_dict.get('andamentos') else []
            reg_dict['documentos'] = json.loads(reg_dict['documentos']) if reg_dict.get('documentos') else []
        except (json.JSONDecodeError, TypeError):
            reg_dict['andamentos'] = []
            reg_dict['documentos'] = []
        registros_processados.append(reg_dict)
        
    count_query = f"SELECT COUNT(DISTINCT NPJ) FROM {database.TABELA_NOTIFICACOES}"
    if conditions:
        count_query_params = params[:]
        count_query += " WHERE " + " AND ".join(conditions)
        total_registros = conn.execute(count_query, count_query_params).fetchone()[0]
    else:
        total_registros = conn.execute(count_query).fetchone()[0]
        
    total_paginas = (total_registros + ITENS_POR_PAGINA - 1) // ITENS_POR_PAGINA

    tipos_notificacao_query = f"SELECT DISTINCT tipo_notificacao FROM {database.TABELA_NOTIFICACOES} WHERE tipo_notificacao IS NOT NULL ORDER BY tipo_notificacao"
    tipos_notificacao = [row[0] for row in conn.execute(tipos_notificacao_query).fetchall()]

    logs_query = f"SELECT * FROM {database.TABELA_LOGS} ORDER BY id DESC"
    logs_raw = conn.execute(logs_query).fetchall()
    logs = [dict(row) for row in logs_raw]
    
    conn.close()

    return render_template_string(
        HTML_TEMPLATE,
        registros=registros_processados,
        logs=logs,
        pagina_atual=page,
        total_paginas=total_paginas,
        status_selecionado=status_filtro,
        tipo_selecionado=tipo_filtro,
        data_inicio_filtro=data_inicio_filtro,
        data_fim_filtro=data_fim_filtro,
        tipos_notificacao=tipos_notificacao,
        logo=LOGO_BASE64,
        formatar_duracao=formatar_duracao
    )

@app.route('/arquivar/<string:npj>', methods=['POST'])
def arquivar(npj):
    database.arquivar_notificacao_por_npj(npj)
    flash(f'Notificações para o NPJ {npj} foram arquivadas.')
    return redirect(request.referrer or url_for('index'))

@app.route('/desarquivar/<string:npj>', methods=['POST'])
def desarquivar(npj):
    database.desarquivar_notificacao_por_npj(npj)
    flash(f'Notificações para o NPJ {npj} foram desarquivadas.')
    return redirect(request.referrer or url_for('index'))

@app.route('/arquivar_lote', methods=['POST'])
def arquivar_lote():
    npjs_para_arquivar = request.form.getlist('selecao_npj')
    if npjs_para_arquivar:
        registros_afetados = database.arquivar_notificacoes_em_lote_por_npj(npjs_para_arquivar)
        flash(f'{registros_afetados} notificações (de {len(npjs_para_arquivar)} NPJs) foram arquivadas com sucesso!')
    else:
        flash('Nenhum NPJ foi selecionado para arquivar.')
    return redirect(request.referrer or url_for('index'))

# --- CORREÇÃO APLICADA AQUI ---
@app.route('/downloads/<path:path>')
def serve_download(path):
    # A função send_from_directory do Flask é a forma segura de enviar arquivos.
    # Ela lida com as verificações de segurança para evitar ataques de "path traversal".
    try:
        return send_from_directory(DOWNLOADS_DIR, path, as_attachment=True)
    except Exception as e:
        # Adiciona um log no terminal para facilitar a depuração em caso de erro
        print(f"ERRO ao tentar servir o arquivo: {path}. Detalhes: {e}")
        # Retorna um erro 404 (Não Encontrado) para o navegador
        return "Arquivo não encontrado ou acesso negado.", 404

def abrir_navegador():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)
    
    database.inicializar_banco() 

    print("="*50)
    print("Servidor web OneNotify iniciado.")
    print("Acesse em seu navegador: http://127.0.0.1:5000")
    print("Para parar o servidor, pressione CTRL+C no terminal.")
    print("="*50)
    Timer(1, abrir_navegador).start()
    app.run(port=5000, debug=True, use_reloader=False)

