# arquivo: database.py
import sqlite3
import json
from pathlib import Path

DB_NOME = "rpa.db"
TABELA_NOTIFICACOES = "notificacoes_processos"
TABELA_LOGS = "logs_execucao"

def inicializar_banco():
    # ... (código existente sem alterações)
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        
        schema_notificacoes = f"""
        CREATE TABLE IF NOT EXISTS {TABELA_NOTIFICACOES} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NPJ TEXT NOT NULL,
            tipo_notificacao TEXT NOT NULL,
            adverso_principal TEXT,
            data_notificacao TEXT NOT NULL,
            andamentos TEXT,
            documentos TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(schema_notificacoes)

        schema_logs = f"""
        CREATE TABLE IF NOT EXISTS {TABELA_LOGS} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            duracao_total TEXT,
            tempo_medio_npj TEXT,
            notificacoes_salvas INTEGER,
            andamentos_capturados INTEGER,
            documentos_baixados INTEGER,
            npjs_sucesso INTEGER,
            npjs_falha TEXT
        )
        """
        cursor.execute(schema_logs)
        
        conn.commit()
        print(f"✅ Banco de dados '{DB_NOME}' e tabelas verificados/criados.")
    except sqlite3.Error as e:
        print(f"❌ ERRO ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def arquivar_notificacao(item_id: int):
    """Atualiza o status de uma notificação específica para 'Arquivado'."""
    # ... (código existente sem alterações)
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        query = f"UPDATE {TABELA_NOTIFICACOES} SET status = 'Arquivado' WHERE id = ?"
        cursor.execute(query, (item_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ ERRO ao arquivar notificação ID {item_id}: {e}")
    finally:
        if conn:
            conn.close()

def desarquivar_notificacao(item_id: int):
    """Atualiza o status de uma notificação 'Arquivado' de volta para 'Processado'."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        # Volta para 'Processado' pois era o estado original antes de arquivar.
        query = f"UPDATE {TABELA_NOTIFICACOES} SET status = 'Processado' WHERE id = ?"
        cursor.execute(query, (item_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ ERRO ao desarquivar notificação ID {item_id}: {e}")
    finally:
        if conn:
            conn.close()

# (O restante do arquivo database.py continua o mesmo)
# ...
def obter_notificacoes_paginadas(filtros: dict, pagina: int, por_pagina: int) -> list[dict]:
    # ...
    offset = (pagina - 1) * por_pagina
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        base_query = f"SELECT * FROM {TABELA_NOTIFICACOES}"
        where_clauses = []
        params = []

        if filtros.get("status"):
            where_clauses.append("status = ?")
            params.append(filtros["status"])
        if filtros.get("tipo_notificacao"):
            where_clauses.append("tipo_notificacao = ?")
            params.append(filtros["tipo_notificacao"])

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)
            
        ordenar_por = filtros.get("ordenar_por", "data_criacao")
        ordem = "ASC" if filtros.get("ordem") == "asc" else "DESC"
        base_query += f" ORDER BY {ordenar_por} {ordem}"

        base_query += " LIMIT ? OFFSET ?"
        params.extend([por_pagina, offset])
        
        cursor.execute(base_query, params)
        return [dict(row) for row in cursor.fetchall()]
        
    except sqlite3.Error as e:
        print(f"❌ ERRO ao buscar notificações: {e}")
        return []
    finally:
        if conn:
            conn.close()

def contar_notificacoes(filtros: dict) -> int:
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        
        base_query = f"SELECT COUNT(id) FROM {TABELA_NOTIFICACOES}"
        where_clauses = []
        params = []

        if filtros.get("status"):
            where_clauses.append("status = ?")
            params.append(filtros["status"])
        if filtros.get("tipo_notificacao"):
            where_clauses.append("tipo_notificacao = ?")
            params.append(filtros["tipo_notificacao"])

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(base_query, params)
        return cursor.fetchone()[0]

    except sqlite3.Error as e:
        print(f"❌ ERRO ao contar notificações: {e}")
        return 0
    finally:
        if conn:
            conn.close()

def obter_tipos_notificacao_unicos() -> list[str]:
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        query = f"SELECT DISTINCT tipo_notificacao FROM {TABELA_NOTIFICACOES} ORDER BY tipo_notificacao"
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"❌ ERRO ao buscar tipos de notificação: {e}")
        return []
    finally:
        if conn:
            conn.close()
            
