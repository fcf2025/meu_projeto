import streamlit as st
import uuid
import time
import json
from pathlib import Path
from sqlalchemy import text
from PyPDF2 import PdfReader
from openai import OpenAI
# ==========================================================
# DEFINIÇÃO DAS LISTAS GLOBAIS
#==========================================================
LISTA_TIPOS = ["", "Artigo",
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
                "Outros"]
LISTA_TEMAS = ["", "Financiamento",
                "Tarifa (Taxas de drenagem)",
                "Custos (Operacionais e de Implantação)",
                "Taxas",
                "Regulação e Governança",
                "Soluções Baseadas na Natureza (SbN) e Infraestrutura Verde",
                "Planejamento Urbano e Uso do Solo",
                "Sustentabilidade e Mudanças Climáticas",
                "Tecnologias de Monitoramento",
                "Cidades Inteligentes (Smart Cities)",
                "Investimentos em DMAPU",
                "Manejo de Águas Pluviais Urbanas (MAPU)",
                "Saneamento Básico",
                "Direitos Fundamentais",
                "Drenagem Urbana",
                "Recursos Hídricos",
                "Gestão de Riscos e Desastres Hidrológicos",
                "Microdrenagem e Sistemas de Coleta",
                "Macrodrenagem e Controle de Cheias",
                "Modelagem Hidrodinâmica e Simulação de Vazão",
                "Controle de Erosão e Assoreamento",
                "Qualidade das Águas e Poluição Difusa",
                "Técnicas de Baixo Impacto (LID - Low Impact Development)",
                "Bacias de Detenção e Retenção (Piscinões)",
                "Planos Diretores de Drenagem Urbana (PDDU)",
                "Participação Social e Mobilização Comunitária",
                "Educação Ambiental e Percepção de Risco",
                "Manutenção Corretiva e Preventiva de ativos",
                "Saúde Pública e Doenças de Veiculação Hídrica",
                "Impermeabilização do Solo e Coeficientes de Escoamento",
                "Pavimentos Permeáveis e Dispositivos de Infiltração",
                "Sistemas de Alerta Precoce e Telemetria",
                "Instrumentos de Outorga e Legislação de Águas",
                "Recuperação de Rios Urbanos e Renaturalização",
                "Interoperabilidade entre Sistemas de Drenagem e Esgoto",
                "Parcerias Público-Privadas (PPP) e Concessões",
                "Outro"]
