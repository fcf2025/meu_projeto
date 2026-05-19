from fpdf import FPDF
from pathlib import Path

def gerar_guia_rapido():
    caminho_pdf = Path("exports/guia_rapido.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(200, 10, "Guia Rápido – Biblioteca Digital DMAPLU", ln=True, align="C")
    pdf.ln(10)

    conteudo_p1 = """O que é?
Sistema para cadastro, consulta e exportação de referências bibliográficas.

Como iniciar?
1. streamlit run app.py
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
    print(f"Guia rápido gerado em: {caminho_pdf}")