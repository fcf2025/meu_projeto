# ==========================================================
# pages/editar.py
# Edição de Documentos
# Biblioteca Digital DMAPU
# ==========================================================

import streamlit as st
from pathlib import Path
import uuid
import pandas as pd
from sqlalchemy import text
# Importações das funções de banco de dados
# Certifique-se de que estas funções existam em utils/database.py
from utils.database import (
    listar_documentos,
    obter_documento,
    atualizar_documento,
    conectar_db  # certifique-se que essa função retorna a conexão SQLAlchemy
)

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Editar Documento",
    page_icon="✏️",
    layout="wide"
)

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "pdfs"
PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# LISTA E SELEÇÃO DE DOCUMENTOS
# ==========================================================

st.title("✏️ Editar Documento")
st.markdown("Atualize os dados bibliográficos cadastrados.")
st.markdown("---")

df_docs = listar_documentos()

if df_docs.empty:
    st.warning("Nenhum documento cadastrado no banco de dados.")
    st.stop()

# Criar dicionário para o selectbox: "ID - Título" -> ID
documentos_dict = {
    f"{row['id']} - {row['titulo']}": row["id"]
    for _, row in df_docs.iterrows()
}

selecionado_label = st.selectbox(
    "Selecione o documento para editar",
    options=list(documentos_dict.keys())
)

doc_id = documentos_dict[selecionado_label]

# Carregar dados atuais do documento selecionado
documento = obter_documento(doc_id)
if documento is None:

    st.error(
        "Documento não encontrado."
    )

    st.stop()

# ==========================================================
# DEFINIÇÃO DE OPÇÕES (LISTAS)
# ==========================================================

tipos = ["",    "Artigo",
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
                "Outros", "Outro"]
paises = ["", "Brasil", "Portugal", "Estados Unidos", "Reino Unido", "França", "Alemanha", "Espanha", "Itália", "China", "Japão", "Outro"]
idiomas = ["", "Português", "Inglês", "Espanhol", "Francês", "Alemão", "Outro"]
temas = ["",    "Planejamento e elaboração de Planos de Drenagem e Manejo de Águas Pluviais (PDMP)",
                "Integração entre DMAPU e plano diretor municipal",
                "Zoneamento de risco de inundações e ocupação de áreas críticas",
                "Medidas estruturais de drenagem (bueiros, canais, reservatórios, bacias de detenção)",
                "Infraestrutura verde e soluções baseadas na natureza na drenagem urbana",
                "Modelagem hidrológica e hidráulica de bacias urbanas",
                "Controle de cheias e gestão de eventos pluviais extremos",
                "Gestão integrada de recursos hídricos e DMAPU",
                "Políticas públicas, regulamentação e fiscalização do manejo de águas pluviais",
                "Participação comunitária, educação ambiental e aceitação social de obras de drenagem",
                "Financiamento","Tarifa (taxas de drenagem)","Outro"]

veiculos = ["","Revista",
            "Journal",
            "Periódico",
            "Conferência",
            "Livro",
            "Capítulo de Livro","Financiamento", "Tarifa (Taxas de drenagem)", "Custos (Operacionais e de Implantação)","Taxas","Regulação e Governança","Soluções Baseadas na Natureza (SbN) e Infraestrutura Verde",
                "Planejamento Urbano e Uso do Solo","Sustentabilidade e Mudanças Climáticas","Tecnologias de Monitoramento", "Cidades Inteligentes (Smart Cities)",                    
                "Investimentos em DMAPU","Cidades Inteligentes","Outro"
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
            "Outro"]
categorias = ["","Regulação e Governança",
                "Sustentabilidade Financeira",
                "Infraestrutura e Engenharia",
                "Soluções Baseadas na Natureza (SbN)",
                "Planejamento Urbano e Territorial",
                "Mudanças Climáticas e Resiliência",
                "Operação e manutenção",
                "Tecnologia e Monitoramento",
                "Outro"]
