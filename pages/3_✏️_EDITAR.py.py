# ==========================================================
# pages/editar.py
# Edição de Documentos
# Biblioteca Digital DMAPU
# ==========================================================

import streamlit as st
from pathlib import Path
import uuid
from sqlalchemy import text
# ==========================================================
# IMPORTS
# ==========================================================

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

# ==========================================================
# CAMINHOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "pdfs"

PDF_DIR.mkdir(exist_ok=True)

# ==========================================================
# TÍTULO
# ==========================================================

st.title("✏️ Editar Documento")

st.markdown("""
Atualize os dados bibliográficos cadastrados.
""")

st.markdown("---")

# ==========================================================
# LISTA DOCUMENTOS
# ==========================================================

df_docs = listar_documentos()

# ==========================================================
# VERIFICA DOCUMENTOS
# ==========================================================

if len(df_docs) == 0:

    st.warning(
        "Nenhum documento cadastrado."
    )

    st.stop()

# ==========================================================
# SELEÇÃO DOCUMENTO
# ==========================================================

documentos_dict = {
    f"{row['id']} - {row['titulo']}": row["id"]
    for _, row in df_docs.iterrows()
}

selecionado = st.selectbox(
    "Selecione o documento",
    list(documentos_dict.keys())
)

doc_id = documentos_dict[selecionado]

# ==========================================================
# CARREGAR DOCUMENTO
# ==========================================================

documento = obter_documento(doc_id)

# ==========================================================
# FORMULÁRIO
# ==========================================================

with st.form(
    "form_edicao"
):

# ======================================================
# LINHA 1
# ======================================================

    col1, col2 = st.columns([3, 1])

    with col1:

        titulo = st.text_input(
            "Título *",
            value=documento["titulo"]
        )
    with col2:
        ano = st.number_input(
            "Ano",
            min_value=1900,
            max_value=2100,
            value=int(
                documento["ano"]
            ) if documento["ano"] else 2025
        )
    # ======================================================
    # AUTORES
    # ======================================================
    autores = st.text_input(
        "Autores",
        value=documento["autores"]
    )
    # ======================================================
    # INSTITUIÇÃO
    # ======================================================

    instituicao = st.text_input(
        "Instituição",
        value=documento["instituicao"]
    )
with st.form("form_edicao"):
    # ======================================================
    # TIPO / PAÍS / IDIOMA
    # ======================================================
    col1, col2, col3 = st.columns(3)

    tipos = [
        "",
        "Artigo",
        "Livro",
        "Capítulo",
        "Dissertação",
        "Tese",
        "Relatório Técnico",
        "Nota Técnica",
        "Legislação",
        "Manual",
        "Outro"
    ]

    paises = [
        "",
        "Brasil",
        "Portugal",
        "Estados Unidos",
        "Reino Unido",
        "França",
        "Alemanha",
        "Espanha",
        "Itália",
        "China",
        "Japão",
        "Outro"
    ]

    idiomas = [
        "",
        "Português",
        "Inglês",
        "Espanhol",
        "Francês",
        "Alemão",
        "Outro"
    ]

    with col1:
        tipo_documento = st.selectbox("Tipo de Documento", tipos)

    with col2:
        pais = st.selectbox("País", paises)

    with col3:
        idioma = st.selectbox("Idioma", idiomas)

    # Botão de envio (última linha do formulário)
    salvar = st.form_submit_button("Salvar alterações")

