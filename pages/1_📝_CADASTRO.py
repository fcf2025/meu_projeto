# ==========================================================
# pages/cadastro.py
# Cadastro de Bibliografia - Biblioteca Digital DMAPLU
# ==========================================================

import streamlit as st
from pathlib import Path
import uuid
from sqlalchemy import text

# ==========================================================
# IMPORTAÇÕES DE BANCO
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
# CAMINHO PDFs
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

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
    except Exception:
        return False
    finally:
        if hasattr(conn, 'close'): 
            conn.close()

# ==========================================================
# TÍTULO
# ==========================================================
st.title("📝 Cadastro de Referências Bibliográficas")
st.markdown("Preencha os campos abaixo para inserir um novo documento.")
st.markdown("---")

# ==========================================================
# FORMULÁRIO
# ==========================================================
with st.form("form_cadastro", clear_on_submit=True):

    # --- LINHA 1 ---
    col1, col2 = st.columns([3, 1])
    with col1:
        titulo = st.text_input("Título *")
    with col2:
        # ANO COMO SELECIONÁVEL
        lista_anos = list(range(2026, 1899, -1))
        ano = st.selectbox("Ano", options=lista_anos, index=1) # index 1 = 2025

    # --- LINHA 2 ---
    autores = st.text_input("Autor(es)")
    instituicao = st.text_input("Instituição do Autor/Afiliação")

    # --- LINHA 3 ---
    col1, col2, col3 = st.columns(3)
    with col1:
        tipo_documento = st.selectbox("Tipo de Documento", ["", "Artigo", "Livro", "Capítulo", "Dissertação", "Tese", "Monografia", "TCC", "Outros"])
    with col2:
        pais = st.selectbox("País", ["", "Brasil", "Argentina", "Chile", "Espanha", "Estados Unidos", "Portugal", "Uruguai", "Outro"])
    with col3:
        idioma = st.selectbox("Idioma", ["", "Português", "Inglês", "Espanhol", "Francês", "Outro"])

    # --- LINHA 5 ---
    col1, col2 = st.columns(2)
    with col1:
        tema = st.selectbox("Tema", ["", "Planejamento e elaboração de Planos de Drenagem e Manejo de Águas Pluviais (PDMP)",
                "Integração entre DMAPU e plano diretor municipal",
                "Zoneamento de risco de inundações e ocupação de áreas críticas",
                "Medidas estruturais de drenagem (bueiros, canais, reservatórios, bacias de detenção)",
                "Infraestrutura verde e soluções baseadas na natureza na drenagem urbana",
                "Modelagem hidrológica e hidráulica de bacias urbanas",
                "Controle de cheias e gestão de eventos pluviais extremos",
                "Gestão integrada de recursos hídricos e DMAPU",
                "Políticas públicas, regulamentação e fiscalização do manejo de águas pluviais",
                "Participação comunitária, educação ambiental e aceitação social de obras de drenagem","Financiamento",
                "Outro"])
    with col2:
        subtema = st.selectbox("Subtema", ["", "Planejamento urbano integrado",
            "Diagnóstico de bacias urbanas e mapas de pontos críticos de inundação",
            "Projeção de cenários de chuva intensa e eventos extremos",
            "Zoneamento de risco para ocupação de margens de rios e áreas de escoamento",
            "Obras de drenagem em bairros de baixa renda e assentamentos precários",
            "Pavimentos permeáveis e soluções de superfície porosa em vias e calçadas",
            "Telhados e paredes verdes em edificações urbanas",
            "Bacias de detenção e retenção em praças, parques e áreas públicas",
            "Microrreservatórios, reservatórios subterrâneos e cisternas coletivas",
            "Integração de poços de infiltração e valas de drenagem com sistemas viários",
            "Modelagem computacional de inundações urbanas (softwares como InfoWorks, SWMM, etc.)",
            "Uso de geoprocessamento e SIG para mapear áreas de risco e drenagem",
            "Telemetria, sensores de nível e chuva e sistemas de alerta precoce",
            "Manual de condicionantes de parcelamento e uso do solo para proteção de drenagem",
            "Fiscalização de loteamentos e obras que interferem em bocas de lobo e canais",
            "Participação de associações de moradores em projetos de drenagem local",
            "Campanhas de educação ambiental sobre descarte de resíduos e entupimento de bueiros",
            "Modelos de financiamento para obras de drenagem e manutenção de sistemas",
            "Indicadores de desempenho de sistemas de DMAPU (velocidade de escoamento, inundação, etc.)",
            "Integração entre DMAPU, saneamento básico e mobilidade urbana",
            "Monitoramento pós‑obra e avaliação de risco após implantação de sistemas de drenagem",
            "Outros"])

    palavras_chave = st.text_input("Palavras-chave")
    resumo = st.text_area("Resumo", height=150)

    # --- LINHA 8 ---
    col1, col2 = st.columns(2)
    with col1:
        doi = st.selectbox("Veículo de Publicação", ["Revista", "Livro", "Conferência", "Site", "Repositório", "Outro"])
    with col2:
        link = st.text_input("Link")

    # --- LINHA 9 ---
    col1, col2, col3 = st.columns(3)
    with col1:
        categoria = st.selectbox("Categoria", ["", "Infraestrutura", "Gestão", "Planejamento", "Educação", "Outro"])
    with col2:
        metodo = st.selectbox("Método", ["", "Pesquisa de Campo", "Entrevistas", "Modelagem", "Análise Documental", "Outro"])
    with col3:
        regiao = st.selectbox("Região", ["", "Brasil", "América Latina", "Europa", "Global", "Outro"])

    observacoes = st.text_area("Observações", height=80)

    # --- UPLOAD ---
    st.markdown("### 📎 Upload de PDF")
    uploaded_file = st.file_uploader("Selecione um PDF", type=["pdf"])

    # --- BOTÃO ---
    submitted = st.form_submit_button("💾 Salvar Documento", use_container_width=True)

# ==========================================================
# PROCESSAMENTO (ESTA PARTE DEVE FICAR FORA DO WITH FORM)
# ==========================================================
if submitted:
    if titulo.strip() == "":
        st.error("O título é obrigatório.")
    
    elif verificar_duplicidade(titulo, autores):
        st.warning("⚠️ Este documento (Título + Autor) já existe no sistema.")
        
    else:
        try:
            nome_pdf = ""
            if uploaded_file is not None:
                extensao = "pdf"
                nome_pdf = f"{uuid.uuid4()}.{extensao}"
                caminho_pdf = PDF_DIR / nome_pdf
                with open(caminho_pdf, "wb") as f:
                    f.write(uploaded_file.read())

            inserir_documento(
                titulo=titulo, autores=autores, ano=ano, tipo_documento=tipo_documento,
                instituicao=instituicao, pais=pais, idioma=idioma, tema=tema,
                subtema=subtema, resumo=resumo, palavras_chave=palavras_chave,
                doi=doi, link=link, arquivo_pdf=nome_pdf, categoria=categoria,
                metodo=metodo, regiao=regiao, observacoes=observacoes
            )

            st.success("Cadastro realizado com sucesso!")
            st.balloons()
            st.toast("Dados atualizados!")

        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU • Cadastro")
