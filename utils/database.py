# ==========================================================
# utils/database.py
# Funções de acesso ao banco de dados
# Biblioteca Digital DMAPLU
# ==========================================================

import pandas as pd
import streamlit as st

from sqlalchemy import create_engine, text
# ==========================================================
# CAMINHOS
# ==========================================================

# ==========================================================
# CONEXÃO
# ==========================================================

DATABASE_URL = st.secrets["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

def conectar_db():
    return engine.connect()

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
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
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

    df = pd.read_sql(query, conn)

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
            titulo LIKE %s
            OR autores LIKE %s
            OR resumo LIKE %s
            OR palavras_chave LIKE %s
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

        query += " AND tema = %s "

        parametros.append(tema)

    # ======================================================
    # ANO
    # ======================================================

    if ano:

        query += " AND ano = %s "

        parametros.append(ano)

    # ======================================================
    # PAÍS
    # ======================================================

    if pais:

        query += " AND pais = %s "

        parametros.append(pais)

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    query += " ORDER BY ano DESC, titulo ASC "

    df = pd.read_sql(
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
    WHERE id = %s
    """

    df = pd.read_sql(
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
    WHERE id = %s
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
    """
    Atualiza documento existente
    """

    conn = conectar_db()

    cursor = conn.cursor()

    query = """
    UPDATE bibliografia
    SET

        titulo = %s,
        autores = %s,
        ano = %s,
        instituicao = %s,
        tipo_documento = %s,
       
        pais = %s,
        idioma = %s,

        tema = %s,
        subtema = %s,

        resumo = %s,
        palavras_chave = %s,

        doi = %s,
        link = %s,

        arquivo_pdf = %s,

        categoria = %s,
        metodo = %s,
        regiao = %s,

        observacoes = %s

    WHERE id = %s
    """

    valores = (
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
