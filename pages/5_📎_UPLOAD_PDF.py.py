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
    """Carrega a lista de documentos do banco de dados."""
    engine = conectar_db()
    query = "SELECT id, titulo, autores, ano, arquivo_pdf FROM bibliografia ORDER BY titulo ASC"
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

# ==========================================================
# TÍTULO E CARREGAMENTO DE DADOS
# ==========================================================
st.title("📎 Gerenciamento de PDFs")
st.markdown("Associe arquivos PDF aos documentos cadastrados na Biblioteca Digital DMAPLU.")

df_docs = carregar_documentos()

if df_docs.empty:
    st.warning("Nenhum documento cadastrado no banco de dados.")
    st.stop()

st.markdown("---")

# ==========================================================
# SELEÇÃO DE DOCUMENTO
# ==========================================================
st.subheader("📚 Selecionar Documento")

# Criar dicionário para o selectbox
documentos_dict = {
    f"{row['id']} - {row['titulo']}": row["id"]
    for _, row in df_docs.iterrows()
}

selecionado_label = st.selectbox(
    "Selecione o documento para gerenciar o arquivo:",
    list(documentos_dict.keys())
)

doc_id = documentos_dict[selecionado_label]
documento = df_docs[df_docs["id"] == doc_id].iloc[0]

# Exibição de Detalhes
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Título**\n\n{documento['titulo']}")
with col2:
    st.info(f"**Autores**\n\n{documento['autores']}")
with col3:
    st.info(f"**Ano**\n\n{documento['ano']}")

st.markdown("---")

# ==========================================================
# GESTÃO DO ARQUIVO ATUAL
# ==========================================================
st.subheader("📄 Status do PDF")

arquivo_atual = documento["arquivo_pdf"]
pdf_existe_no_disco = False

if arquivo_atual:
    caminho_pdf = PDF_DIR / arquivo_atual
    if caminho_pdf.exists():
        pdf_existe_no_disco = True
        st.success(f"PDF encontrado: {arquivo_atual}")
        
        col_down, col_rem = st.columns(2)
        
        with col_down:
            with open(caminho_pdf, "rb") as file:
                st.download_button(
                    label="⬇️ Download PDF Atual",
                    data=file,
                    file_name=f"documento_{doc_id}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        
        with col_rem:
            if st.button("🗑️ Remover PDF Atual", use_container_width=True):
                try:
                    # Remove arquivo físico
                    caminho_pdf.unlink()
                    
                    # Atualiza Banco
                    engine = conectar_db()
                    with engine.begin() as conn:
                        conn.execute(
                            text("UPDATE bibliografia SET arquivo_pdf = NULL WHERE id = :id"),
                            {"id": int(doc_id)}
                        )
                    st.success("PDF removido com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao remover: {e}")
    else:
        st.error("O banco indica um arquivo, mas ele não foi encontrado na pasta 'pdfs'.")
else:
    st.info("Nenhum PDF associado a este documento.")

# ==========================================================
# UPLOAD / SUBSTITUIÇÃO
# ==========================================================
st.markdown("---")
st.subheader("📤 Upload de Novo Arquivo")

uploaded_file = st.file_uploader(
    "Selecione um arquivo PDF (Máx 50MB)",
    type=["pdf"],
    key="uploader_principal"
)

if st.button("💾 Salvar / Substituir PDF", use_container_width=True):
    if uploaded_file is not None:
        try:
            # 1. Gerar novo nome único
            extensao = "pdf"
            novo_nome = f"{uuid.uuid4()}.{extensao}"
            caminho_destino = PDF_DIR / novo_nome

            # 2. Salvar novo arquivo
            with open(caminho_destino, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # 3. Remover arquivo antigo do disco se existir
            if arquivo_atual:
                antigo = PDF_DIR / arquivo_atual
                if antigo.exists():
                    antigo.unlink()

            # 4. Atualizar banco de dados
            engine = conectar_db()
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE bibliografia SET arquivo_pdf = :arquivo WHERE id = :id"),
                    {"arquivo": novo_nome, "id": int(doc_id)}
                )

            st.success("✅ Upload concluído com sucesso!")
            st.rerun()

        except Exception as e:
            st.error(f"Erro no processamento do upload: {e}")
    else:
        st.warning("Por favor, selecione um arquivo antes de clicar em salvar.")

# ==========================================================
# LISTAGEM GERAL DO SISTEMA (Manutenção)
# ==========================================================
st.markdown("---")
with st.expander("🔍 Visualizar todos os PDFs no servidor"):
    arquivos_pdf = list(PDF_DIR.glob("*.pdf"))

    if arquivos_pdf:
        lista_pdfs = []
        for arq in arquivos_pdf:
            tamanho_mb = arq.stat().st_size / (1024 * 1024)
            lista_pdfs.append({
                "Arquivo": arq.name,
                "Tamanho (MB)": round(tamanho_mb, 2)
            })

        df_listagem = pd.DataFrame(lista_pdfs)
        st.dataframe(df_listagem, use_container_width=True, hide_index=True)
        
        # Opção de limpeza manual
        arquivo_avulso = st.selectbox("Remover arquivo específico do disco:", [arq.name for arq in arquivos_pdf])
        if st.button("🗑️ Apagar do Servidor"):
            try:
                (PDF_DIR / arquivo_avulso).unlink()
                # Limpar referências no banco que usem esse nome
                engine = conectar_db()
                with engine.begin() as conn:
                    conn.execute(
                        text("UPDATE bibliografia SET arquivo_pdf = NULL WHERE arquivo_pdf = :nome"),
                        {"nome": arquivo_avulso}
                    )
                st.success("Arquivo apagado!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro: {e}")
    else:
        st.info("A pasta de PDFs está vazia.")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU • Gerenciamento de PDFs v2.0")
