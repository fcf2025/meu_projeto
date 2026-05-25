# ==========================================================
# ==========================================================
# pages/upload_pdf.py
# ==========================================================

import streamlit as st
import pandas as pd
from pathlib import Path
import uuid
from sqlalchemy import text

# ==========================================================
# IMPORTS E CONFIGURAÇÃO
# ==========================================================
from utils.database import conectar_db

st.set_page_config(
    page_title="Upload de PDFs",
    page_icon="📎",
    layout="wide"
)

# ==========================================================
# CAMINHOS E DIRETÓRIOS
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# FUNÇÕES DE APOIO CORRIGIDAS
# ==========================================================
def carregar_documentos():
    """Carrega a lista de documentos tratando a conexão adequadamente."""
    conn = conectar_db()
    query = "SELECT id, titulo, autores, ano, arquivo_pdf FROM bibliografia ORDER BY titulo ASC"
    
    try:
        # Tenta carregar usando pandas diretamente com a conexão
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao ler banco de dados: {e}")
        return pd.DataFrame()
    finally:
        # Se a conexão tiver o método close (boa prática)
        if hasattr(conn, "close"):
            conn.close()

# ==========================================================
# TÍTULO E CARREGAMENTO DE DADOS
# ==========================================================
st.title("📎 Gerenciamento de PDFs")

df_docs = carregar_documentos()

if df_docs.empty:
    st.warning("Nenhum documento cadastrado ou erro na conexão.")
    st.stop()

st.markdown("---")

# ==========================================================
# SELEÇÃO DE DOCUMENTO
# ==========================================================
st.subheader("📚 Selecionar Documento")

documentos_dict = {
    f"{row['id']} - {row['titulo']}": row["id"]
    for _, row in df_docs.iterrows()
}

selecionado_label = st.selectbox(
    "Selecione o documento:",
    list(documentos_dict.keys())
)

doc_id = documentos_dict[selecionado_label]
documento = df_docs[df_docs["id"] == doc_id].iloc[0]

# Exibição
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Título**\n\n{documento['titulo']}")
with col2:
    st.info(f"**Autores**\n\n{documento['autores']}")
with col3:
    st.info(f"**Ano**\n\n{documento['ano']}")

st.markdown("---")

# ==========================================================
# STATUS E REMOÇÃO
# ==========================================================
st.subheader("📄 Status do PDF")

arquivo_atual = documento["arquivo_pdf"]

if arquivo_atual and str(arquivo_atual).strip() != "":
    caminho_pdf = PDF_DIR / arquivo_atual
    if caminho_pdf.exists():
        st.success(f"Arquivo associado: {arquivo_atual}")
        
        col_d, col_r = st.columns(2)
        with col_d:
            with open(caminho_pdf, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name=arquivo_atual, use_container_width=True)
        
        with col_r:
            if st.button("🗑️ Remover PDF Atual", use_container_width=True):
                caminho_pdf.unlink() # Deleta arquivo
                conn = conectar_db()
                # Ajuste de execução para diferentes tipos de conexão
                try:
                    if hasattr(conn, 'execute'): # SQLAlchemy
                        with conn.begin() if hasattr(conn, 'begin') else conn:
                            conn.execute(text("UPDATE bibliografia SET arquivo_pdf = NULL WHERE id = :id"), {"id": int(doc_id)})
                    st.success("Removido!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar banco: {e}")
    else:
        st.warning("Arquivo registrado no banco mas não encontrado na pasta 'pdfs'.")
else:
    st.info("Nenhum PDF associado.")

# ==========================================================
# NOVO UPLOAD
# ==========================================================
st.subheader("📤 Novo Upload")
uploaded_file = st.file_uploader("Selecione o PDF", type=["pdf"])

if st.button("💾 Salvar PDF", use_container_width=True):
    if uploaded_file:
        try:
            # Gerar nome e salvar
            novo_nome = f"{uuid.uuid4()}.pdf"
            with open(PDF_DIR / novo_nome, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Remover antigo se existir
            if arquivo_atual:
                antigo = PDF_DIR / str(arquivo_atual)
                if antigo.exists(): antigo.unlink()
            
            # Atualizar Banco
            conn = conectar_db()
            # Lógica compatível com SQLAlchemy Engine ou Connection
            sql = text("UPDATE bibliografia SET arquivo_pdf = :nome WHERE id = :id")
            params = {"nome": novo_nome, "id": int(doc_id)}
            
            # Verifica se é SQLAlchemy Engine ou conexão pura
            if hasattr(conn, 'connect'): # É um Engine
                with conn.connect() as connection:
                    with connection.begin():
                        connection.execute(sql, params)
            else: # Já é uma Conexão
                conn.execute(sql, params)
                if hasattr(conn, 'commit'): conn.commit()
            
            st.success("✅ PDF salvo com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Selecione um arquivo.")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU")
