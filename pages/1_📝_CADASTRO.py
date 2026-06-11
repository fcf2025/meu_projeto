import streamlit as st
import uuid
import time
import json
from pathlib import Path
from sqlalchemy import text
from PyPDF2 import PdfReader
from openai import OpenAI

# ==========================================================
# CONFIGURAÇÃO E CHAVES
# ==========================================================
DATABASE_URL = st.secrets["DATABASE_URL"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

from utils.database import conectar_db, inserir_documento

st.set_page_config(page_title="Cadastro de Bibliografia", page_icon="📝", layout="wide")

# Inicializar Session State para evitar erros de valor ausente
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "titulo": "", "autores": "", "ano": 2025, "pais": "Brasil", 
        "resumo": "", "palavras_chave": "", "instituicao": "", "idioma": "Português"
    }

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# FUNÇÕES DE APOIO
# ==========================================================
def extrair_texto_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        texto = ""
        # Lemos as primeiras 4 páginas
        for i in range(min(len(reader.pages), 4)):
            page_text = reader.pages[i].extract_text()
            if page_text:
                texto += page_text
        return texto
    except Exception as e:
        st.error(f"Erro ao ler PDF: {e}")
        return ""

def sugerir_metadados(texto_pdf):
    prompt = f"""
    Extraia os metadados do seguinte texto. Responda APENAS em formato JSON:
    {{
      "titulo": "...", "autores": "...", "ano": 2024, "pais": "...", 
      "resumo": "...", "palavras_chave": "...", "instituicao": "...", "idioma": "..."
    }}
    Texto: {texto_pdf[:4000]}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Erro na IA: {e}")
        return None

def verificar_duplicidade(titulo, autores):
    conn = conectar_db()
    query = text("SELECT id FROM bibliografia WHERE LOWER(TRIM(titulo)) = LOWER(TRIM(:t))")
    try:
        if hasattr(conn, 'connect'):
            with conn.connect() as connection:
                res = connection.execute(query, {"t": titulo}).fetchone()
        else:
            res = conn.execute(query, {"t": titulo}).fetchone()
        return res is not None
    except:
        return False

# ==========================================================
# UI - UPLOAD E EXTRAÇÃO
# ==========================================================
st.title("📝 Cadastro de Referências Bibliográficas")

with st.expander("📂 Importar dados de PDF (Opcional)", expanded=True):
    u_file = st.file_uploader("Selecione um PDF para preenchimento automático", type=["pdf"])
    if u_file and st.button("🤖 Extrair com IA"):
        with st.spinner("Analisando PDF..."):
            texto_pdf = extrair_texto_pdf(u_file)
            dados = sugerir_metadados(texto_pdf)
            if dados:
                st.session_state.form_data.update(dados)
                st.success("Dados extraídos! Confira os campos abaixo.")
                time.sleep(1)
                st.rerun()

# ==========================================================
# FORMULÁRIO DE CADASTRO
# ==========================================================
with st.form("form_cadastro"):
    # Linha 1
    c1, c2 = st.columns([3, 1])
    with c1:
        titulo = st.text_input("Título *", value=st.session_state.form_data["titulo"])
    with c2:
        lista_anos = list(range(2026, 1899, -1))
        try:
            val_ano = int(st.session_state.form_data["ano"])
            ano_idx = lista_anos.index(val_ano)
        except:
            ano_idx = 1
        ano = st.selectbox("Ano", options=lista_anos, index=ano_idx)

    # Linha 2
    c_aut, c_inst = st.columns(2)
    with c_aut:
        autores = st.text_input("Autor(es)", value=st.session_state.form_data["autores"])
    with c_inst:
        instituicao = st.text_input("Instituição", value=st.session_state.form_data["instituicao"])

    # Linha 3
    col_tipo, col_pais, col_idioma = st.columns(3)
    with col_tipo:
        tipo_doc = st.selectbox("Tipo de Documento", ["", "Artigo", "Livro", "Capítulo", "Dissertação", "Tese", "Relatório", "Outros"])
    with col_pais:
        pais = st.selectbox("País", ["", "Brasil", "Espanha", "Portugal", "EUA", "Argentina", "Chile", "Outros"])
    with col_idioma:
        idioma = st.selectbox("Idioma", ["Português", "Inglês", "Espanhol", "Francês", "Outro"])

    # Temas
    tema = st.selectbox("Tema", ["", "Financiamento", "Tarifa", "Drenagem Urbana", "SBN", "Sustentabilidade", "Outro"])
    subtema = st.selectbox("Subtema", ["", "PPP", "Cidades-Esponja", "Controle e Fiscalização", "Jardins de Chuva", "Outro"])

    palavras_chave = st.text_input("Palavras-chave", value=st.session_state.form_data["palavras_chave"])
    resumo = st.text_area("Resumo", value=st.session_state.form_data["resumo"], height=150)

    # Rodapé
    col_v, col_l = st.columns(2)
    with col_v:
        veiculo = st.text_input("Veículo de Publicação / DOI")
    with col_l:
        link = st.text_input("Link")

    submitted = st.form_submit_button("💾 Salvar Documento", use_container_width=True)

# ==========================================================
# SALVAMENTO NO BANCO
# ==========================================================
if submitted:
    if not titulo.strip():
        st.error("O título é obrigatório.")
    elif verificar_duplicidade(titulo, autores):
        st.warning("⚠️ Este documento já existe no sistema.")
    else:
        try:
            nome_arquivo = ""
            if u_file:
                nome_arquivo = f"{uuid.uuid4()}.pdf"
                with open(PDF_DIR / nome_arquivo, "wb") as f:
                    f.write(u_file.getbuffer())

            inserir_documento(
                titulo=titulo, autores=autores, ano=ano, tipo_documento=tipo_doc,
                instituicao=instituicao, pais=pais, idioma=idioma, tema=tema,
                subtema=subtema, resumo=resumo, palavras_chave=palavras_chave,
                veiculo_publicacao=veiculo, link=link, arquivo_pdf=nome_arquivo
            )
            
            st.success("✅ Cadastro realizado com sucesso!")
            # Resetar estado
            st.session_state.form_data = {k: "" for k in st.session_state.form_data}
            st.session_state.form_data["ano"] = 2025
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
