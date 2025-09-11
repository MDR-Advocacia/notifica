# arquivo: database.py
import sqlite3
import json
from pathlib import Path

DB_NOME = "rpa.db"
TABELA_NOTIFICACOES = "notificacoes_processos"
TABELA_LOGS = "logs_execucao"

def inicializar_banco():
    """
    Garante que o banco de dados e as tabelas necessárias existam,
    realizando migrações de schema se necessário para adicionar colunas faltantes.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        
        # 1. Garante que a tabela de notificações exista com a estrutura base
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABELA_NOTIFICACOES} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NPJ TEXT NOT NULL,
            tipo_notificacao TEXT NOT NULL,
            data_notificacao TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 2. Lógica de Migração de Schema: Adiciona colunas se estiverem faltando
        cursor.execute(f"PRAGMA table_info({TABELA_NOTIFICACOES})")
        colunas_existentes = [row[1] for row in cursor.fetchall()]
        
        colunas_desejadas = {
            "adverso_principal": "TEXT",
            "andamentos": "TEXT",
            "documentos": "TEXT"
        }

        for coluna, tipo in colunas_desejadas.items():
            if coluna not in colunas_existentes:
                print(f"INFO: Migrando schema. Adicionando coluna '{coluna}'...")
                cursor.execute(f"ALTER TABLE {TABELA_NOTIFICACOES} ADD COLUMN {coluna} {tipo}")
        
        # 3. Garante que a tabela de logs exista
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABELA_LOGS} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            duracao_total REAL,
            tempo_medio_npj REAL,
            notificacoes_salvas INTEGER,
            andamentos_capturados INTEGER,
            documentos_baixados INTEGER,
            npjs_sucesso INTEGER,
            npjs_falha TEXT
        )
        """)
        
        conn.commit()
        print(f"✅ Banco de dados '{DB_NOME}' e tabelas verificados/migrados com sucesso.")
    except sqlite3.Error as e:
        print(f"❌ ERRO ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

# --- O RESTANTE DAS FUNÇÕES PERMANECE O MESMO ---

def salvar_notificacoes(lista_notificacoes: list[dict]):
    """Salva uma lista de novas notificações no banco de dados."""
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
    """Busca NPJs únicos que tenham notificações com status 'Pendente'."""
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
    """Busca os últimos NPJs processados para rodar em modo de teste."""
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
    """Atualiza todas as notificações de um NPJ com os dados processados."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()

        andamentos_json = json.dumps(andamentos, ensure_ascii=False)
        documentos_json = json.dumps(documentos, ensure_ascii=False)
        novo_status = "Processado em Teste" if is_test else "Processado"
        
        # Define a cláusula WHERE baseada no modo de execução
        where_clause = "status = 'Pendente'"
        params = (andamentos_json, documentos_json, novo_status, npj)

        if is_test:
             # Em modo de teste, atualiza apenas a notificação mais recente do NPJ para não bagunçar o histórico
             where_clause = f"id = (SELECT id FROM {TABELA_NOTIFICACOES} WHERE NPJ = ? ORDER BY data_criacao DESC LIMIT 1)"
             params = (andamentos_json, documentos_json, novo_status, npj)

        query = f"UPDATE {TABELA_NOTIFICACOES} SET andamentos = ?, documentos = ?, status = ? WHERE NPJ = ? AND {where_clause}"
        
        cursor.execute(query, params)
        conn.commit()
        print(f"    - ✅ Registros do NPJ {npj} atualizados para '{novo_status}'.")

    except sqlite3.Error as e:
        print(f"❌ ERRO ao atualizar registro do NPJ {npj}: {e}")
    finally:
        if conn:
            conn.close()


def marcar_como_erro(npj: str):
    """Marca todas as notificações pendentes de um NPJ como 'Erro'."""
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

def salvar_log_execucao(log_data: dict):
    """Salva um registro de log no banco de dados."""
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
        print(f"❌ ERRO ao salvar log de execução: {e}")
    finally:
        if conn:
            conn.close()

def arquivar_notificacao_por_npj(npj: str):
    """Atualiza todas as notificações de um NPJ para 'Arquivado'."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        query = f"UPDATE {TABELA_NOTIFICACOES} SET status = 'Arquivado' WHERE NPJ = ? AND status IN ('Processado', 'Processado em Teste')"
        cursor.execute(query, (npj,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ ERRO ao arquivar notificações para o NPJ {npj}: {e}")
    finally:
        if conn:
            conn.close()

def desarquivar_notificacao_por_npj(npj: str):
    """Atualiza todas as notificações arquivadas de um NPJ de volta para 'Processado'."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        query = f"UPDATE {TABELA_NOTIFICACOES} SET status = 'Processado' WHERE NPJ = ? AND status = 'Arquivado'"
        cursor.execute(query, (npj,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ ERRO ao desarquivar notificações para o NPJ {npj}: {e}")
    finally:
        if conn:
            conn.close()

def arquivar_notificacoes_em_lote_por_npj(lista_npjs: list[str]):
    """Atualiza o status de uma lista de NPJs para 'Arquivado'."""
    if not lista_npjs:
        return 0
    conn = None
    try:
        conn = sqlite3.connect(DB_NOME)
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(lista_npjs))
        query = f"""
        UPDATE {TABELA_NOTIFICACOES}
        SET status = 'Arquivado'
        WHERE NPJ IN ({placeholders})
        AND status IN ('Processado', 'Processado em Teste')
        """
        cursor.execute(query, lista_npjs)
        conn.commit()
        registros_afetados = cursor.rowcount
        print(f"✅ {registros_afetados} notificações (de {len(lista_npjs)} NPJs) arquivadas em lote.")
        return registros_afetados
    except sqlite3.Error as e:
        print(f"❌ ERRO ao arquivar notificações em lote por NPJ: {e}")
        return 0
    finally:
        if conn:
            conn.close()