metodos = ["", "Pesquisa de Campo – coleta de dados diretamente em ambientes reais.",
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
regioes = ["", "Brasil",
                "América Latina",
                "Europa",
                "América do Norte",
                "Ásia",
                "África",
                "Global",
                "Outro"]
subtemas = ["","Planejamento urbano integrado",
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
            "Taxa de drenagem urbana","Outros"]

# Funções auxiliares para encontrar o índice atual nos selects
def get_index(lista, valor):
    try:
        return lista.index(valor) if valor in lista else 0
    except:
        return 0

# ==========================================================
# FORMULÁRIO DE EDIÇÃO
# ==========================================================

with st.form("form_edicao"):
    st.subheader("Informações Básicas")
    
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        titulo = st.text_input("Título *", value=documento.get("titulo", ""))
    with col_t2:
        # Criamos uma lista de anos de 2030 até 2000
        lista_anos = list(range(2030, 2000, -1))
        
        ano = st.selectbox(
            "Ano",
            options=lista_anos,
            index=5 # Isso define o ano 2025 como padrão (posições: 2030=0, 2029=1...)
        )

    autores = st.text_input("Autores", value=documento.get("autores", ""))
    instituicao = st.text_input("Instituição", value=documento.get("instituicao", ""))

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        tipo_documento = st.selectbox("Tipo de Documento", tipos, index=get_index(tipos, documento.get("tipo_documento")))
    with col_f2:
        pais = st.selectbox("País", paises, index=get_index(paises, documento.get("pais")))
    with col_f3:
        idioma = st.selectbox("Idioma", idiomas, index=get_index(idiomas, documento.get("idioma")))

    st.markdown("---")
    st.subheader("Classificação e Conteúdo")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        tema = st.selectbox("Tema", temas, index=get_index(temas, documento.get("tema")))
    with col_c2:
        subtema = st.selectbox("Subtema", subtemas, index=get_index(subtemas, documento.get("subtema")))

    palavras_chave = st.text_input("Palavras-chave", value=documento.get("palavras_chave", ""))
    resumo = st.text_area("Resumo", value=documento.get("resumo", ""), height=150)

    st.markdown("---")
    st.subheader("Links e Metadados")

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        doi = st.selectbox("Veículo de Publicação", veiculos, index=get_index(veiculos, documento.get("doi")))
    with col_l2:
        link = st.text_input("Link Externo", value=documento.get("link", ""))

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        categoria = st.selectbox("Categoria", categorias, index=get_index(categorias, documento.get("categoria")))
    with col_m2:
         metodo = st.selectbox("Método", metodos, index=get_index(metodos, documento.get("metodo")))
    with col_m3:
        regiao = st.selectbox("Região", regioes, index=get_index(regioes, documento.get("regiao")))

    observacoes = st.text_area("Observações", value=documento.get("observacoes", ""), height=100)

    st.markdown("---")
    st.subheader("📎 Atualizar PDF")
    st.info(f"PDF atual: {documento.get('arquivo_pdf') if documento.get('arquivo_pdf') else 'Nenhum arquivo anexado'}")
    uploaded_file = st.file_uploader("Selecionar novo PDF (substituirá o atual)", type=["pdf"])

    # Botão de Envio dentro do formulário
    salvar = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)

# ==========================================================
# PROCESSAMENTO DO FORMULÁRIO
# ==========================================================

if salvar:
    if not titulo:
        st.error("O campo Título é obrigatório.")
    else:
        try:
            # 1. Gerenciar o PDF
            nome_pdf = documento.get("arquivo_pdf")  # Mantém o antigo por padrão

            if uploaded_file is not None:
                extensao = uploaded_file.name.split(".")[-1]
                nome_pdf = f"{uuid.uuid4()}.{extensao}"
                caminho_pdf = PDF_DIR / nome_pdf

                with open(caminho_pdf, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # 2. Atualizar no banco
            atualizar_documento(
                doc_id=doc_id,
                titulo=titulo,
                autores=autores,
                ano=ano,
                instituicao=instituicao,
                tipo_documento=tipo_documento,
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

            st.success("✅ Documento atualizado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar alterações: {e}")

# ==========================================================
# BOTÃO DE EXCLUSÃO DE DOCUMENTO
# ==========================================================

st.markdown("---")
st.subheader("🗑️ Excluir Documento")

confirmar_exclusao = st.checkbox("Confirmar exclusão deste documento")

if confirmar_exclusao:
    if st.button("Excluir este documento", use_container_width=True):
        try:
            # Remover PDF físico, se existir
            arquivo_pdf = documento.get("arquivo_pdf")
            if arquivo_pdf:
                caminho_pdf = PDF_DIR / arquivo_pdf
                if caminho_pdf.exists():
                    caminho_pdf.unlink()

            # Remover registro no banco (SQLAlchemy + PostgreSQL)
            conn = conectar_db()
            with conn.begin():
                conn.execute(
                    text("DELETE FROM bibliografia WHERE id = :id"),
                    {"id": doc_id}
                )

            st.success("📌 Documento excluído com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao excluir documento: {e}")

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")
st.caption("Biblioteca Digital DMAPU • Edição de Documentos")
