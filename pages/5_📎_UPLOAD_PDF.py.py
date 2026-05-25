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
# FUNÇÃO DE EXECUÇÃO SQL (RESOLVE O ERRO DE CONEXÃO)
# ==========================================================
def executar_sql(query, params):
    """Executa SQL tratando se a conexão é Engine ou Connection."""
    conn = conectar_db()
    try:
        # Se for um Engine (tem o método connect)
        if hasattr(conn, 'connect'):
            with conn.connect() as connection:
                with connection.begin():
                    connection.execute(text(query), params)
        # Se já for uma Conexão direta
        else:
            conn.execute(text(query), params)
            if hasattr(conn, 'commit'):
                conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro no banco de dados: {e}")
        return False
    finally:
        if hasattr(conn, 'close'):
            conn.close()

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

# Dados do Doc em colunas
col1, col2, col3 = st.columns(3)
with col1: st.info(f"**Título**\n\n{documento['titulo']}")
with col2: st.info(f"**Autores**\n\n{documento['autores']}")
with col3: st.info(f"**Ano**\n\n{documento['ano']}")

st.markdown("---")

# ==========================================================
# STATUS DO PDF
# ==========================================================
st.subheader("📄 Status do PDF")

arquivo_atual = documento["arquivo_pdf"]

# Verificação robusta de valor nulo
if arquivo_atual and not pd.isna(arquivo_atual) and str(arquivo_atual).strip() != "":
    
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
                # 1. Tenta atualizar o banco primeiro
                sucesso = executar_sql(
                    "UPDATE bibliografia SET arquivo_pdf = NULL WHERE id = :id", 
                    {"id": int(doc_id)}
                )
                if sucesso:
                    # 2. Se atualizou o banco, remove o arquivo físico
                    if caminho_pdf.exists():
                        caminho_pdf.unlink()
                    st.success("Removido com sucesso!")
                    st.rerun()
    else:
        st.warning(f"O registro existe no banco ({nome_arquivo_str}), mas o arquivo físico não foi encontrado.")
        if st.button("Limpar registro inexistente no banco"):
            executar_sql("UPDATE bibliografia SET arquivo_pdf = NULL WHERE id = :id", {"id": int(doc_id)})
            st.rerun()
else:
    st.info("Nenhum PDF associado a este documento.")

# ==========================================================
# UPLOAD
# ==========================================================
st.markdown("---")
st.subheader("📤 Novo Upload")
uploaded_file = st.file_uploader("Selecione o arquivo PDF", type=["pdf"])

if st.button("💾 Salvar PDF", use_container_width=True):
    if uploaded_file:
        try:
            # 1. Gerar nome único
            novo_nome = f"{uuid.uuid4()}.pdf"
            
            # 2. Salvar arquivo físico
            with open(PDF_DIR / novo_nome, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 3. Atualizar Banco de Dados
            sucesso = executar_sql(
                "UPDATE bibliografia SET arquivo_pdf = :nome WHERE id = :id",
                {"nome": novo_nome, "id": int(doc_id)}
            )
            
            if sucesso:
                # 4. Remover arquivo físico antigo se ele existia
                if arquivo_atual and not pd.isna(arquivo_atual):
                    antigo = PDF_DIR / str(arquivo_atual)
                    if antigo.exists():
                        antigo.unlink()
                
                st.success("✅ Upload realizado com sucesso!")
                st.rerun()
            else:
                # Se falhou o banco, remove o arquivo que acabou de subir para não sujar a pasta
                (PDF_DIR / novo_nome).unlink()

        except Exception as e:
            st.error(f"Erro no processo de upload: {e}")
    else:
        st.warning("Selecione um arquivo PDF antes de salvar.")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU • Sistema de Gestão de Arquivos")
