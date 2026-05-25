# ==========================================================
# pages/editar.py
# Edição de Documentos
# Biblioteca Digital DMAPU
# ==========================================================

import streamlit as st
from pathlib import Path
import uuid
import pandas as pd

# Importações das funções de banco de dados
# Certifique-se de que estas funções existam em utils/database.py
from utils.database import (
    listar_documentos,
    obter_documento,
    atualizar_documento
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

tipos = ["", "Artigo", "Livro", "Capítulo", "Dissertação", "Tese", "Relatório Técnico", "Nota Técnica", "Legislação", "Manual", "Outro"]
paises = ["", "Brasil", "Portugal", "Estados Unidos", "Reino Unido", "França", "Alemanha", "Espanha", "Itália", "China", "Japão", "Outro"]
idiomas = ["", "Português", "Inglês", "Espanhol", "Francês", "Alemão", "Outro"]
temas = ["", "Planejamento Urbano", "Meio Ambiente", "Mobilidade", "Habitação", "Geoprocessamento", "Legislação", "Outros"]

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
        ano = st.number_input("Ano", min_value=1900, max_value=2100, 
                             value=int(documento.get("ano")) if documento.get("ano") else 2024)

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
        subtema = st.text_input("Subtema", value=documento.get("subtema", ""))

    palavras_chave = st.text_input("Palavras-chave", value=documento.get("palavras_chave", ""))
    resumo = st.text_area("Resumo", value=documento.get("resumo", ""), height=150)

    st.markdown("---")
    st.subheader("Links e Metadados")

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        doi = st.text_input("Veículo de Publicação/DOI", value=documento.get("doi", ""))
    with col_l2:
        link = st.text_input("Link Externo", value=documento.get("link", ""))

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        categoria = st.text_input("Categoria", value=documento.get("categoria", ""))
    with col_m2:
        metodo = st.text_input("Método", value=documento.get("metodo", ""))
    with col_m3:
        regiao = st.text_input("Região", value=documento.get("regiao", ""))

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
            nome_pdf = documento.get("arquivo_pdf") # Mantém o antigo por padrão

            if uploaded_file is not None:
                # Se enviou um novo, gera novo nome e salva
                extensao = uploaded_file.name.split(".")[-1]
                nome_pdf = f"{uuid.uuid4()}.{extensao}"
                caminho_pdf = PDF_DIR / nome_pdf
                
                with open(caminho_pdf, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # 2. Chamar a função de atualização
            # Certifique-se que a ordem dos argumentos bate com sua função em database.py
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
                arquivo_pdf=nome_pdf, # O nome do arquivo (novo ou mantido)
                categoria=categoria,
                metodo=metodo,
                regiao=regiao,
                observacoes=observacoes
            )
            
            st.success("✅ Documento atualizado com sucesso!")
                        
            # Recarregar a página para atualizar os dados na tela
            # st.rerun() # Opcional: reatualiza a página
            
        except Exception as e:
            st.error(f"Erro ao salvar alterações: {e}")

# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")
st.caption("Biblioteca Digital DMAPU • Edição de Documentos")
