# ==========================================================
# app.py
# Biblioteca Digital DMAPLU
# ==========================================================

import streamlit as st
from fpdf import FPDF
from pathlib import Path
import pandas as pd
from utils.database import (
    criar_tabela,
    listar_documentos,
    estatisticas_gerais
)
from sqlalchemy import text
from utils.database import estatisticas_gerais
from utils.database import conectar_db
from io import BytesIO
# ==========================================================
# EXPORTS
# ==========================================================

EXPORT_DIR = Path(__file__).parent / "exports"

# ==========================================================
# CRIA TABELA
# ==========================================================

criar_tabela()

# st.success("Tabela criada com sucesso!")
# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Biblioteca DMAPU",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)
#===========================================================
try:

    # conn = conectar_db()
    # st.success("Sistema iniciado com sucesso.")
    st.success("SISTEMA INICIADO")

except Exception as e:

    st.error(e)
# ==========================================================
EXPORT_DIR = Path(__file__).parent / "exports"
FONT_DIR = Path(__file__).parent / "fonts"
EXPORT_DIR.mkdir(exist_ok=True)
FONT_DIR.mkdir(exist_ok=True)

def gerar_guia_rapido():
    caminho_pdf = EXPORT_DIR / "guia_rapido.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Fonte Unicode
    pdf.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"), uni=True)
    pdf.set_font("DejaVu", size=12)

    pdf.cell(200, 10, "Guia Rápido – Biblioteca Digital DMAPU", ln=True, align="C")
    pdf.ln(10)

    conteudo_p1 = """O que é?
Sistema para cadastro, consulta e exportação de referências bibliográficas.

Como iniciar?
1. streamlit run BD_DMAPU.py
2. Acesse http://localhost:8501

Estrutura de Pastas:
- /database → bibliografia.db
- /pdfs → PDFs enviados
- /exports → arquivos exportados
"""
    pdf.multi_cell(0, 10, conteudo_p1)

    pdf.add_page()
    conteudo_p2 = """Funcionalidades Essenciais:

Cadastro:
- Preencha os campos obrigatórios
- Upload de PDF
- Salvar Documento

Consulta:
- Filtros por tema, país, idioma
- Resultados em tabela

Estatísticas:
- Indicadores do acervo

Exportação:
- Excel (.xlsx) e PDF (.pdf) em /exports

Boas Práticas:
- Preencher título
- Usar palavras-chave
- Exportar regularmente
"""
    pdf.multi_cell(0, 10, conteudo_p2)

    pdf.output(str(caminho_pdf))
    return caminho_pdf


# ==========================================================
# CSS MENU LATERAL
# ==========================================================

