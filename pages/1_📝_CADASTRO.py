# ==========================================================
# pages/cadastro.py
# Cadastro de Bibliografia - Biblioteca Digital DMAPLU
# ==========================================================

import streamlit as st
DATABASE_URL = st.secrets["DATABASE_URL"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

from pathlib import Path
import uuid
from sqlalchemy import text
import time
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
        tipo_documento = st.selectbox("Tipo de Documento", ["",    "Artigo",
                "Livro",
                "Capítulo",
                "Dissertação",
                "Tese",
                "Monografia",
                "Trabalho de Conclusão de Curso (TCC)",
                "Anais de Congresso / Conferência",
                "Resenha / Revisão",
                "Estudo Técnico",
                "Nota Técnica",
                "Informação Técnica",
                "Parecer Técnico",
                "Norma Técnica (ABNT, ISO etc.)",
                "Manual",
                "White Paper",
                "Mapa / Planta / Desenho Técnico",
                "Dados Estatísticos / Base de Dados",
                "Legislação",
                "Regulamentação",
                "Plano / Projeto",
                "Patente",
                "Guia Prático / Cartilha",
                "Boletim Técnico / Informativo",
                "Artigo de Opinião / Editorial",
                "Entrevista / Depoimento",
                "Outros", "Outro"])
    with col2:
        pais = st.selectbox("País", ["", "Brasil", "Argentina", "Chile", "Espanha", 
                "Europa","Estados Unidos","Alemanha","Portugal", "Países Baixos","Suécia","Uruguai", "Outro"])
    with col3:
        idioma = st.selectbox("Idioma", ["", "Português", "Inglês", "Espanhol", "Francês", "Outro"])

    # --- LINHA 5 ---
    col1, col2 = st.columns(2)
    with col1:
        tema = st.selectbox("Tema", ["", "Financiamento", "Tarifa (Taxas de drenagem)", "Custos (Operacionais e de Implantação)","Taxas","Regulação e Governança","Soluções Baseadas na Natureza (SbN) e Infraestrutura Verde",
                "Planejamento Urbano e Uso do Solo","Sustentabilidade e Mudanças Climáticas","Tecnologias de Monitoramento", "Cidades Inteligentes (Smart Cities)",                    
                "Investimentos em DMAPU","Cidades Inteligentes","Manejo de Águas Pluviais Urbanas (MAPU)",
                "Saneamento Básico","Direitos Fundamentais","Drenagem Urbana",
                "Recursos Hídricos","Outro"])
    with col2:
        subtema = st.selectbox("Subtema", ["", "Parcerias Público-Privadas (PPPs)","Títulos Verdes (Green Bonds)","Investimento em Propriedade Privada",
             "Fundos Municipais de Saneamento","Financiamento Multilateral (BID/BIRD)","Cálculo por Área Impermeabilizada","Cofaturamento na Conta de Água",
            "Estruturação de Tarifas Sociais","Incentivos por Desempenho (Taxa de Desconto)","Aceitabilidade Social da Cobrança", 
            "Norma de Referência 12/2025 (ANA)","Indicadores de Desempenho (KPIs)","Consórcios Intermunicipais","Controle e Fiscalização","Segurança Jurídica dos Contratos"
            "Cidades-Esponja (Sponge Cities)","Desempenho de Jardins de Chuva","Telhados Verdes e Microclima","Multifuncionalidade de Parques Lineares",
            "Desenho Urbano Sensível à Água (WSUD)","Zonemanento e Taxas de Permeabilidade","Integração PDD (Plano Diretor de Drenagem) e Plano Diretor",
            "Drenagem em Assentamentos Precários","Revitalização de Rios Urbanos","Adaptação a Chuvas Extremas","Gestão de Risco de Desastres",
            "Vulnerabilidade e Justiça Climática","Resiliência Baseada em Ecossistemas (AbE)","Adaptação de Cidades Costeiras",
            "Monitoramento em Tempo Real (IoT)","Digital Twins (Gêmeos Digitais)","IA na Previsão de Inundações","Modelagem SWMM e HEC-RAS",
            "Uso de Drones na Inspeção","Metodologia de Cobrança","Governança Urbana e Cidades Inteligentes",
            "Simulação de Taxa de Drenagem", "Planejamento e Avaliação de Políticas Públicas",
            "Implementação de sistemas sustentáveis","Eficiência Econômica","Custos Operacionais","Regulação","Outros"])

    palavras_chave = st.text_input("Palavras-chave")
    resumo = st.text_area("Resumo", height=150)

    # --- LINHA 8 ---
    col1, col2 = st.columns(2)
    with col1:
        doi = st.selectbox("Veículo de Publicação",["", "Parcerias Público-Privadas (PPPs)","Títulos Verdes (Green Bonds)","Investimento em Propriedade Privada",
             "Fundos Municipais de Saneamento","Financiamento Multilateral (BID/BIRD)","Cálculo por Área Impermeabilizada","Cofaturamento na Conta de Água",
            "Estruturação de Tarifas Sociais","Incentivos por Desempenho (Taxa de Desconto)","Aceitabilidade Social da Cobrança", 
            "Norma de Referência 12/2025 (ANA)","Indicadores de Desempenho (KPIs)","Consórcios Intermunicipais","Controle e Fiscalização","Segurança Jurídica dos Contratos"
            "Cidades-Esponja (Sponge Cities)","Desempenho de Jardins de Chuva","Telhados Verdes e Microclima","Multifuncionalidade de Parques Lineares",
            "Desenho Urbano Sensível à Água (WSUD)","Zonemanento e Taxas de Permeabilidade","Integração PDD (Plano Diretor de Drenagem) e Plano Diretor",
            "Drenagem em Assentamentos Precários","Revitalização de Rios Urbanos","Adaptação a Chuvas Extremas","Gestão de Risco de Desastres",
            "Vulnerabilidade e Justiça Climática","Resiliência Baseada em Ecossistemas (AbE)","Adaptação de Cidades Costeiras",
            "Monitoramento em Tempo Real (IoT)","Digital Twins (Gêmeos Digitais)","IA na Previsão de Inundações","Modelagem SWMM e HEC-RAS",
            "Uso de Drones na Inspeção","Metodologia de Cobrança","Governança Urbana e Cidades Inteligentes",
            "Simulação de Taxa de Drenagem", "Planejamento e Avaliação de Políticas Públicas",
            "Implementação de sistemas sustentáveis","Eficiência Econômica","Custos Operacionais","Regulação","Outros"])
    with col2:
        link = st.text_input("Link")

    # --- LINHA 9 ---
    col1, col2, col3 = st.columns(3)
    with col1:
        categoria = st.selectbox("Categoria", ["", "Regulação e Governança",
                "Sustentabilidade Financeira",
                "Infraestrutura e Engenharia",
                "Soluções Baseadas na Natureza (SbN)",
                "Planejamento Urbano e Territorial",
                "Mudanças Climáticas e Resiliência",
                "Operação e manutenção",
                "Tecnologia e Monitoramento","Economia do Saneamento","Gestão Pública","Infraestrutura",
                "Engenharia Urbana","Drenagem Urbana","Gestão Ambiental","Outro"]) 
    with col2:
        metodo = st.selectbox("Método", ["", "Pesquisa de Campo",
                "Estudo de Caso",
                "Questionários/Survey",
                "Revisão Bibliográfica/Sistemática",
                "Experimento Controlado",
                "Modelagem Matemática",
                "Análise Documental",
                "Benchmarking",
                "Análise Econômico-Financeira",
                "Análise Multicritério",
                "Geoprocessamento/SIG",
                "Análise de Dados Secundários/Estatística",
                "Simulação Estocástica/Monte Carlo",
                "Outro"])
    with col3:
        regiao = st.selectbox("Região", ["", "Brasil", "América Latina","América do Norte", "Europa", "Global", "Outro"])

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
            placeholder = st.empty()
            placeholder.success("Cadastro realizado com sucesso!")
            
            time.sleep(3)  # espera 3 segundos
            placeholder.empty()  # apaga a mensagem
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

# ==========================================================
# RODAPÉ
# ==========================================================
st.markdown("---")
st.caption("Biblioteca Digital DMAPLU • Cadastro")
