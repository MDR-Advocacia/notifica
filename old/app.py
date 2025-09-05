# arquivo: app.py
import sqlite3
import glob
import os
from flask import Flask, render_template, g, send_from_directory, abort

# Configuração do aplicativo Flask
app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')

def get_db_connection(db_name):
    """Cria e reutiliza uma conexão com o banco de dados."""
    if 'db' not in g or g.db_name != db_name:
        g.db_name = db_name
        g.db = sqlite3.connect(db_name)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Fecha a conexão com o banco de dados ao final da requisição."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def sanitize_npj_for_folder(npj_string: str) -> str:
    """Converte um NPJ (ex: '2024/123-000') em um nome de pasta válido (ex: '2024_123_000')."""
    if not isinstance(npj_string, str):
        return ""
    return npj_string.replace("/", "_").replace("-", "_")

def get_files_for_npj(sanitized_npj: str) -> list:
    """Encontra os arquivos baixados para um NPJ específico."""
    if not sanitized_npj:
        return []
    
    npj_folder_path = os.path.join(DOWNLOAD_FOLDER, sanitized_npj)
    if os.path.isdir(npj_folder_path):
        try:
            return os.listdir(npj_folder_path)
        except OSError:
            return []
    return []

@app.route('/')
def index():
    """Página inicial que lista todos os arquivos .db no diretório."""
    database_files = [f for f in glob.glob("*.db")]
    return render_template('index.html', databases=database_files)

@app.route('/view/<db_name>')
def view_database(db_name):
    """Exibe o conteúdo das tabelas e os arquivos associados a cada NPJ."""
    conn = get_db_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    tables_data = []
    for table_name in tables:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        headers = []
        augmented_rows = []

        if rows:
            headers = rows[0].keys()
            for row in rows:
                # Converte a linha do DB para um dicionário mutável
                row_dict = dict(row)
                
                # Se a linha tiver uma coluna NPJ, procura por arquivos
                if 'NPJ' in row_dict:
                    sanitized_npj = sanitize_npj_for_folder(row_dict['NPJ'])
                    row_dict['sanitized_npj'] = sanitized_npj
                    row_dict['files'] = get_files_for_npj(sanitized_npj)
                
                augmented_rows.append(row_dict)
            
        tables_data.append({
            'name': table_name,
            'headers': headers,
            'rows': augmented_rows # Usa as linhas com os dados dos arquivos
        })

    return render_template('view_table.html', db_name=db_name, tables_data=tables_data)

# --- NOVA ROTA PARA DOWNLOADS ---
@app.route('/downloads/<path:subpath>')
def download_file(subpath):
    """Serve um arquivo da pasta de downloads de forma segura."""
    # Garante que o caminho é seguro e está dentro da pasta de downloads
    if not os.path.exists(os.path.join(DOWNLOAD_FOLDER, subpath)):
        abort(404) # Retorna "Não encontrado" se o arquivo não existir
        
    return send_from_directory(DOWNLOAD_FOLDER, subpath, as_attachment=True)


if __name__ == '__main__':
    print("Servidor iniciado! Acesse http://127.0.0.1:5000 no seu navegador.")
    app.run(debug=True)