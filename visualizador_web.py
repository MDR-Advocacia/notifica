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

# --- TEMPLATE HTML E CSS ATUALIZADO ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OneNotify - Dashboard</title>
    <style>
        /* ============================================== */
        /* ===         RESET E ESTILOS GLOBAIS        === */
        /* ============================================== */
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
            'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
            sans-serif;
          -webkit-font-smoothing: antialiased;
          -moz-osx-font-smoothing: grayscale;
          background: linear-gradient(120deg, #1d2b4b 0%, #3a506b 100%);
          color: #e0e0e0;
          min-height: 100vh;
        }
        /* ============================================== */
        /* ===             ESTRUTURA GERAL            === */
        /* ============================================== */
        .App {
          text-align: center;
        }
        .App-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1rem 2rem;
          font-size: calc(10px + 2vmin);
          color: white;
          background: rgba(255, 255, 255, 0.1);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.15);
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .header-logo {
          height: 40px;
        }
        .panel-container {
          padding: 2rem;
          max-width: 1800px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        .input-section, .results-section {
          padding: 2rem;
          text-align: left;
          border-radius: 16px;
          background: rgba(255, 255, 255, 0.08);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          border: 1px solid rgba(255, 255, 255, 0.18);
          box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
        }
        .input-section h2, .results-section h2 {
          margin-bottom: 1.5rem;
          color: #ffffff;
          border-bottom: 2px solid #5bc0de;
          padding-bottom: 0.5rem;
          display: inline-block;
        }
        /* ============================================== */
        /* ===           INPUTS E BOTÕES              === */
        /* ============================================== */
        select, textarea, input.filter-input, .item-add-form input, input[type="date"] {
          width: 100%;
          padding: 12px;
          margin-bottom: 1rem;
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 8px;
          font-size: 1rem;
          background: rgba(0, 0, 0, 0.2);
          color: #f0f0f0;
        }
        textarea::placeholder, input::placeholder {
          color: #a0a0a0;
        }
        .button-group {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
        }
        button {
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          color: white;
          background-color: #5bc0de;
          cursor: pointer;
          font-weight: bold;
          font-size: 1rem;
          transition: all 0.3s ease;
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(91, 192, 222, 0.4);
        }
        button:disabled {
          background-color: #555;
          cursor: not-allowed;
          opacity: 0.6;
        }
        /* ============================================== */
        /* ===             TABELA E FILTROS           === */
        /* ============================================== */
        .filter-container {
          display: flex;
          flex-wrap: wrap;
          gap: 1rem;
          align-items: flex-end;
        }
        .filter-group {
          display: flex;
          flex-direction: column;
          flex-grow: 1;
          min-width: 150px;
        }
        .filter-group label {
          margin-bottom: 0.5rem;
          font-weight: bold;
          text-align: left;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 1.5rem;
          color: #e0e0e0;
        }
        th, td {
          padding: 15px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          text-align: left;
          vertical-align: middle;
        }
        thead {
          background-color: rgba(0, 0, 0, 0.2);
        }
        th {
          font-weight: bold;
          color: #ffffff;
        }
        tbody tr:hover {
          background-color: rgba(91, 192, 222, 0.1);
        }
        /* Adicionando estilos para status com base no visualizador_web.py original */
        .status {
          padding: 5px 12px;
          border-radius: 20px;
          font-weight: bold;
          color: #fff;
          text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
          white-space: nowrap;
          font-size: 0.9em;
          text-align: center;
        }
        .status-Pendente { background-color: #f0ad4e; }
        .status-Processado, .status-Processado-em-Teste { background-color: #007bff; }
        .status-Arquivado { background-color: #6c757d; }
        .status-Erro { background-color: #dc3545; }
        .badge { background-color: #5bc0de; color: #1d2b4b; border-radius: 10px; padding: 3px 8px; font-size: 0.8em; font-weight: bold; margin-left: 8px; }
        /* ============================================== */
        /* ===           PAGINAÇÃO E MODAIS           === */
        /* ============================================== */
        .pagination-controls {
          display: flex;
          justify-content: center;
          align-items: center;
          margin-top: 1.5rem;
          padding: 10px;
          background-color: rgba(0, 0, 0, 0.2);
          border-radius: 8px;
        }
        .page-navigation { display: flex; align-items: center; gap: 5px; }
        .page-navigation a, .page-navigation span {
            color: white;
            padding: 8px 12px;
            text-decoration: none;
            border-radius: 4px;
            border: 1px solid transparent;
            transition: all 0.3s ease;
        }
        .page-navigation a:hover {
            background-color: #5bc0de;
            border-color: #5bc0de;
        }
        .page-navigation .active {
            background-color: #5bc0de;
            font-weight: bold;
        }
        .page-navigation .disabled {
            color: #777;
            cursor: not-allowed;
        }
        .flash-message {
            padding: 1em;
            margin-bottom: 1.5rem;
            background-color: rgba(0, 0, 0, 0.2);
            border-left: 5px solid #5bc0de;
            color: white;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
        }
        a { color: #5bc0de; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .publication-text { white-space: pre-wrap; background-color: rgba(0,0,0,0.3); padding: 10px; margin-top: 5px; border-radius: 4px; font-family: monospace; max-height: 200px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.1); }
        /* ============================================== */
        /* ===      ESTILOS ABAS E OUTROS             === */
        /* ============================================== */
        .modal-tabs {
          display: flex;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
          margin-bottom: 2rem;
        }
        .tab-button {
          padding: 10px 20px;
          cursor: pointer;
          background-color: transparent;
          border: none;
          color: rgba(255, 255, 255, 0.6);
          font-size: 1rem;
          border-bottom: 3px solid transparent;
          margin-bottom: -1px;
        }
        .tab-button.active {
          color: white;
          border-bottom: 3px solid #5bc0de;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="App">
        <header class="App-header">
            <img src="{{ logo }}" alt="Logo OneNotify" class="header-logo">
            <h1>Dashboard de Notificações</h1>
        </header>

        <div class="panel-container">
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    {% for message in messages %}
                        <div class="flash-message">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="modal-tabs">
                <button class="tab-button active" onclick="openTab(event, 'Dashboard')">Dashboard Principal</button>
                <button class="tab-button" onclick="openTab(event, 'Logs')">Histórico de Execuções</button>
            </div>

            <div id="Dashboard" class="tab-content active">
                <section class="input-section">
                    <form method="get">
                        <div class="filter-container">
                            <div class="filter-group">
                                <label for="status-filter">Status:</label>
                                <select id="status-filter" name="status">
                                    <option value="Todos" {% if status_selecionado == 'Todos' %}selected{% endif %}>Todos</option>
                                    <option value="Pendente" {% if status_selecionado == 'Pendente' %}selected{% endif %}>Pendente</option>
                                    <option value="Processado" {% if status_selecionado == 'Processado' %}selected{% endif %}>Processado</option>
                                    <option value="Arquivado" {% if status_selecionado == 'Arquivado' %}selected{% endif %}>Arquivado</option>
                                    <option value="Erro" {% if status_selecionado == 'Erro' %}selected{% endif %}>Erro</option>
                                </select>
                            </div>
                            <div class="filter-group">
                                <label for="tipo-filter">Tipo:</label>
                                <select id="tipo-filter" name="tipo">
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
                            <div class="filter-group">
                                <button type="submit">Filtrar</button>
                            </div>
                        </div>
                    </form>
                </section>
                
                <section class="results-section">
                    <form id="bulk-action-form" action="{{ url_for('arquivar_lote') }}" method="post">
                        <div class="button-group" style="justify-content: flex-start;">
                            <button type="submit">Arquivar Selecionados</button>
                        </div>
                        
                        <table>
                            <thead>
                                <tr>
                                    <th style="width: 3%;"><input type="checkbox" id="select-all"></th>
                                    <th>NPJ</th>
                                    <th>Tipo(s)</th>
                                    <th>Data(s)</th>
                                    <th>Status</th>
                                    <th>Andamentos e Documentos</th>
                                    <th>Ação</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for reg in registros %}
                                <tr>
                                    <td><input type="checkbox" name="selecao_npj" value="{{ reg.NPJ }}" class="row-checkbox"></td>
                                    <td>{{ reg.NPJ }} {% if reg.notificacao_count > 1 %}<span class="badge" title="{{ reg.notificacao_count }} notificações">{{ reg.notificacao_count }}</span>{% endif %}</td>
                                    <td>{{ reg.tipos_notificacao.replace(',', ', ') }}</td>
                                    <td>{{ reg.datas_notificacao.replace(',', ', ') }}</td>
                                    <td><span class="status status-{{ reg.status.replace(' ', '-') }}">{{ reg.status }}</span></td>
                                    <td>
                                        {% for andamento in reg.andamentos %}
                                            {% if andamento.texto %}<details><summary>{{ andamento.data }} - {{ andamento.tipo }}</summary><div class="publication-text">{{ andamento.texto }}</div></details>
                                            {% else %}<div>{{ andamento.data }} - {{ andamento.tipo }}</div>{% endif %}
                                        {% endfor %}
                                        {% if reg.documentos and reg.documentos is not string %}
                                            <div style="margin-top: 10px; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 10px;">
                                            {% for doc in reg.documentos %}<div><a href="/downloads/{{ doc.caminho_relativo | replace('\\\\', '/') }}" download>{{ doc.nome_arquivo }}</a></div>{% endfor %}
                                            </div>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if reg.status in ['Processado', 'Processado em Teste'] %}
                                            <form action="{{ url_for('arquivar', npj=reg.NPJ) }}" method="post" style="margin:0;"><button type="submit" style="padding: 8px 16px; font-size: 0.9rem;">Arquivar</button></form>
                                        {% elif reg.status == 'Arquivado' %}
                                            <form action="{{ url_for('desarquivar', npj=reg.NPJ) }}" method="post" style="margin:0;"><button type="submit" style="padding: 8px 16px; font-size: 0.9rem; background-color: #3a506b;">Desarquivar</button></form>
                                        {% endif %}
                                    </td>
                                </tr>
                                {% else %}
                                <tr><td colspan="7" style="text-align:center; padding: 20px;">Nenhuma notificação encontrada para os filtros selecionados.</td></tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </form>
                        
                    <div class="pagination-controls">
                        <div class="page-navigation">
                            {% if total_paginas > 1 %}
                                {% if pagina_atual > 1 %}<a href="{{ url_for('index', page=pagina_atual-1, status=status_selecionado, tipo=tipo_selecionado, data_inicio=data_inicio_filtro, data_fim=data_fim_filtro) }}">&laquo;</a>
                                {% else %}<span class="disabled">&laquo;</span>{% endif %}
                                {% for p in range(1, total_paginas + 1) %}
                                    {% if p == 1 or p == total_paginas or (p >= pagina_atual - 2 and p <= pagina_atual + 2) %}
                                        {% if p == pagina_atual %}<span class="active">{{ p }}</span>
                                        {% else %}<a href="{{ url_for('index', page=p, status=status_selecionado, tipo=tipo_selecionado, data_inicio=data_inicio_filtro, data_fim=data_fim_filtro) }}">{{ p }}</a>{% endif %}
                                    {% elif loop.previtem and (p > pagina_atual + 2 or p < pagina_atual - 2) %}<span>...</span>{% endif %}
                                {% endfor %}
                                {% if pagina_atual < total_paginas %}<a href="{{ url_for('index', page=pagina_atual+1, status=status_selecionado, tipo=tipo_selecionado, data_inicio=data_inicio_filtro, data_fim=data_fim_filtro) }}">&raquo;</a>
                                {% else %}<span class="disabled">&raquo;</span>{% endif %}
                            {% endif %}
                        </div>
                    </div>
                </section>
            </div>

            <div id="Logs" class="tab-content">
                <section class="results-section">
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
                </section>
            </div>
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

# --- ROTAS FLASK (sem alteração na lógica) ---
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

@app.route('/downloads/<path:path>')
def serve_download(path):
    try:
        return send_from_directory(DOWNLOADS_DIR, path, as_attachment=True)
    except Exception as e:
        print(f"ERRO ao tentar servir o arquivo: {path}. Detalhes: {e}")
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