def salvar_log_execucao(log_data: dict):
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        
        colunas = ', '.join(log_data.keys())
        placeholders = ', '.join(['?'] * len(log_data))
        
        query = f"INSERT INTO {TABELA_LOGS} ({colunas}) VALUES ({placeholders})"
        
        cursor.execute(query, list(log_data.values()))
        conn.commit()
        print("✅ Resumo da execução salvo no log.")
    except sqlite3.Error as e:
        print(f"❌ ERRO ao salvar log de execução no banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def salvar_notificacoes(lista_notificacoes: list[dict]):
    # ...
    if not lista_notificacoes:
        return
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        
        query = f"""
        INSERT INTO {TABELA_NOTIFICACOES} 
        (NPJ, tipo_notificacao, adverso_principal, data_notificacao) 
        VALUES (?, ?, ?, ?)
        """
        
        registros_a_inserir = [
            (item['NPJ'], item['tipo_notificacao'], item.get('adverso_principal'), item['data_notificacao'])
            for item in lista_notificacoes
        ]
        
        cursor.executemany(query, registros_a_inserir)
        registros_inseridos = cursor.rowcount
        conn.commit()
        print(f"✅ {registros_inseridos} novas notificações salvas para processamento.")

    except sqlite3.Error as e:
        print(f"❌ ERRO ao salvar notificações: {e}")
    finally:
        if conn:
            conn.close()

def obter_npjs_pendentes() -> list[dict]:
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        query = f"""
        SELECT NPJ, GROUP_CONCAT(DISTINCT data_notificacao) as datas_notificacao
        FROM {TABELA_NOTIFICACOES}
        WHERE status = 'Pendente'
        GROUP BY NPJ
        """
        cursor.execute(query)
        pendentes = [dict(row) for row in cursor.fetchall()]
        print(f"🔎 Encontrados {len(pendentes)} NPJs únicos com notificações pendentes.")
        return pendentes
    except sqlite3.Error as e:
        print(f"❌ ERRO ao obter NPJs pendentes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obter_npjs_para_teste(limite: int = 5) -> list[dict]:
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = f"""
        SELECT NPJ, GROUP_CONCAT(DISTINCT data_notificacao) as datas_notificacao
        FROM {TABELA_NOTIFICACOES}
        WHERE status = 'Processado' OR status = 'Processado em Teste'
        GROUP BY NPJ
        ORDER BY MAX(data_criacao) DESC
        LIMIT ?
        """
        cursor.execute(query, (limite,))
        testes = [dict(row) for row in cursor.fetchall()]
        if testes:
            print(f"🔎 Nenhum item pendente. Modo de teste ativado com {len(testes)} NPJ(s).")
        return testes
    except sqlite3.Error as e:
        print(f"❌ ERRO ao obter NPJs para teste: {e}")
        return []
    finally:
        if conn:
            conn.close()

def atualizar_registro_processado(npj: str, andamentos: list[dict], documentos: list[dict], is_test: bool = False):
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()

        andamentos_json = json.dumps(andamentos, ensure_ascii=False)
        documentos_json = json.dumps(documentos, ensure_ascii=False)
        
        novo_status = "Processado em Teste" if is_test else "Processado"
        
        where_clause = "status = 'Pendente'"
        if is_test:
            where_clause = f"id IN (SELECT id FROM {TABELA_NOTIFICACOES} WHERE NPJ = ? ORDER BY data_criacao DESC LIMIT 1)"

        query = f"""
        UPDATE {TABELA_NOTIFICACOES}
        SET 
            andamentos = ?,
            documentos = ?,
            status = ?
        WHERE NPJ = ? AND ({where_clause})
        """
        
        params = (
            andamentos_json,
            documentos_json,
            novo_status,
            npj
        )
        if is_test:
            params += (npj,)

        cursor.execute(query, params)
        conn.commit()
        print(f"    - ✅ Registros do NPJ {npj} atualizados para '{novo_status}'.")

    except sqlite3.Error as e:
        print(f"❌ ERRO ao atualizar registro do NPJ {npj}: {e}")
    finally:
        if conn:
            conn.close()

def marcar_como_erro(npj: str):
    # ...
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        query = f"UPDATE {TABELA_NOTIFICACOES} SET status = 'Erro' WHERE NPJ = ? AND status = 'Pendente'"
        cursor.execute(query, (npj,))
        conn.commit()
        print(f"    - ⚠️ Registros do NPJ {npj} marcados como 'Erro'.")
    except sqlite3.Error as e:
        print(f"❌ ERRO ao marcar NPJ {npj} como erro: {e}")
    finally:
        if conn:
            conn.close()