LISTA_SUBTEMAS = ["", "Parcerias Público-Privadas (PPPs)","Títulos Verdes (Green Bonds)","Investimento em Propriedade Privada",
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
LISTA_DOI = [
                "",
                "Revista",
                "Repositorio",
                "Anais",
                "Periódico Científico",
                "Tese de Doutorado",
                "Dissertação de Mestrado",
                "Relatório Técnico-Científico",
                "Manual ou Guia Técnico",
                "Livro",
                "Capítulo de Livro",
                "Nota Técnica",
                "Boletim Informativo ou Epidemiológico",
                "Plano Diretor (Documento Oficial)",
                "Cartilha Educativa",
                "Norma Técnica (ABNT/Entidades Reguladoras)",
                "Diário Oficial (União, Estado ou Município)",
                "Monografia",
                "Portal de Dados Abertos / Dashboard",
                "Documento de Patente",
                "Caderno de Resumos de Eventos",
                "Site ou Blog Institucional",
                "Podcast ou Webinar (Transcrição/Mídia)",
                "Estudo de Impacto Ambiental (EIA/RIMA)",
                "Projetos de Lei e Decretos",
                "Informativo de Conselho Municipal",
                "Termo de Referência (TR)",
                "Manual de Drenagem Urbana (Municipal/Estadual)",
                "Artigo de Opinião/Jornalístico",
                "Memoriais Descritivos",
                "Base de Dados Georreferenciados (Metadados)",
                "Outro"]
LISTA_CATEGORIA = ["", "Regulação e Governança",
                "Sustentabilidade Financeira",
                "Infraestrutura e Engenharia",
                "Soluções Baseadas na Natureza (SbN)",
                "Planejamento Urbano e Territorial",
                "Mudanças Climáticas e Resiliência",
                "Operação e manutenção",
                "Tecnologia e Monitoramento",
                "Microdrenagem e Redes Coletoras",
                "Macrodrenagem e Canalização",
                "Sistemas de Detenção e Retenção (Piscinões)",
                "Modelagem Hidrológica e Hidrodinâmica",
                "Qualidade da Água Pluvial e Poluição Difusa",
                "Planos Diretores de Drenagem Urbana (PDDU)",
                "Controle de Processos Erosivos e Assoreamento",
                "Técnicas de Baixo Impacto (LID)",
                "Pavimentos Permeáveis e Superfícies Filtrantes",
                "Sistemas de Alerta e Gestão de Emergências",
                "Mapeamento de Áreas de Risco e Inundação",
                "Mecanismos de Cobrança e Tarifação de Drenagem",
                "Interoperabilidade com Esgotamento Sanitário",
                "Gestão de Resíduos Sólidos em Sistemas de Drenagem",
                "Reabilitação e Renaturalização de Rios",
                "Hidrologia e Séries Temporais de Precipitação",
                "Gestão da Impermeabilização do Solo",
                "Normatização e Manuais Técnicos",
                "Educação Ambiental para o Manejo de Águas",
                "Dragagem e Desobstrução de Galerias",
                "Cadastramento de Ativos e Geoprocessamento",
                "Inovação em Dispositivos de Drenagem",
                "Outro"]
LISTA_METODO = ["", "Pesquisa de Campo – coleta de dados diretamente em ambientes reais.",
                "Entrevistas – estruturadas, semiestruturadas ou abertas.",
                "Questionários/Survey – aplicação de formulários para coleta de dados.",
                "Observação Participante – acompanhamento direto de práticas ou comunidades.",
                "Experimento Controlado – testes em condições laboratoriais ou simuladas.",
                "Modelagem Matemática – construção de equações e modelos analíticos.",
                "Análise Documental – estudo de relatórios, legislações, registros históricos.",
                "Benchmarking – comparação com padrões ou casos de referência.",
                "Delphi/Consulta a Especialistas – coleta de opiniões de especialistas em rodadas sucessivas.",
                "Análise Multicritério – avaliação de alternativas considerando múltiplos fatores.",
                "Geoprocessamento/SIG – uso de Sistemas de Informação Geográfica.",
                "Análise de Sensibilidade – testar variações em parâmetros de modelos.",
                "Prototipagem – desenvolvimento de versões iniciais de soluções para teste.",
                "Meta-análise – síntese quantitativa de resultados de múltiplos estudos.",
                "Revisão Sistemática – levantamento estruturado e criterioso da literatura.",
                "Simulação Estocástica/Monte Carlo – uso de probabilidades para prever cenários.",
                "Análise Qualitativa – categorização e interpretação de dados não numéricos.",
                "Análise Quantitativa – uso de estatística e métricas numéricas.",
                "Estudo Longitudinal – acompanhamento de fenômenos ao longo do tempo.",
                "Estudo Transversal – análise em um único momento ou recorte.",
                "Outro"]
LISTA_REGIAO = ["", "Brasil",
                "América Latina",
                "Europa",
                "América do Norte",
                "Ásia",
                "África",
                "Global",
                "Outro"]

# Inicializar Session State com tipo_documento
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        "titulo": "",
        "autores": "",
        "ano": 2025,
        "instituicao": "",
        "pais": "",
        "idioma": "Português",
        "tipo_documento": "",
        "tema": "",
        "subtema": "",
        "categoria": "",
        "metodo": "",
        "regiao": "",
        "observacoes": "",
        "doi": "",
        "link": "",
        "resumo": "",
        "palavras_chave": ""
    }
