# ==========================================================
# utils/database.py
# Funções de acesso ao banco de dados
# Biblioteca Digital DMAPLU
# ==========================================================

import pandas as pd
import streamlit as st

from sqlalchemy import create_engine, text

# ==========================================================
# CONEXÃO
# ==========================================================

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

def conectar_db():
    return engine.connect()

# ==========================================================
# CRIAR TABELA
# ==========================================================

def criar_tabela():
    with conectar_db() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bibliografia (
                id SERIAL PRIMARY KEY,
                titulo TEXT,
                autores TEXT,
                ano INTEGER,
                tema TEXT,
                pais TEXT
            )
        """))
        conn.commit()

    conn.close()

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

    parametros = {}

    # ======================================================
    # TEXTO
    # ======================================================

    if texto:

        query += """
        AND (
            titulo ILIKE :termo
            OR autores ILIKE :termo
            OR resumo ILIKE :termo
            OR palavras_chave ILIKE :termo
        )
        """

        parametros["termo"] = f"%{texto}%"

    # ======================================================
    # TEMA
    # ======================================================

    if tema:

        query += " AND tema = :tema "

        parametros["tema"] = tema

    # ======================================================
    # ANO
    # ======================================================

    if ano:

        query += " AND ano = :ano "

        parametros["ano"] = ano

    # ======================================================
    # PAÍS
    # ======================================================

    if pais:

        query += " AND pais = :pais "

        parametros["pais"] = pais

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    query += " ORDER BY ano DESC, titulo ASC "

    df = pd.read_sql(
        text(query),
        conn,
        params=parametros
    )

    conn.close()

    return df

# ==========================================================
# INSERIR DOCUMENTO
# ==========================================================

def inserir_documento(
    titulo,
    autores,
    ano,
    instituicao,
    tipo_documento,
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

    conn = conectar_db()

    query = text("""

    INSERT INTO bibliografia (

        titulo,
        autores,
        ano,
        instituicao,
        tipo_documento,
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

    VALUES (

        :titulo,
        :autores,
        :ano,
        :instituicao,
        :tipo_documento,
        :pais,
        :idioma,
        :tema,
        :subtema,
        :resumo,
        :palavras_chave,
        :doi,
        :link,
        :arquivo_pdf,
        :categoria,
        :metodo,
        :regiao,
        :observacoes

    )

    """)

    conn.execute(query, {

        "titulo": titulo,
        "autores": autores,
        "ano": ano,
        "instituicao": instituicao,
        "tipo_documento": tipo_documento,
        "pais": pais,
        "idioma": idioma,
        "tema": tema,
        "subtema": subtema,
        "resumo": resumo,
        "palavras_chave": palavras_chave,
        "doi": doi,
        "link": link,
        "arquivo_pdf": arquivo_pdf,
        "categoria": categoria,
        "metodo": metodo,
        "regiao": regiao,
        "observacoes": observacoes

    })

    conn.commit()

    conn.close()


# ==========================================================
# LISTAR DOCUMENTO 
# ==========================================================
def listar_documentos():

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

    df = pd.read_sql(query, conn)

    conn.close()

    return df
# ==========================================================
# OBTER DOCUMENTO POR ID
# ==========================================================

def obter_documento(doc_id):

    conn = conectar_db()

    query = text("""
    SELECT *
    FROM bibliografia
    WHERE id = :id
    """)

    df = pd.read_sql(
        query,
        conn,
        params={"id": doc_id}
    )

    conn.close()

    if len(df) > 0:
        return df.iloc[0]

    return None

# ==========================================================
# EXCLUIR DOCUMENTO
# ==========================================================

def excluir_documento(doc_id):

    conn = conectar_db()

    query = text("""
    DELETE FROM bibliografia
    WHERE id = :id
    """)

    conn.execute(query, {"id": doc_id})

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
    instituicao,
    tipo_documento,
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

    conn = conectar_db()

    query = text("""

    UPDATE bibliografia
    SET
        titulo = :titulo,
        autores = :autores,
        ano = :ano,
        instituicao = :instituicao,
        tipo_documento = :tipo_documento,
        pais = :pais,
        idioma = :idioma,
        tema = :tema,
        subtema = :subtema,
        resumo = :resumo,
        palavras_chave = :palavras_chave,
        doi = :doi,
        link = :link,
        arquivo_pdf = :arquivo_pdf,
        categoria = :categoria,
        metodo = :metodo,
        regiao = :regiao,
        observacoes = :observacoes
    WHERE id = :doc_id

    """)

    conn.execute(query, {

        "titulo": titulo,
        "autores": autores,
        "ano": ano,
        "instituicao": instituicao,
        "tipo_documento": tipo_documento,
        "pais": pais,
        "idioma": idioma,
        "tema": tema,
        "subtema": subtema,
        "resumo": resumo,
        "palavras_chave": palavras_chave,
        "doi": doi,
        "link": link,
        "arquivo_pdf": arquivo_pdf,
        "categoria": categoria,
        "metodo": metodo,
        "regiao": regiao,
        "observacoes": observacoes,
        "doc_id": doc_id

    })

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

    stats["total_documentos"] = pd.read_sql(
        query_total,
        conn
    )["total"][0]

    # Total de temas
    query_temas = """
    SELECT COUNT(DISTINCT tema) AS total
    FROM bibliografia
    """

    stats["total_temas"] = pd.read_sql(
        query_temas,
        conn
    )["total"][0]

    # Total de países
    query_paises = """
    SELECT COUNT(DISTINCT pais) AS total
    FROM bibliografia
    """

    stats["total_paises"] = pd.read_sql(
        query_paises,
        conn
    )["total"][0]

    conn.close()

    return stats
