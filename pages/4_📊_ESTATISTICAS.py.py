# ==========================================================
# pages/estatisticas.py
# Estatísticas do Acervo
# Biblioteca Digital DMAPLU
# ==========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# IMPORTS
# ==========================================================

from utils.database import (
    conectar_db,
    estatisticas_gerais
)

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Estatísticas",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# TÍTULO
# ==========================================================

st.title("📊 Estatísticas do Acervo")

st.markdown("""
Painel estatístico da Biblioteca Digital DMAPLU.
""")

st.markdown("---")

# ==========================================================
# ESTATÍSTICAS GERAIS
# ==========================================================

stats = estatisticas_gerais()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total de Documentos",
        stats["total_documentos"]
    )

with col2:

    st.metric(
        "Total de Temas",
        stats["total_temas"]
    )

with col3:

    st.metric(
        "Total de Países",
        stats["total_paises"]
    )

st.markdown("---")

# ==========================================================
# CONEXÃO
# ==========================================================

conn = conectar_db()

# ==========================================================
# DOCUMENTOS POR TEMA
# ==========================================================

st.subheader("📚 Documentos por Tema")

query_tema = """
SELECT
    tema,
    COUNT(*) AS quantidade
FROM bibliografia
WHERE tema IS NOT NULL
AND tema <> ''
GROUP BY tema
ORDER BY quantidade DESC
"""

df_tema = pd.read_sql_query(
    query_tema,
    conn
)

if len(df_tema) > 0:

    col1, col2 = st.columns([1, 2])

    with col1:

        st.dataframe(
            df_tema,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.bar(
            df_tema["tema"],
            df_tema["quantidade"]
        )

        ax.set_xlabel("Tema")
        ax.set_ylabel("Quantidade")
        ax.set_title("Documentos por Tema")

        plt.xticks(
            rotation=45,
            ha="right"
        )

        st.pyplot(fig)

else:

    st.info(
        "Nenhum dado disponível."
    )

st.markdown("---")

# ==========================================================
# DOCUMENTOS POR ANO
# ==========================================================

st.subheader("📅 Evolução Temporal")

query_ano = """
SELECT
    ano,
    COUNT(*) AS quantidade
FROM bibliografia
WHERE ano IS NOT NULL
GROUP BY ano
ORDER BY ano
"""

df_ano = pd.read_sql_query(
    query_ano,
    conn
)

if len(df_ano) > 0:

    col1, col2 = st.columns([1, 2])

    with col1:

        st.dataframe(
            df_ano,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.plot(
            df_ano["ano"],
            df_ano["quantidade"],
            marker="o"
        )

        ax.set_xlabel("Ano")
        ax.set_ylabel("Quantidade")
        ax.set_title("Evolução Temporal do Acervo")

        st.pyplot(fig)

else:

    st.info(
        "Nenhum dado disponível."
    )

st.markdown("---")

# ==========================================================
# DOCUMENTOS POR PAÍS
# ==========================================================

st.subheader("🌎 Documentos por País")

query_pais = """
SELECT
    pais,
    COUNT(*) AS quantidade
FROM bibliografia
WHERE pais IS NOT NULL
AND pais <> ''
GROUP BY pais
ORDER BY quantidade DESC
LIMIT 15
"""

df_pais = pd.read_sql_query(
    query_pais,
    conn
)

if len(df_pais) > 0:

    col1, col2 = st.columns([1, 2])

    with col1:

        st.dataframe(
            df_pais,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.barh(
            df_pais["pais"],
            df_pais["quantidade"]
        )

        ax.set_xlabel("Quantidade")
        ax.set_ylabel("País")
        ax.set_title("Documentos por País")

        st.pyplot(fig)

else:

    st.info(
        "Nenhum dado disponível."
    )

st.markdown("---")

# ==========================================================
# TIPOS DE DOCUMENTOS
# ==========================================================

st.subheader("📄 Tipos de Documento")

query_tipo = """
SELECT
    tipo_documento,
    COUNT(*) AS quantidade
FROM bibliografia
WHERE tipo_documento IS NOT NULL
AND tipo_documento <> ''
GROUP BY tipo_documento
ORDER BY quantidade DESC
"""

df_tipo = pd.read_sql_query(
    query_tipo,
    conn
)

if len(df_tipo) > 0:

    col1, col2 = st.columns([1, 2])

    with col1:

        st.dataframe(
            df_tipo,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        fig, ax = plt.subplots(
            figsize=(7, 7)
        )

        ax.pie(
            df_tipo["quantidade"],
            labels=df_tipo["tipo_documento"],
            autopct="%1.1f%%"
        )

        ax.set_title(
            "Distribuição por Tipo de Documento"
        )

        st.pyplot(fig)

else:

    st.info(
        "Nenhum dado disponível."
    )

st.markdown("---")

# ==========================================================
# AUTORES MAIS FREQUENTES
# ==========================================================

st.subheader("👨‍🔬 Principais Autores")

query_autores = """
SELECT
    autores,
    COUNT(*) AS quantidade
FROM bibliografia
WHERE autores IS NOT NULL
AND autores <> ''
GROUP BY autores
ORDER BY quantidade DESC
LIMIT 15
"""

df_autores = pd.read_sql_query(
    query_autores,
    conn
)

if len(df_autores) > 0:

    st.dataframe(
        df_autores,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Nenhum dado disponível."
    )

# ==========================================================
# FECHAR CONEXÃO
# ==========================================================

conn.close()

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption(
    "Biblioteca Digital DMAPLU • Painel Estatístico"
)