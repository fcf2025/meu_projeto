# ==========================================================
# pages/cadastro.py
# Cadastro de Bibliografia - Biblioteca Digital DMAPU
# ==========================================================

import streamlit as st
from pathlib import Path
import uuid
import pandas as pd
from sqlalchemy import text

# ==========================================================
# IMPORTAÇÕES DE BANCO (CORRIGIDO)
# ==========================================================
from utils.database import conectar_db, inserir_documento

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Cadastro de Bibliografia",
    page_icon="📝",
    layout="wide"
)

# ==========================================================
# FUNÇÃO DE CRÍTICA
# ==========================================================
def verificar_duplicidade(titulo, autores):
    """Verifica se já existe título e autor idênticos no banco."""
    conn = conectar_db()
    query = text("""
        SELECT id FROM bibliografia 
        WHERE LOWER(TRIM(titulo)) = LOWER(TRIM(:t)) 
        AND LOWER(TRIM(autores)) = LOWER(TRIM(:a))
    """)
    try:
        if hasattr(conn, 'connect'):
            with conn.connect() as connection:
                res = connection.execute(query, {"t": titulo, "a": autores}).fetchone()
        else:
            res = conn.execute(query, {"t": titulo, "a": autores}).fetchone()
        return res is not None
    finally:
        if hasattr(conn, 'close'): 
            conn.close()

# ==========================================================
# CAMINHO PDFs
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# TÍTULO
# ==========================================================
st.title("📝 Cadastro de Referências Bibliográficas")
st.markdown("Preencha os campos abaixo para inserir um novo documento na Biblioteca Digital DMAPLU.")
st.markdown("---")

# ==========================================================
# FORMULÁRIO
# ==========================================================
with st.form("form_cadastro", clear_on_submit=True):

    # LINHA 1
    col1, col2 = st.columns([3, 1])
    with col1:
        titulo = st.text_input("Título *")
    with col2:
        # Criamos uma lista de anos de 2030 até 1900
        lista_anos = list(range(2030, 1899, -1))
        
        ano = st.selectbox(
            "Ano",
            options=lista_anos,
            index=5 # Isso define o ano 2025 como padrão (posições: 2030=0, 2029=1...)
        )

    # LINHA 2
    autores = st.text_input("Autor(es)")
    instituicao = st.text_input("Instituição do Autor/Afiliação")
    
    # LINHA 3
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_documento = st.selectbox("Tipo de Documento", ["", "Artigo", "Livro", "Capítulo", "Dissertação", "Tese", "Monografia", "TCC", "Outros"])
    with col2:
        pais = st.selectbox("País", ["", "Brasil", "Argentina", "Chile", "Estados Unidos", "Portugal", "Outro"])
    with col3:
        idioma = st.selectbox("Idioma", ["", "Português", "Inglês", "Espanhol", "Francês", "Outro"])

    # LINHA 5
    col1, col2 = st.columns(2)
    with col1:
        tema = st.selectbox("Tema", ["", "Planejamento e Planos de Drenagem", "Infraestrutura verde", "Controle de cheias", "Outro"])
    with col2:
        subtema = st.selectbox("Subtema", ["", "Planejamento urbano integrado", "Bacias de detenção", "Educação ambiental", "Outro"])

    palavras_chave = st.text_input("Palavras-chave")
    resumo = st.text_area("Resumo", height=200)

    # LINHA 8
    col1, col2 = st.columns(2)
    with col1:
        doi = st.selectbox("Veículo de Publicação", ["Revista", "Journal", "Conferência", "Livro", "Site", "Outro"])
    with col2:
        link = st.text_input("Link")

    # LINHA 9
    col1, col2, col3 = st.columns(3)
    with col1:
        categoria = st.selectbox("Categoria", ["", "Infraestrutura estrutural", "Gestão", "Planejamento urbano", "Outro"])
    with col2:
        metodo = st.selectbox("Método", ["", "Pesquisa de Campo", "Modelagem Matemática", "Análise Documental", "Outro"])
    with col3:
        regiao = st.selectbox("Região", ["", "Brasil", "América Latina", "Europa", "Global", "Outro"])

    observacoes = st.text_area("Observações", height=100)

    st.markdown("### 📎 Upload de PDF")
    uploaded_file = st.file_uploader("Selecione um PDF", type=["pdf"])

    submitted = st.form_submit_button("💾 Salvar Documento", use_container_width=True)

# ==========================================================
# PROCESSAMENTO (REVISADO E ÚNICO)
# ==========================================================
if submitted:

    # 1. Validação de Título
    if titulo.strip() == "":
        st.error("O título é obrigatório.")
    
    # 2. Crítica de Duplicidade
    elif verificar_duplicidade(titulo, autores):
        st.warning(f"⚠️ Já existe um registro cadastrado com este título e autor(es).")
        st.info("Verifique se o documento já não foi inserido anteriormente.")

    # 3. Processamento de Salvamento
    else:
        try:
            nome_pdf = ""
            if uploaded_file is not None:
                extensao = uploaded_file.name.split(".")[-1]
                nome_pdf = f"{uuid.uuid4()}.{extensao}"
                caminho_pdf = PDF_DIR / nome_pdf
                with open(caminho_pdf, "wb") as f:
                    f.write(uploaded_file.read())

            inserir_documento(
                titulo=titulo,
                autores=autores,
                ano=ano,
                tipo_documento=tipo_documento,
                instituicao=instituicao,
                pais=pais,
                idioma=idioma,
                tema=tema,
                subtema=subtema,
                resumo=resumo,
                palavras_chave=palavras_chave,
                doi=doi,
                link=link,
                arquivo_pdf=nome_pdf,
                categoria=categoria,
                metodo=metodo,
                regiao=regiao,
                observacoes=observacoes
            )

            st.success("Cadastro realizado com sucesso!")
            st.balloons()
            st.toast("Dados atualizados!")

        except Exception as e:
            st.error(f"Erro ao salvar documento: {e}")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU • Cadastro de Bibliografia")
