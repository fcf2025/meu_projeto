# ==========================================================
# pages/cadastro.py
# Cadastro de Bibliografia
# Biblioteca Digital DMAPU
# ==========================================================

import streamlit as st
from pathlib import Path
import uuid
import pandas as pd
from fpdf import FPDF
# ==========================================================
# IMPORTA FUNÇÕES DO BANCO
# ==========================================================

from utils.database import inserir_documento

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
# TÍTULO
# ==========================================================

st.title("📝 Cadastro de Referências Bibliográficas")

st.markdown("""
Preencha os campos abaixo para inserir um novo documento
na Biblioteca Digital DMAPU.
""")

st.markdown("---")

# ==========================================================
# FORMULÁRIO
# ==========================================================

with st.form("form_cadastro", clear_on_submit=True):

    # ======================================================
    # LINHA 1
    # ======================================================

    col1, col2 = st.columns([3, 1])

    with col1:
        titulo = st.text_input(
            "Título *"
        )

    with col2:
        ano = st.number_input(
            "Ano",
            min_value=1900,
            max_value=2100,
            step=1,
            value=2025
        )

    # ======================================================
    # LINHA 2
    # ======================================================

    autores = st.text_input(
        "Autor(es)"
    )

    # ======================================================
    # LINHA 4
    # ======================================================

    instituicao = st.text_input(
        "Instituição do Autor/Afiliação"
    )


    
    # ======================================================
    # LINHA 3
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        tipo_documento = st.selectbox(
            "Tipo de Documento",
            [
                "",
                "Artigo",
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
                "Outros"
            ]
                                               
    )

    with col2:
        pais = st.selectbox(
            "País",
            [
        "",  # opção vazia no início
        # 🌎 América do Sul
        "Argentina",
        "Bolívia",
        "Brasil",
        "Chile",
        "Colômbia",
        "Equador",
        "Guiana",
        "Paraguai",
        "Peru",
        "Suriname",
        "Uruguai",
        "Venezuela",

        # 🌎 América Central
        "Belize",
        "Costa Rica",
        "El Salvador",
        "Guatemala",
        "Honduras",
        "Nicarágua",
        "Panamá",

        # 🌎 América do Norte
        "Canadá",
        "Estados Unidos",
        "México",

        # 🌍 Europa
        "Alemanha",
        "Áustria",
        "Bélgica",
        "Bulgária",
        "Croácia",
        "Dinamarca",
        "Eslováquia",
        "Eslovênia",
        "Espanha",
        "Estônia",
        "Finlândia",
        "França",
        "Grécia",
        "Hungria",
        "Irlanda",
        "Islândia",
        "Itália",
        "Letônia",
        "Lituânia",
        "Luxemburgo",
        "Malta",
        "Noruega",
        "Países Baixos",
        "Polônia",
        "Portugal",
        "Reino Unido",
        "República Tcheca",
        "Romênia",
        "Suécia",
        "Suíça",

        # 🌏 Ásia
        "Afeganistão",
        "Arábia Saudita",
        "Armênia",
        "Azerbaijão",
        "Bangladesh",
        "Barein",
        "Brunei",
        "Butão",
        "Camboja",
        "Cazaquistão",
        "China",
        "Chipre",
        "Coreia do Norte",
        "Coreia do Sul",
        "Emirados Árabes Unidos",
        "Filipinas",
        "Geórgia",
        "Índia",
        "Indonésia",
        "Irã",
        "Iraque",
        "Israel",
        "Japão",
        "Jordânia",
        "Kuwait",
        "Laos",
        "Líbano",
        "Malásia",
        "Maldivas",
        "Mianmar",
        "Mongólia",
        "Nepal",
        "Omã",
        "Paquistão",
        "Qatar",
        "Singapura",
        "Síria",
        "Sri Lanka",
        "Tailândia",
        "Timor-Leste",
        "Turcomenistão",
        "Turquia",
        "Uzbequistão",
        "Vietnã",
        "Iêmen",

        # 🌍 África
        "África do Sul",
        "Angola",
        "Argélia",
        "Benim",
        "Botsuana",
        "Burquina Faso",
        "Burundi",
        "Cabo Verde",
        "Camarões",
        "Chade",
        "Comores",
        "Congo",
        "Costa do Marfim",
        "Djibuti",
        "Egito",
        "Eritreia",
        "Eswatini",
        "Etiópia",
        "Gabão",
        "Gâmbia",
        "Gana",
        "Guiné",
        "Guiné-Bissau",
        "Guiné Equatorial",
        "Lesoto",
        "Libéria",
        "Líbia",
        "Madagascar",
        "Malawi",
        "Mali",
        "Marrocos",
        "Maurícia",
        "Mauritânia",
        "Moçambique",
        "Namíbia",
        "Níger",
        "Nigéria",
        "Quênia",
        "República Centro-Africana",
        "República Democrática do Congo",
        "Ruanda",
        "São Tomé e Príncipe",
        "Senegal",
        "Serra Leoa",
        "Seicheles",
        "Somália",
        "Sudão",
        "Sudão do Sul",
        "Tanzânia",
        "Togo",
        "Tunísia",
        "Uganda",
        "Zâmbia",
        "Zimbábue",

        # 🌏 Oceania
        "Austrália",
        "Fiji",
        "Nova Zelândia",
        "Papua-Nova Guiné",
        "Samoa",
        "Tonga",
        "Vanuatu",

        # opção genérica
        "Outro"
    ]
) 

    with col3:

        idioma = st.selectbox(
            "Idioma",
            [
                "",
                "Português",
                "Inglês",
                "Espanhol",
                "Francês",
                "Outro"
            ]
        )



    # ======================================================
    # LINHA 5
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        tema = st.selectbox(
            "Tema",
            [
                "",
                "Planejamento e elaboração de Planos de Drenagem e Manejo de Águas Pluviais (PDMP)",
                "Integração entre DMAPU e plano diretor municipal",
                "Zoneamento de risco de inundações e ocupação de áreas críticas",
                "Medidas estruturais de drenagem (bueiros, canais, reservatórios, bacias de detenção)",
                "Infraestrutura verde e soluções baseadas na natureza na drenagem urbana",
                "Modelagem hidrológica e hidráulica de bacias urbanas",
                "Controle de cheias e gestão de eventos pluviais extremos",
                "Gestão integrada de recursos hídricos e DMAPU",
                "Políticas públicas, regulamentação e fiscalização do manejo de águas pluviais",
                "Participação comunitária, educação ambiental e aceitação social de obras de drenagem",
                "Outro"
            ]
    )

    with col2:

        subtema = st.selectbox(
        "Subtema",
        [
            "","Planejamento urbano integrado",
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
            "Outro"
        ]
    )

    # ======================================================
    # LINHA 6
    # ======================================================

    palavras_chave = st.text_input(
        "Palavras-chave"
    )

    # ======================================================
    # LINHA 7
    # ======================================================

    resumo = st.text_area(
        "Resumo",
        height=200
    )

    # ======================================================
    # LINHA 8
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        doi = st.selectbox(
        "Veículo de Publicação/Periódico",
        options=[
            "Revista",
            "Journal",
            "Periódico",
            "Conferência",
            "Livro",
            "Capítulo de Livro",
            "Site",
            "Repositório",
            "Anais de Congresso / Proceedings",
            "Boletim Técnico",
            "Newsletter",
            "Plataforma Digital Acadêmica (ex.: ResearchGate, Academia.edu)",
            "Biblioteca Digital (ex.: BDTD, Scielo, JSTOR)",
            "Base de Dados Estatística (ex.: IBGE, ONU Data)",
            "Documento Oficial / Institucional (ex.: ONU, OMS, IBGE)",
            "Enciclopédia / Dicionário Especializado",
            "Blog Técnico ou Acadêmico",
            "Outro"],
        index=0  # opcional: define qual opção vem selecionada por padrão
    )

    with col2:

        link = st.text_input(
            "Link"
        )

    # ======================================================
    # LINHA 9
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        categoria = st.selectbox(
            "Categoria",
            [
                "",
                "Economia",
                "Legislação",
                "Política Pública",
                "Meio Ambiente",
                "Saúde",
                "Educação",
                "Tecnologia e Inovação",
                "Engenharia",
                "Ciências Sociais",
                "Ciências Naturais",
                "Gestão e Administração",
                "Infraestrutura e Urbanismo",
                "Direitos Humanos",
                "Cultura e Sociedade",
                "Energia",
                "Agricultura e Recursos Naturais",
                "Planejamento Urbano e Regional",
                "Saneamento Básico",
                "Outro"
            ]
        )

    with col2:
        metodo = st.selectbox(
            "Método",
            [
                "",
                "Pesquisa de Campo – coleta de dados diretamente em ambientes reais.",
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
                "Outro"
            ]
        )

    with col3:
        regiao = st.selectbox(
            "Região",
            [
                "",
                "Brasil",
                "América Latina",
                "Europa",
                "América do Norte",
                "Ásia",
                "África",
                "Global",
                "Outro"
            ]
        )

    # ======================================================
    # OBSERVAÇÕES
    # ======================================================

    observacoes = st.text_area(
        "Observações",
        height=100
    )

    # ======================================================
    # UPLOAD PDF
    # ======================================================

    st.markdown("### 📎 Upload de PDF")

    uploaded_file = st.file_uploader(
        "Selecione um PDF",
        type=["pdf"]
    )

    # ======================================================
    # BOTÃO
    # ======================================================

    submitted = st.form_submit_button(
        "💾 Salvar Documento",
        use_container_width=True
    )

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if submitted:

    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    if titulo.strip() == "":

        st.error("O título é obrigatório.")

    else:

        try:

            # ==================================================
            # PDF
            # ==================================================

            nome_pdf = ""

            if uploaded_file is not None:

                extensao = uploaded_file.name.split(".")[-1]

                nome_pdf = (
                    f"{uuid.uuid4()}.{extensao}"
                )

                caminho_pdf = PDF_DIR / nome_pdf

                with open(caminho_pdf, "wb") as f:
                    f.write(uploaded_file.read())

            # ==================================================
            # INSERÇÃO
            # ==================================================

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
            st.toast("Dados atualizados!")

        except Exception as e:

            st.error(
                f"Erro ao salvar documento: {e}"
            )


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")
st.caption(
    "Biblioteca Digital DMAPU • Cadastro de Bibliografia"
)