st.markdown("""
<style>

/* sidebar */
section[data-testid="stSidebar"] {
    width: 280px !important;
}

/* links das páginas */
section[data-testid="stSidebarNav"] a {
    font-weight: 900 !important;
}

/* texto dos links */
section[data-testid="stSidebarNav"] span {
    font-weight: 900 !important;
    font-size: 20px !important;
}

/* hover */
section[data-testid="stSidebarNav"] a:hover {
    background-color: #dfe6f3 !important;
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)
# ==========================================================
# CAMINHOS
# ==========================================================

BASE_DIR = Path(__file__).parent

DB_DIR = BASE_DIR / "database"

DB_PATH = DB_DIR / "bibliografia.db"

PDF_DIR = BASE_DIR / "pdfs"
EXPORT_DIR = BASE_DIR / "exports"

# ==========================================================
# CRIAR DIRETÓRIOS
# ==========================================================

DB_DIR.mkdir(exist_ok=True)

PDF_DIR.mkdir(exist_ok=True)

EXPORT_DIR.mkdir(exist_ok=True)

# ==========================================================
# INICIALIZAÇÃO DO BANCO
# ==========================================================

criar_tabela()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image("logo_ANA.png", width=120)
    st.write("Processo nº 02501.005102/2025-00")
    st.markdown("---")

    st.markdown("""
    ### Biblioteca Digital
    ### Dados abertos, Acesso Público
    - Drenagem Urbana
    - Manejo de Águas Pluviais
    - Tarifação
    - Infraestrutura Verde
    - Regulação
    - Economia Urbana
   
    """)
    
    st.markdown("---")

    # st.success("Sistema iniciado com sucesso.")

# ==========================================================
# GUIA RÁPIDO PDF
# ==========================================================
with st.sidebar:
    # st.markdown("### 📘 Guia Rápido")
    caminho_pdf = gerar_guia_rapido()

    with open(caminho_pdf, "rb") as f:
        st.download_button(
            label="⬇️ Baixar Guia Rápido (PDF)",
            data=f,
            file_name="guia_rapido.pdf",
            mime="application/pdf"
        )




# ==========================================================
# CABEÇALHO PRINCIPAL
# ==========================================================

st.title("📚 Biblioteca Digital DMAPU")

st.markdown("""
Bem-vindo ao sistema de gerenciamento bibliográfico sobre
**Drenagem e Manejo de Águas Pluviais Urbanas (DMAPU)**.

O sistema permitirá:

- cadastro de referências;
- upload de PDFs;
- buscas avançadas;
- filtros temáticos;
- estatísticas do acervo;
- exportação bibliográfica.
""")

# ==========================================================
# INDICADORES
# ==========================================================

try:

    stats = estatisticas_gerais()

    total_docs = stats["total_documentos"]
    total_temas = stats["total_temas"]
    total_paises = stats["total_paises"]

except Exception as e:

    st.error(
        f"Erro ao carregar indicadores: {e}"
    )

    total_docs = 0
    total_temas = 0
    total_paises = 0

# ==========================================================
# MÉTRICAS
# ==========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="Documentos",
        value=total_docs
    )

with col2:

    st.metric(
        label="Temas",
        value=total_temas
    )

with col3:

    st.metric(
        label="Países",
        value=total_paises
    )
# ==========================================================
# ÁREA CENTRAL
# ==========================================================

st.markdown("---")

st.subheader("📖 Últimos documentos cadastrados")

#conn = conectar_db()

try:

    df_docs = listar_documentos()

    if len(df_docs) > 0:

        st.dataframe(
            df_docs.head(10),
            use_container_width=True
        )

    else:

        st.info("Nenhum documento cadastrado.")

except Exception as e:

    st.error(f"Erro ao carregar dados: {e}")

finally:
    pass
  
# ==========================================================
# EXPORTAÇÃO DE DADOS
# ==========================================================

st.markdown("### 📤 Exportar Acervo Completo")

col1, col2 = st.columns(2)

with col1:
    export_excel = st.button("📊 Exportar para Excel")
with col1:
    st.markdown(
    "<h5>* Todos os dados do acervo serão exportados para Excel (.xlsx)</h5>",
    unsafe_allow_html=True
)


# ==========================================================
# FUNÇÕES DE EXPORTAÇÃO
# ==========================================================

def exportar_excel():
   
    try:
        # 2. Conecta ao banco
        conn = conectar_db()
        
        # 3. Lê os dados
        query = "SELECT * FROM bibliografia"
        df = pd.read_sql(query, conn)
        
        # 4. Cria o arquivo Excel em memória
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados')
        
        # 5. Botão de download no Streamlit
        st.download_button(
            label="📥 Baixar Excel",
            data=output.getvalue(),
            file_name="bibliografia_digital.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        if hasattr(conn, 'close'):
            conn.close()
            
    except Exception as e:
        st.error(f"Erro ao exportar: {e}")



# ==========================================================
# PROCESSAMENTO DE EXPORTAÇÃO
# ==========================================================

if export_excel:
    exportar_excel()


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown("---")

st.caption(
    "Biblioteca Digital DMAPU • Versão 0.1"
)
