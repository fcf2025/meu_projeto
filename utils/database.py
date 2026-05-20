# ==========================================================
# utils/database.py
# Funções de acesso ao banco de dados
# Biblioteca Digital DMAPLU
# ==========================================================

import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================================
# CAMINHOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "bibliografia.db"

# ==========================================================
# CONEXÃO
# ==========================================================

def conectar_db():
    """
    Cria conexão com o banco SQLite
    """

    conn = sqlite3.connect(DB_PATH)

    return conn
def verificar_documento_existente(titulo, autores, ano):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM documentos
        WHERE titulo = ? AND (autores = ? OR ano = ?)
        LIMIT 1
    """, (titulo, autores, ano))

    existe = cursor.fetchone() is not None
    conn.close()
    return existe
# ==========================================================
# INSERIR DOCUMENTO
# ==========================================================

def inserir_documento(
    titulo,
    autores,
    ano,
    tipo_documento,
    instituicao,
    pais,
    idioma,
    tema,
    subtema,
    resumo,
    palavras_chave,
    doi,
    link,
    arquivo_pdf,
    categoria,
    metodo,
    regiao,
    observacoes
):
    """
    Insere um novo documento no banco
    """

    conn = conectar_db()

    cursor = conn.cursor()

    query = """
    INSERT INTO bibliografia (

        titulo,
        autores,
        ano,

        tipo_documento,
        instituicao,
        pais,
        idioma,

        tema,
        subtema,

        resumo,
        palavras_chave,

        doi,
        link,

        arquivo_pdf,

        categoria,
        metodo,
        regiao,

        observacoes

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    valores = (
        titulo,
        autores,
        ano,

        tipo_documento,
        instituicao,
        pais,
        idioma,

        tema,
        subtema,

        resumo,
        palavras_chave,

        doi,
        link,

        arquivo_pdf,

        categoria,
        metodo,
        regiao,

        observacoes
    )

    cursor.execute(query, valores)

    conn.commit()

    conn.close()

# ==========================================================
# LISTAR DOCUMENTOS
# ==========================================================

def listar_documentos():
    """
    Retorna todos os documentos
    """

    conn = conectar_db()

    query = """
    SELECT
        id,
        titulo,
        autores,
        ano,
        tema,
        pais,
        tipo_documento
    FROM bibliografia
    ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

# ==========================================================
# BUSCA GERAL
# ==========================================================

def buscar_documentos(
    texto="",
    tema="",
    ano=None,
    pais=""
):
    """
    Busca documentos com filtros
    """

    conn = conectar_db()

    query = """
    SELECT
        id,
        titulo,
        autores,
        ano,
        tema,
        pais,
        tipo_documento,
        resumo,
        link
    FROM bibliografia
    WHERE 1=1
    """

    parametros = []

    # ======================================================
    # TEXTO
    # ======================================================

    if texto:

        query += """
        AND (
            titulo LIKE ?
            OR autores LIKE ?
            OR resumo LIKE ?
            OR palavras_chave LIKE ?
        )
        """

        termo = f"%{texto}%"

        parametros.extend([
            termo,
            termo,
            termo,
            termo
        ])

    # ======================================================
    # TEMA
    # ======================================================

    if tema:

        query += " AND tema = ? "

        parametros.append(tema)

    # ======================================================
    # ANO
    # ======================================================

    if ano:

        query += " AND ano = ? "

        parametros.append(ano)

    # ======================================================
    # PAÍS
    # ======================================================

    if pais:

        query += " AND pais = ? "

        parametros.append(pais)

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    query += " ORDER BY ano DESC, titulo ASC "

    df = pd.read_sql_query(
        query,
        conn,
        params=parametros
    )

    conn.close()

    return df

# ==========================================================
# OBTER DOCUMENTO POR ID
# ==========================================================

def obter_documento(doc_id):
    """
    Retorna documento específico
    """

    conn = conectar_db()

    query = """
    SELECT *
    FROM bibliografia
    WHERE id = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=[doc_id]
    )

    conn.close()

    if len(df) > 0:
        return df.iloc[0]

    return None

# ==========================================================
# EXCLUIR DOCUMENTO
# ==========================================================

def excluir_documento(doc_id):
    """
    Remove documento do banco
    """

    conn = conectar_db()

    cursor = conn.cursor()

    query = """
    DELETE FROM bibliografia
    WHERE id = ?
    """

    cursor.execute(query, (doc_id,))

    conn.commit()

    conn.close()

# ==========================================================
# ATUALIZAR DOCUMENTO
# ==========================================================

def atualizar_documento(
    doc_id,
    titulo,
    autores,
    ano,
    tipo_documento,
    instituicao,
    pais,
    idioma,
    tema,
    subtema,
    resumo,
    palavras_chave,
    doi,
    link,
    arquivo_pdf,
    categoria,
    metodo,
    regiao,
    observacoes
):
    """
    Atualiza documento existente
    """

    conn = conectar_db()

    cursor = conn.cursor()

    query = """
    UPDATE bibliografia
    SET

        titulo = ?,
        autores = ?,
        ano = ?,

        tipo_documento = ?,
        instituicao = ?,
        pais = ?,
        idioma = ?,

        tema = ?,
        subtema = ?,

        resumo = ?,
        palavras_chave = ?,

        doi = ?,
        link = ?,

        arquivo_pdf = ?,

        categoria = ?,
        metodo = ?,
        regiao = ?,

        observacoes = ?

    WHERE id = ?
    """

    valores = (
        titulo,
        autores,
        ano,

        tipo_documento,
        instituicao,
        pais,
        idioma,

        tema,
        subtema,

        resumo,
        palavras_chave,

        doi,
        link,

        arquivo_pdf,

        categoria,
        metodo,
        regiao,

        observacoes,

        doc_id
    )

    cursor.execute(query, valores)

    conn.commit()

    conn.close()

# ==========================================================
# ESTATÍSTICAS
# ==========================================================

def estatisticas_gerais():
    """
    Retorna estatísticas gerais do acervo
    """

    conn = conectar_db()

    stats = {}

    # Total de documentos
    query_total = """
    SELECT COUNT(*) AS total
    FROM bibliografia
    """

    stats["total_documentos"] = pd.read_sql_query(
        query_total,
        conn
    )["total"][0]

    # Total de temas
    query_temas = """
    SELECT COUNT(DISTINCT tema) AS total
    FROM bibliografia
    """

    stats["total_temas"] = pd.read_sql_query(
        query_temas,
        conn
    )["total"][0]

    # Total de países
    query_paises = """
    SELECT COUNT(DISTINCT pais) AS total
    FROM bibliografia
    """

    stats["total_paises"] = pd.read_sql_query(
        query_paises,
        conn
    )["total"][0]

    conn.close()

    return stats
