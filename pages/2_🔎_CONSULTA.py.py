# ==========================================================
# pages/consulta.py
# Consulta Bibliográfica
# Biblioteca Digital DMAPU
# ==========================================================

import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================================
# IMPORTS
# ==========================================================

from utils.database import (
    buscar_documentos,
    excluir_documento,
    obter_documento
)

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Consulta Bibliográfica",
    page_icon="🔎",
    layout="wide"
)

# ==========================================================
# CAMINHOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "pdfs"

# ==========================================================
# TÍTULO
# ==========================================================

st.title("🔎 Consulta Bibliográfica")

st.markdown("""
Pesquise documentos da Biblioteca Digital DMAPU.
""")

st.markdown("---")

# ==========================================================
# FILTROS
# ==========================================================

st.subheader("Filtros de Pesquisa")

col1, col2, col3, col4 = st.columns(4)

with col1:

    texto_busca = st.text_input(
        "Texto livre",
        placeholder="Título, autor, resumo..."
    )

with col2:

    tema = st.selectbox(
        "Tema",
        ["", "Financiamento", "Tarifa (Taxas de drenagem)", "Custos (Operacionais e de Implantação)","Taxas","Regulação e Governança","Soluções Baseadas na Natureza (SbN) e Infraestrutura Verde",
                "Planejamento Urbano e Uso do Solo","Sustentabilidade e Mudanças Climáticas","Tecnologias de Monitoramento", "Cidades Inteligentes (Smart Cities)",                    
                "Investimentos em DMAPU","Cidades Inteligentes","Manejo de Águas Pluviais Urbanas (MAPU)",
                "Saneamento Básico","Direitos Fundamentais","Drenagem Urbana",
                "Recursos Hídricos","Outro"]
    )

with col3:

    ano = st.number_input(
        "Ano",
        min_value=1900,
        max_value=2100,
        value=None,
        step=1
    )

with col4:

    pais = st.text_input(
        "País"
    )

# ==========================================================
# BOTÃO BUSCA
# ==========================================================

buscar = st.button(
    "🔍 Buscar",
    use_container_width=True
)

# ==========================================================
# RESULTADOS
# ==========================================================

if buscar:

    try:

        df = buscar_documentos(
            texto=texto_busca,
            tema=tema,
            ano=ano,
            pais=pais
        )

        st.markdown("---")

        st.subheader(
            f"📚 Resultados encontrados: {len(df)}"
        )

        # ==================================================
        # SEM RESULTADOS
        # ==================================================

        if len(df) == 0:

            st.warning(
                "Nenhum documento encontrado."
            )

        else:

            # ==============================================
            # TABELA
            # ==============================================

            st.dataframe(
                df[
                    [
                        "id",
                        "titulo",
                        "autores",
                        "ano",
                        "tema",
                        "pais",
                        "tipo_documento"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            # ==============================================
            # DETALHAMENTO
            # ==============================================

            st.subheader("📄 Visualizar Documento")

            lista_ids = df["id"].tolist()

            doc_id = st.selectbox(
                "Selecione o ID",
                lista_ids
            )

            documento = obter_documento(doc_id)

            if documento is not None:

                st.markdown("---")

                # ==========================================
                # CABEÇALHO
                # ==========================================

                st.markdown(
                    f"## {documento['titulo']}"
                )

                # ==========================================
                # INFORMAÇÕES
                # ==========================================

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.info(
                        f"**Autores:**\n\n{documento['autores']}"
                    )

                with col2:
                    st.info(
                        f"**Ano:**\n\n{documento['ano']}"
                    )

                with col3:
                    st.info(
                        f"**Tema:**\n\n{documento['tema']}"
                    )

                # ==========================================
                # RESUMO
                # ==========================================

                st.markdown("### 📘 Resumo")

                st.write(documento["resumo"])

                # ==========================================
                # PALAVRAS-CHAVE
                # ==========================================

                st.markdown("### 🏷️ Palavras-chave")

                st.write(documento["palavras_chave"])

                # ==========================================
                # METADADOS
                # ==========================================

                st.markdown("### ℹ️ Informações")

                meta1, meta2 = st.columns(2)

                with meta1:

                    st.write(
                        f"**Tipo:** {documento['tipo_documento']}"
                    )

                    st.write(
                        f"**Instituição:** {documento['instituicao']}"
                    )

                    st.write(
                        f"**País:** {documento['pais']}"
                    )

                    st.write(
                        f"**Idioma:** {documento['idioma']}"
                    )

                with meta2:

                    st.write(
                        f"**Subtema:** {documento['subtema']}"
                    )

                    st.write(
                        f"**Categoria:** {documento['categoria']}"
                    )

                    st.write(
                        f"**Método:** {documento['metodo']}"
                    )

                    st.write(
                        f"**Região:** {documento['regiao']}"
                    )

                # ==========================================
                # DOI E LINK
                # ==========================================

                st.markdown("### 🌐 Links")

                if documento["doi"]:
                    st.write(f"**DOI:** {documento['doi']}")

                if documento["link"]:
                    st.markdown(
                        f"[Acessar Documento]({documento['link']})"
                    )

                # ==========================================
                # PDF
                # ==========================================

                st.markdown("### 📎 PDF")

                if documento["arquivo_pdf"]:

                    caminho_pdf = (
                        PDF_DIR /
                        documento["arquivo_pdf"]
                    )

                    if caminho_pdf.exists():

                        with open(
                            caminho_pdf,
                            "rb"
                        ) as pdf_file:

                            st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_file,
                                file_name=documento["arquivo_pdf"],
                                mime="application/pdf",
                                use_container_width=True
                            )

                    else:

                        st.warning(
                            "Arquivo PDF não encontrado."
                        )

                else:

                    st.info(
                        "Documento sem PDF anexado."
                    )

                # ==========================================
                # OBSERVAÇÕES
                # ==========================================

                if documento["observacoes"]:

                    st.markdown("### 📝 Observações")

                    st.write(documento["observacoes"])

                # ==========================================
                # EXCLUSÃO
                # ==========================================

                st.markdown("---")

                st.subheader("⚠️ Área Administrativa")

                excluir = st.button(
                    "🗑️ Excluir Documento",
                    use_container_width=True
                )

                if excluir:

                    excluir_documento(doc_id)

                    st.success(
                        "Documento excluído com sucesso."
                    )

                    st.rerun()

    except Exception as e:

        st.error(
            f"Erro na consulta: {e}"
        )

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption(
    "Biblioteca Digital DMAPU • Consulta Bibliográfica"
)
