# ==========================================================
# pages/upload_pdf.py
# Upload e Gerenciamento de PDFs
# Biblioteca Digital DMAPLU
# ==========================================================

import streamlit as st
import pandas as pd
from pathlib import Path
import uuid
import shutil

# ==========================================================
# IMPORTS
# ==========================================================

from utils.database import (
    conectar_db
)

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Upload de PDFs",
    page_icon="📎",
    layout="wide"
)

# ==========================================================
# CAMINHOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "pdfs"

PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# TÍTULO
# ==========================================================

st.title("📎 Gerenciamento de PDFs")

st.markdown("""
Associe arquivos PDF aos documentos cadastrados
na Biblioteca Digital DMAPLU.
""")

st.markdown("---")

# ==========================================================
# CARREGAR DOCUMENTOS
# ==========================================================

conn = conectar_db()

query = """
SELECT
    id,
    titulo,
    autores,
    ano,
    arquivo_pdf
FROM bibliografia
ORDER BY titulo
"""

df_docs = pd.read_sql_query(
    query,
    conn
)

conn.close()

# ==========================================================
# VERIFICA DOCUMENTOS
# ==========================================================

if len(df_docs) == 0:

    st.warning(
        "Nenhum documento cadastrado."
    )

    st.stop()

# ==========================================================
# SELEÇÃO
# ==========================================================

st.subheader("📚 Selecionar Documento")

documentos_dict = {
    f"{row['id']} - {row['titulo']}": row["id"]
    for _, row in df_docs.iterrows()
}

selecionado = st.selectbox(
    "Documento",
    list(documentos_dict.keys())
)

doc_id = documentos_dict[selecionado]

# ==========================================================
# DADOS DOCUMENTO
# ==========================================================

documento = df_docs[
    df_docs["id"] == doc_id
].iloc[0]

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        f"**Título**\n\n{documento['titulo']}"
    )

with col2:

    st.info(
        f"**Autores**\n\n{documento['autores']}"
    )

with col3:

    st.info(
        f"**Ano**\n\n{documento['ano']}"
    )

# ==========================================================
# STATUS PDF
# ==========================================================

st.subheader("📄 Status do PDF")

arquivo_atual = documento["arquivo_pdf"]

if arquivo_atual:

    caminho_pdf = PDF_DIR / arquivo_atual

    if caminho_pdf.exists():

        st.success(
            "PDF associado ao documento."
        )

        # ==================================================
        # DOWNLOAD
        # ==================================================

        with open(caminho_pdf, "rb") as file:

            st.download_button(
                label="⬇️ Download PDF Atual",
                data=file,
                file_name=arquivo_atual,
                mime="application/pdf",
                use_container_width=True
            )

        # ==================================================
        # REMOVER PDF
        # ==================================================

        remover = st.button(
            "🗑️ Remover PDF",
            use_container_width=True
        )

        if remover:

            try:

                # ==========================================
                # REMOVE ARQUIVO
                # ==========================================

                caminho_pdf.unlink()

                # ==========================================
                # REMOVE REFERÊNCIA
                # ==========================================

                conn = conectar_db()

                cursor = conn.cursor()

                cursor.execute("""
                UPDATE bibliografia
                SET arquivo_pdf = ''
                WHERE id = ?
                """, (doc_id,))

                conn.commit()

                conn.close()

                st.success(
                    "PDF removido com sucesso."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Erro ao remover PDF: {e}"
                )

    else:

        st.warning(
            "Arquivo PDF não encontrado no diretório."
        )

else:

    st.info(
        "Nenhum PDF associado."
    )

st.markdown("---")

# ==========================================================
# NOVO UPLOAD
# ==========================================================

st.subheader("📤 Novo Upload")

uploaded_file = st.file_uploader(
    "Selecione um arquivo PDF",
    type=["pdf"]
)

# ==========================================================
# BOTÃO SALVAR
# ==========================================================

salvar = st.button(
    "💾 Salvar PDF",
    use_container_width=True
)

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if salvar:

    if uploaded_file is None:

        st.warning(
            "Selecione um PDF."
        )

    else:

        try:

            # ==============================================
            # EXTENSÃO
            # ==============================================

            extensao = uploaded_file.name.split(".")[-1]

            # ==============================================
            # NOME ÚNICO
            # ==============================================

            novo_nome = (
                f"{uuid.uuid4()}.{extensao}"
            )

            caminho_destino = PDF_DIR / novo_nome

            # ==============================================
            # SALVAR PDF
            # ==============================================

            with open(
                caminho_destino,
                "wb"
            ) as f:

                shutil.copyfileobj(
                    uploaded_file,
                    f
                )

            # ==============================================
            # REMOVE PDF ANTIGO
            # ==============================================

            if arquivo_atual:

                antigo = PDF_DIR / arquivo_atual

                if antigo.exists():

                    antigo.unlink()

            # ==============================================
            # ATUALIZA BANCO
            # ==============================================

            conn = conectar_db()

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE bibliografia
            SET arquivo_pdf = ?
            WHERE id = ?
            """, (novo_nome, doc_id))

            conn.commit()

            conn.close()

            st.success(
                "PDF enviado com sucesso."
            )

            st.rerun()

        except Exception as e:

            st.error(
                f"Erro no upload: {e}"
            )

# ==========================================================
# LISTAGEM PDFs com opção de remoção
# ==========================================================

st.markdown("---")
st.subheader("📚 PDFs no Sistema")

arquivos_pdf = list(PDF_DIR.glob("*.pdf"))

if len(arquivos_pdf) > 0:
    lista_pdfs = []
    for arq in arquivos_pdf:
        tamanho_mb = arq.stat().st_size / (1024 * 1024)
        lista_pdfs.append({
            "Arquivo": arq.name,
            "Tamanho (MB)": round(tamanho_mb, 2)
        })

    df_pdfs = pd.DataFrame(lista_pdfs)

    st.dataframe(df_pdfs, use_container_width=True, hide_index=True)

    # Seleção de arquivo para remover
    arquivo_remover = st.selectbox(
        "Selecione um PDF para remover",
        [arq.name for arq in arquivos_pdf]
    )

    if st.button("🗑️ Remover PDF Selecionado", use_container_width=True):
        try:
            caminho_remover = PDF_DIR / arquivo_remover
            caminho_remover.unlink()
    
            # Opcional: remover referência no banco
            conn = conectar_db()
            conn.execute("""
                UPDATE bibliografia
                SET arquivo_pdf = ''
                WHERE arquivo_pdf = ?
            """, (arquivo_remover,))
            conn.commit()
            conn.close()
    
            st.success(f"PDF {arquivo_remover} removido com sucesso.")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao remover PDF: {e}")


else:
    st.info("Nenhum PDF armazenado.")
# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption(
    "Biblioteca Digital DMAPLU • Gerenciamento de PDFs"
)