# ==========================================================
# CONFIGURAÇÃO E CHAVES
# ==========================================================
DATABASE_URL = st.secrets["DATABASE_URL"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

from utils.database import conectar_db, inserir_documento

st.set_page_config(page_title="Cadastro de Bibliografia", page_icon="📝", layout="wide")

# Lista de Tipos de Documento (Definida fora para ser usada no index)



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
        for i in range(min(len(reader.pages), 30)):
            page_text = reader.pages[i].extract_text()
            if page_text: texto += page_text
        return texto
    except Exception as e:
        st.error(f"Erro ao ler PDF: {e}")
        return ""

def sugerir_metadados(texto_pdf):
    # 1. Transformamos TODAS as listas em texto para a IA não inventar opções
    tipos_str = ", ".join(LISTA_TIPOS[1:])
    temas_str = ", ".join(LISTA_TEMAS[1:])
    subtemas_str = ", ".join(LISTA_SUBTEMAS[1:])
    categorias_str = ", ".join(LISTA_CATEGORIAS[1:]) # ADICIONADO
    metodos_str = ", ".join(LISTA_METODOS[1:])       # ADICIONADO
    regioes_str = ", ".join(LISTA_REGIOES[1:])       # ADICIONADO

    prompt = f"""
    Você é um bibliotecário especialista. Sua tarefa é extrair metadados do texto fornecido.
    
    REGRAS CRÍTICAS:
    1. Você DEVE preencher TODOS os campos do JSON abaixo. Nenhum campo pode ser vazio ou nulo.
    2. Se uma informação não estiver explícita, use seu conhecimento para INFERIR a resposta mais provável com base no contexto técnico do documento.
    3. Para 'tipo_documento', escolha obrigatoriamente um destes: [{tipos_str}].
    4. Para 'tema', escolha obrigatoriamente um destes: [{temas_str}].
    5. Para 'subtema', escolha obrigatoriamente um destes: [{subtemas_str}].
    6. Para 'categoria', escolha obrigatoriamente um destes: [{categorias_str}].
    7. Para 'metodo', escolha obrigatoriamente um destes: [{metodos_str}].
    8. Para 'regiao', escolha obrigatoriamente um destes: [{regioes_str}].
    9. Se não encontrar o Ano, use '2024'. Se não encontrar a Instituição, use 'Não identificada'.
    10. No campo 'pais', deduza pelo contexto ou idioma.
    11. O campo 'observacoes' deve conter uma breve nota sobre a relevância do documento.
    
    RESPONDA APENAS O JSON NO SEGUINTE FORMATO:
    {{
      "titulo": "",
      "autores": "",
      "ano": 2024,
      "instituicao": "",
      "pais": "",
      "idioma": "Português",
      "tipo_documento": "",
      "tema": "",
      "subtema": "",
      "categoria": "",
      "metodo": "",
      "regiao": "",
      "observacoes":"",
      "doi": "",
      "link": "",
      "resumo": "",
      "palavras_chave": ""
    }}
    
    TEXTO DO PDF:
    {texto_pdf[:5000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Você é um bibliotecário que preenche formulários técnicos e nunca deixa campos em branco."},
                      {"role": "user", "content": prompt}],
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
# UI - UPLOAD
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
                st.success("Dados extraídos!")
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
            ano_idx = lista_anos.index(int(st.session_state.form_data["ano"]))
        except:
            ano_idx = 1
        ano = st.selectbox("Ano", options=lista_anos, index=ano_idx)

    # Linha 2
    c_aut, c_inst = st.columns(2)
    with c_aut:
        autores = st.text_input("Autor(es)", value=st.session_state.form_data["autores"])
    with c_inst:
        instituicao = st.text_input("Instituição", value=st.session_state.form_data["instituicao"])

    # Linha 3 - CORREÇÃO DO TIPO DE DOCUMENTO
    col_tipo, col_pais, col_idioma = st.columns(3)
    with col_tipo:
        # Lógica para selecionar o índice vindo da IA
        tipo_ia = st.session_state.form_data.get("tipo_documento", "")
        try:
            # Tenta encontrar o que a IA mandou na nossa lista oficial
            idx_tipo_default = LISTA_TIPOS.index(tipo_ia) if tipo_ia in LISTA_TIPOS else 0
        except:
            idx_tipo_default = 0
            
        tipo_documento = st.selectbox("Tipo de Documento", options=LISTA_TIPOS, index=idx_tipo_default)

    with col_pais:
        pais = st.selectbox("País", ["Brasil", "Portugal", "Espanha", "EUA", "Outros"])
    with col_idioma:
        idioma = st.selectbox("Idioma", ["Português", "Inglês", "Espanhol", "Outro"])
# --- BLOCO DE TEMAS ---
    col_tema, col_sub = st.columns(2)
    
    with col_tema:
        # Pega o valor que veio da IA ou do estado anterior
        val_tema = st.session_state.form_data.get("tema", "")
        # Se o valor da IA não estiver na lista, volta para o índice 0 (vazio)
        idx_tema = LISTA_TEMAS.index(val_tema) if val_tema in LISTA_TEMAS else 0
        tema = st.selectbox("Tema", options=LISTA_TEMAS, index=idx_tema)

    with col_sub:
        val_sub = st.session_state.form_data.get("subtema", "")
        idx_sub = LISTA_SUBTEMAS.index(val_sub) if val_sub in LISTA_SUBTEMAS else 0
        subtema = st.selectbox("Subtema", options=LISTA_SUBTEMAS, index=idx_sub)

    palavras_chave = st.text_input("Palavras-chave", value=st.session_state.form_data["palavras_chave"])
    resumo = st.text_area("Resumo", value=st.session_state.form_data["resumo"], height=150)
    #------------------------------------------------------------------------------------
    # Categoria, Método e Região

    col_cat, col_met = st.columns(2)
    
    with col_cat:
        categoria = st.selectbox(
            "Categoria",
            LISTA_CATEGORIA
        )
    
    with col_met:
        metodo = st.selectbox(
            "Método",
            LISTA_METODO
        )
    
    regiao = st.selectbox(
        "Região",
        LISTA_REGIAO
    )
    
    observacoes = st.text_area(
        "Observações",
        height=120
    )
    # Linha Final
    cv, cl = st.columns(2)
    with cv: doi = st.text_input("Veículo / DOI")
    with cl: link = st.text_input("Link")
    
    submitted = st.form_submit_button("💾 Salvar Documento", use_container_width=True)

# ==========================================================
# SALVAMENTO
# ==========================================================
if submitted:
    if not titulo.strip():
        st.error("O título é obrigatório.")
    elif verificar_duplicidade(titulo, autores):
        st.warning("⚠️ Documento já existe.")
    else:
        try:
            nome_arquivo = ""
            if u_file:
                nome_arquivo = f"{uuid.uuid4()}.pdf"
                with open(PDF_DIR / nome_arquivo, "wb") as f:
                    f.write(u_file.getbuffer())

            inserir_documento(
                titulo=titulo, autores=autores, ano=ano, tipo_documento=tipo_documento,
                instituicao=instituicao, pais=pais, idioma=idioma, tema=tema,
                subtema=subtema, resumo=resumo, palavras_chave=palavras_chave,
                doi=doi, link=link, categoria=categoria, metodo=metodo, regiao=regiao, observacoes=observacoes, arquivo_pdf=nome_arquivo
            )
            
            st.success("✅ Salvo com sucesso!")
            st.session_state.form_data = {k: "" for k in st.session_state.form_data}
            st.session_state.form_data["ano"] = 2025
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")