# Fora do formulário, você processa o resultado
if salvar:
    atualizar_documento(
        doc_id,
        titulo,
        autores,
        ano,
        instituicao,
        tipo_documento,
        pais,
        idioma,
        tema,
        subtema,
        resumo,
        palavras_chave,
        doi,
        link,
        nome_pdf,
        categoria,
        metodo,
        regiao,
        observacoes
    )
    st.success("Documento atualizado com sucesso!")

    # ======================================================
    # TEMA
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        tema = st.selectbox(
            "Tema",
            temas,
            index=(
                temas.index(
                    documento["tema"]
                )
                if documento["tema"] in temas
                else 0
            )
        )

    with col2:

        subtema = st.text_input(
            "Subtema",
            value=documento["subtema"]
        )

    # ======================================================
    # PALAVRAS-CHAVE
    # ======================================================

    palavras_chave = st.text_input(
        "Palavras-chave",
        value=documento["palavras_chave"]
    )

    # ======================================================
    # RESUMO
    # ======================================================

    resumo = st.text_area(
        "Resumo",
        value=documento["resumo"],
        height=200
    )

    # ======================================================
    # DOI / LINK
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        doi = st.text_input(
            "Veículo de Publicação/Periódico",
            value=documento["doi"]
        )

    with col2:

        link = st.text_input(
            "Link",
            value=documento["link"]
        )

    # ======================================================
    # CATEGORIA / MÉTODO / REGIÃO
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        categoria = st.text_input(
            "Categoria",
            value=documento["categoria"]
        )

    with col2:

        metodo = st.text_input(
            "Método",
            value=documento["metodo"]
        )

    with col3:

        regiao = st.text_input(
            "Região",
            value=documento["regiao"]
        )

    # ======================================================
    # OBSERVAÇÕES
    # ======================================================

    observacoes = st.text_area(
        "Observações",
        value=documento["observacoes"],
        height=100
    )

    # ======================================================
    # PDF
    # ======================================================

    st.markdown("### 📎 Atualizar PDF")

    uploaded_file = st.file_uploader(
        "Selecionar novo PDF",
        type=["pdf"]
    )

    # ======================================================
    # BOTÃO
    # ======================================================

    salvar = st.form_submit_button(
        "💾 Salvar Alterações",
        use_container_width=True
    )

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if salvar:
    try:
        nome_pdf = documento["arquivo_pdf"]
        # aqui você pode salvar o PDF ou processar
    except Exception as e:
        st.error(f"Erro ao salvar documento: {e}")

   # ==================================================
   # NOVO PDF
   # ==================================================

        if uploaded_file is not None:

            extensao = (
                uploaded_file.name
                .split(".")[-1]
            )

            nome_pdf = (
                f"{uuid.uuid4()}.{extensao}"
            )

            caminho_pdf = PDF_DIR / nome_pdf

            with open(
                caminho_pdf,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.read()
                )

# ==========================================================
# ATUALIZAR DOCUMENTO
# ==========================================================
nome_pdf = None  # ou "" se preferir
def atualizar_documento(
    doc_id,
    titulo,
    autores,
    ano,
    instituicao,
    tipo_documento,
    pais,
    idioma,
    tema,
    subtema,
    resumo,
    palavras_chave,
    doi,
    link,
    arquivo_pdf,
    categoria,
    metodo,
    regiao,
    observacoes
):
    """
    Atualiza documento existente usando SQLAlchemy
    """
    with conectar_db() as conn:
        query = text("""
            UPDATE bibliografia
            SET
                titulo = :titulo,
                autores = :autores,
                ano = :ano,
                instituicao = :instituicao,
                tipo_documento = :tipo_documento,
                pais = :pais,
                idioma = :idioma,
                tema = :tema,
                subtema = :subtema,
                resumo = :resumo,
                palavras_chave = :palavras_chave,
                doi = :doi,
                link = :link,
                arquivo_pdf = :arquivo_pdf,
                categoria = :categoria,
                metodo = :metodo,
                regiao = :regiao,
                observacoes = :observacoes
            WHERE id = :id
        """)

        conn.execute(query, {
            "titulo": titulo,
            "autores": autores,
            "ano": ano,
            "instituicao": instituicao,
            "tipo_documento": tipo_documento,
            "pais": pais,
            "idioma": idioma,
            "tema": tema,
            "subtema": subtema,
            "resumo": resumo,
            "palavras_chave": palavras_chave,
            "doi": doi,
            "link": link,
            "arquivo_pdf": arquivo_pdf,
            "categoria": categoria,
            "metodo": metodo,
            "regiao": regiao,
            "observacoes": observacoes,
            "id": doc_id
        })
        conn.commit()
# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption(
    "Biblioteca Digital DMAPU • Edição de Documentos"
)
