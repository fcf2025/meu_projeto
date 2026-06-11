import streamlit as st
import uuid
import time
import json
from pathlib import Path
from sqlalchemy import text
from PyPDF2 import PdfReader
from openai import OpenAI  # NOVO: Para extração com IA

# Configurações de API
DATABASE_URL = st.secrets["DATABASE_URL"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY) # NOVO: Cliente OpenAI

from utils.database import conectar_db, inserir_documento

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Cadastro de Bibliografia", page_icon="📝", layout="wide")

# Inicializar Session State para os campos (NOVO)
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "titulo": "", "autores": "", "ano": 2025,"pais": "", "resumo": "", 
        "palavras_chave": "", "instituicao": "", "idioma": "Português"
    }

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# FUNÇÕES DE APOIO (NOVO)
# ==========================================================

def extrair_texto_pdf(uploaded_file):
    """Extrai as primeiras páginas do PDF para análise."""
    reader = PdfReader(uploaded_file)
    texto = ""
    # Lemos apenas as primeiras 4 páginas para economizar tokens e focar no essencial
    for i in range(min(len(reader.pages), 4)):
        texto += reader.pages[i].extract_text()
    return texto

def sugerir_metadados(texto_pdf):
    """Usa IA para extrair metadados do texto."""
    prompt = f"""
    Extraia os metadados do seguinte texto de um documento técnico/acadêmico. 
    Responda APENAS em formato JSON estrito com as chaves: 
    "titulo", "autores", "ano","pais", "resumo", "palavras_chave", "instituicao", "idioma".
    Texto: {texto_pdf[:4000]}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Ou gpt-3.5-turbo
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
        with conn.connect() as connection:
            res = connection.execute(query, {"t": titulo}).fetchone()
        return res is not None
    except: return False

# ==========================================================
# UI - UPLOAD E EXTRAÇÃO (NOVO)
# ==========================================================
st.title("📝 Cadastro de Referências Bibliográficas")

with st.expander("📂 Upload e Extração Automática", expanded=True):
    uploaded_file = st.file_uploader("Arraste o PDF aqui para preencher o formulário automaticamente", type=["pdf"])
    
    if uploaded_file and st.button("🤖 Extrair Dados com IA"):
        with st.spinner("Analisando PDF..."):
            texto = extrair_texto_pdf(uploaded_file)
            dados_sugeridos = sugerir_metadados(texto)
            
            if dados_sugeridos:
                st.session_state.form_data.update(dados_sugeridos)
                st.success("Dados extraídos! Confira os campos abaixo.")
                # Força o recarregamento para mostrar nos inputs
                st.rerun()

# ==========================================================
# FORMULÁRIO
# ==========================================================
with st.form("form_cadastro"):
    col1, col2 = st.columns(2)
    with col1:
        # Usamos o session_state para preencher o valor padrão
        titulo = st.text_input("Título *", value=st.session_state.form_data["titulo"])
    with col2:
        lista_anos = list(range(2026, 1899, -1))
        # Tenta encontrar o ano extraído na lista, senão usa 2025
        try:
            ano_idx = lista_anos.index(int(st.session_state.form_data["ano"]))
        except:
            ano_idx = 1
        ano = st.selectbox("Ano", options=lista_anos, index=ano_idx)

        autores = st.text_input("Autor(es)", value=st.session_state.form_data["autores"])
        instituicao = st.text_input("Instituição", value=st.session_state.form_data["instituicao"])

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
       pais = st.selectbox("País", ["", "Brasil", "Argentina", "Chile", "Espanha", 
                "Europa","Estados Unidos","Alemanha","Portugal", "Países Baixos","Suécia","Uruguai", "Outro"])
    
        
        idioma = st.selectbox("Idioma", ["Português", "Inglês", "Espanhol", "Outro"])
        tema = st.selectbox("Tema", ["", "Financiamento", "Tarifa (Taxas de drenagem)", "Custos (Operacionais e de Implantação)","Taxas","Regulação e Governança","Soluções Baseadas na Natureza (SbN) e Infraestrutura Verde",
                    "Planejamento Urbano e Uso do Solo","Sustentabilidade e Mudanças Climáticas","Tecnologias de Monitoramento", "Cidades Inteligentes (Smart Cities)",                    
                    "Investimentos em DMAPU","Cidades Inteligentes","Manejo de Águas Pluviais Urbanas (MAPU)",
                    "Saneamento Básico","Direitos Fundamentais","Drenagem Urbana",
                    "Recursos Hídricos","Outro"]
        )
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
                "Implementação de sistemas sustentáveis","Eficiência Econômica","Custos Operacionais","Regulação","Outros"]
        )

        palavras_chave = st.text_input("Palavras-chave", value=st.session_state.form_data["palavras_chave"])
        resumo = st.text_area("Resumo", value=st.session_state.form_data["resumo"], height=150)

    # Campos de rodapé
    col_v, col_l = st.columns(2)
    with col_v: veiculo_publicacao = st.selectbox("Veículo de Publicação",["", "Parcerias Público-Privadas (PPPs)","Títulos Verdes (Green Bonds)","Investimento em Propriedade Privada",
             "Fundos Municipais de Saneamento","Financiamento Multilateral (BID/BIRD)","Cálculo por Área Impermeabilizada","Cofaturamento na Conta de Água",
            "Estruturação de Tarifas Sociais","Incentivos por Desempenho (Taxa de Desconto)","Aceitabilidade Social da Cobrança", 
            "Norma de Referência 12/2025 (ANA)","Indicadores de Desempenho (KPIs)","Consórcios Intermunicipais","Controle e Fiscalização","Segurança Jurídica dos Contratos",
            "Cidades-Esponja (Sponge Cities)","Desempenho de Jardins de Chuva","Telhados Verdes e Microclima","Multifuncionalidade de Parques Lineares",
            "Desenho Urbano Sensível à Água (WSUD)","Zonemanento e Taxas de Permeabilidade","Integração PDD (Plano Diretor de Drenagem) e Plano Diretor",
            "Drenagem em Assentamentos Precários","Revitalização de Rios Urbanos","Adaptação a Chuvas Extremas","Gestão de Risco de Desastres",
            "Vulnerabilidade e Justiça Climática","Resiliência Baseada em Ecossistemas (AbE)","Adaptação de Cidades Costeiras",
            "Monitoramento em Tempo Real (IoT)","Digital Twins (Gêmeos Digitais)","IA na Previsão de Inundações","Modelagem SWMM e HEC-RAS",
            "Uso de Drones na Inspeção","Metodologia de Cobrança","Governança Urbana e Cidades Inteligentes",
            "Simulação de Taxa de Drenagem", "Planejamento e Avaliação de Políticas Públicas",
            "Implementação de sistemas sustentáveis","Eficiência Econômica","Custos Operacionais","Regulação","Outros"])

    with col_l: link = st.text_input("Link")

    submitted = st.form_submit_button("💾 Salvar no Banco de Dados", use_container_width=True)

# ==========================================================
# PROCESSAMENTO FINAL
# ==========================================================
if submitted:
    if not titulo:
        st.error("O título é obrigatório.")
    elif verificar_duplicidade(titulo, autores):
        st.warning("⚠️ Documento já cadastrado.")
    else:
        try:
            nome_arquivo = ""
            if uploaded_file:
                nome_arquivo = f"{uuid.uuid4()}.pdf"
                with open(PDF_DIR / nome_arquivo, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            inserir_documento(
                            titulo=titulo, autores=autores, ano=ano, tipo_documento=tipo_documento,
                            instituicao=instituicao, pais=pais, idioma=idioma, tema=tema,
                            subtema=subtema, resumo=resumo, palavras_chave=palavras_chave,
                            veiculo_publicacao=veiculo_publicacao, link=link, arquivo_pdf=nome_pdf, categoria=categoria,
                            metodo=metodo, regiao=regiao, observacoes=observacoes)

            st.success("Salvo com sucesso!")
            # Limpa o estado após salvar
            st.session_state.form_data = {"titulo": "", "autores": "", "ano": 2025, "resumo": "", "palavras_chave": "", "instituicao": "", "idioma": "Português"}
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
