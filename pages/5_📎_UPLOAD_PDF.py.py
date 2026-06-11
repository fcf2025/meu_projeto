import streamlit as st
import pandas as pd
from pathlib import Path
import uuid
from sqlalchemy import text
from utils.database import conectar_db

# ==========================================================
# 1. AJUSTE DE CAMINHO (MUITO IMPORTANTE)
# ==========================================================
# Se seus PDFs estão na mesma pasta que os scripts (como mostra sua imagem 1)
# mude o caminho abaixo. 
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs" 
PDF_DIR.mkdir(exist_ok=True)

def executar_sql(query, params):
    conn = conectar_db()
    try:
        if hasattr(conn, 'connect'):
            with conn.connect() as connection:
                with connection.begin():
                    connection.execute(text(query), params)
        else:
            conn.execute(text(query), params)
            if hasattr(conn, 'commit'): conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro SQL: {e}")
        return False
    finally:
        if hasattr(conn, 'close'): conn.close()

def carregar_documentos():
    conn = conectar_db()
    try:
        return pd.read_sql("SELECT id, titulo, arquivo_pdf FROM bibliografia ORDER BY titulo DESC", conn)
    finally:
        if hasattr(conn, 'close'): conn.close()

# ==========================================================
# UI INTERFACE
# ==========================================================
st.title("📎 Atualizar PDF")

df_docs = carregar_documentos()
documentos_dict = {f"{r['id']} - {r['titulo']}": r['id'] for _, r in df_docs.iterrows()}
selecionado = st.selectbox("Selecione o documento:", list(documentos_dict.keys()))
doc_id = documentos_dict[selecionado]

# Pega os dados exatos do banco para o ID selecionado
doc_info = df_docs[df_docs['id'] == doc_id].iloc[0]
arquivo_no_banco = doc_info['arquivo_pdf']

st.markdown("---")

# ==========================================================
# DIAGNÓSTICO DO PROBLEMA
# ==========================================================
with st.expander("🔍 Diagnóstico de Sincronização"):
    st.write(f"**ID no Banco:** {doc_id}")
    st.write(f"**Valor na coluna 'arquivo_pdf':** `{arquivo_no_banco}`")
    st.write(f"**Pasta onde o sistema procura:** `{PDF_DIR.absolute()}`")
    
    arquivos_na_pasta = list(PDF_DIR.glob("*.pdf"))
    st.write(f"**Total de PDFs encontrados na pasta:** {len(arquivos_na_pasta)}")

# ==========================================================
# LÓGICA DE EXIBIÇÃO (O QUE ESTAVA DANDO ERRO)
# ==========================================================
# Verificamos se o banco tem algo escrito E se esse arquivo existe no disco
if arquivo_no_banco and str(arquivo_no_banco).strip() != "" and not pd.isna(arquivo_no_banco):
    caminho_pdf = PDF_DIR / str(arquivo_no_banco)
    
    if caminho_pdf.exists():
        st.success(f"✅ PDF vinculado e encontrado: `{arquivo_no_banco}`")
        with open(caminho_pdf, "rb") as f:
            st.download_button("⬇️ Baixar PDF Atual", f, file_name=str(arquivo_no_banco))
    else:
        st.error(f"⚠️ O banco diz que o arquivo é `{arquivo_no_banco}`, mas ele NÃO está na pasta!")
        st.info("Faça um novo upload abaixo para corrigir.")
else:
    # ESTA É A MENSAGEM QUE ESTAVA APARECENDO PARA VOCÊ
    st.warning("ℹ️ PDF atual: Nenhum arquivo anexado no banco de dados para este documento.")

st.markdown("---")
st.subheader("Selecionar novo PDF (substituirá o atual)")
uploaded_file = st.file_uploader("Upload", type=["pdf"], label_visibility="collapsed")

if st.button("💾 Salvar Alterações", use_container_width=True):
    if uploaded_file:
        # 1. Criar novo nome
        novo_nome = f"{uuid.uuid4()}.pdf"
        caminho_destino = PDF_DIR / novo_nome
        
        # 2. Salvar arquivo físico
        with open(caminho_destino, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 3. Atualizar Banco
        sucesso = executar_sql(
            "UPDATE bibliografia SET arquivo_pdf = :nome WHERE id = :id",
            {"nome": novo_nome, "id": int(doc_id)}
        )
        
        if sucesso:
            st.success("✅ Banco de dados atualizado e arquivo salvo!")
            st.rerun()
    else:
        st.error("Selecione um arquivo PDF primeiro.")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU • Sistema de Gestão de Arquivos")
