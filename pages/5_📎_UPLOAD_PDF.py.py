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
# FUNÇÕES DE APOIO
# ==========================================================
def carregar_documentos():
    conn = conectar_db()
    query = "SELECT id, titulo, autores, ano, arquivo_pdf FROM bibliografia ORDER BY titulo ASC"
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao ler banco: {e}")
        return pd.DataFrame()
    finally:
        if hasattr(conn, "close"):
            conn.close()

# ==========================================================
# TÍTULO E CARREGAMENTO
# ==========================================================
st.title("📎 Gerenciamento de PDFs")

df_docs = carregar_documentos()

if df_docs.empty:
    st.warning("Nenhum documento cadastrado.")
    st.stop()

# ==========================================================
# SELEÇÃO
# ==========================================================
documentos_dict = {
    f"{row['id']} - {row['titulo']}": row["id"]
    for _, row in df_docs.iterrows()
}

selecionado_label = st.selectbox("Selecione o documento:", list(documentos_dict.keys()))
doc_id = documentos_dict[selecionado_label]
documento = df_docs[df_docs["id"] == doc_id].iloc[0]

# Dados do Doc
col1, col2, col3 = st.columns(3)
with col1: st.info(f"**Título**\n\n{documento['titulo']}")
with col2: st.info(f"**Autores**\n\n{documento['autores']}")
with col3: st.info(f"**Ano**\n\n{documento['ano']}")

st.markdown("---")

# ==========================================================
# STATUS DO PDF (CORREÇÃO DO ERRO AQUI)
# ==========================================================
st.subheader("📄 Status do PDF")

arquivo_atual = documento["arquivo_pdf"]

# Verifica se o valor não é nulo, não é NaN e não é vazio
if arquivo_atual and not pd.isna(arquivo_atual) and str(arquivo_atual).strip() != "":
    
    # CONVERSÃO EXPLÍCITA PARA STRING PARA EVITAR TYPEERROR
    nome_arquivo_str = str(arquivo_atual)
    caminho_pdf = PDF_DIR / nome_arquivo_str
    
    if caminho_pdf.exists():
        st.success(f"Arquivo associado: {nome_arquivo_str}")
        
        c1, c2 = st.columns(2)
        with c1:
            with open(caminho_pdf, "rb") as f:
                st.download_button("⬇️ Baixar PDF", f, file_name=nome_arquivo_str, use_container_width=True)
        with c2:
            if st.button("🗑️ Remover PDF Atual", use_container_width=True):
                try:
                    caminho_pdf.unlink() # Deleta arquivo físico
                    conn = conectar_db()
                    with conn.connect() as connection:
                        connection.execute(text("UPDATE bibliografia SET arquivo_pdf = NULL WHERE id = :id"), {"id": int(doc_id)})
                        if hasattr(connection, 'commit'): connection.commit()
                    st.success("Removido com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao remover: {e}")
    else:
        st.warning(f"O banco cita o arquivo '{nome_arquivo_str}', mas ele não existe na pasta pdfs.")
else:
    st.info("Nenhum PDF associado.")

# ==========================================================
# UPLOAD
# ==========================================================
st.markdown("---")
st.subheader("📤 Novo Upload")
uploaded_file = st.file_uploader("Selecione o arquivo", type=["pdf"])

if st.button("💾 Salvar PDF", use_container_width=True):
    if uploaded_file:
        try:
            # Novo nome único
            novo_nome = f"{uuid.uuid4()}.pdf"
            
            # Salvar físico
            with open(PDF_DIR / novo_nome, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Remover antigo se existir (com segurança)
            if arquivo_atual and not pd.isna(arquivo_atual):
                antigo = PDF_DIR / str(arquivo_atual)
                if antigo.exists():
                    antigo.unlink()
            
            # Atualizar Banco
            conn = conectar_db()
            sql = text("UPDATE bibliografia SET arquivo_pdf = :nome WHERE id = :id")
            params = {"nome": novo_nome, "id": int(doc_id)}
            
            # Execução compatível com Engine ou Connection
            if hasattr(conn, 'connect'):
                with conn.connect() as connection:
                    connection.execute(sql, params)
                    if hasattr(connection, 'commit'): connection.commit()
            else:
                conn.execute(sql, params)
                if hasattr(conn, 'commit'): conn.commit()

            st.success("✅ Upload realizado!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro no upload: {e}")
    else:
        st.warning("Selecione um arquivo PDF primeiro.")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU")
