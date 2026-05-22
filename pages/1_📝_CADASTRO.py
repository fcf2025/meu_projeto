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
        "Autores"
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
    # LINHA 4
    # ======================================================

    instituicao = st.text_input(
        "Instituição do Autor/Afiliação"
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
                "Governança e Regulação",
                "Políticas Públicas",
                "Gestão Participativa",
                "Instrumentos de Controle Social",
                "Normas Técnicas e Padrões",
                
                "Barreiras e Desafios",
                "Conflitos Socioambientais",
                "Limitações Financeiras",
                "Desafios Tecnológicos",
                "Aceitação Social",
              
                "Planejamento Urbano", 
                "Mobilidade Urbana",
                "Uso e Ocupação do Solo",
                "Expansão Urbana",
                "Resiliência das Cidades",
                
                "Economia e Tarifação",
                "Modelos de Financiamento",
                "Custos Operacionais",
                "Subsídios e Incentivos",
                "Economia Circular",
                
                "Engenharia de Drenagem",
                "Controle de Cheias",
                "Sistemas de Retenção",
                "Tecnologias de Tratamento",
                "Modelagem Hidrológica",
                
                "Sustentabilidade Urbana",
                "Métodos Analíticos",
                "Infraestrutura Verde",
                "Mudanças Climáticas",
                "Outro"
            ]
        )

    with col2:

        subtema = st.selectbox(
        "Subtema",
        [
            "",
            "Planejamento Urbano",
            "Gestão de Recursos Hídricos",
            "Políticas Públicas",
            "Tecnologias de Monitoramento",
            "Modelagem Hidrológica",
            "Infraestrutura Verde",
            "Educação Ambiental",
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
        options=["Revista", "Journal", "Periódico", "Conferência", "Livro", "Capítulo de Livro", "Site","Repositório","Outro"],
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
                "Artigo Científico",
                "Livro",
                "Relatório Técnico",
                "Nota Técnica",
                "Legislação",
                "Manual",
                "Outro"
            ]
        )

    with col2:
        metodo = st.selectbox(
            "Método",
            [
                "",
                "Modelagem Hidrológica",
                "Simulação Computacional",
                "Estudo de Caso",
                "Revisão Bibliográfica",
                "Análise Estatística",
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
