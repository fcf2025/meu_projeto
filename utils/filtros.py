# ==========================================================
# utils/filtros.py
# Funções auxiliares de filtros
# Biblioteca Digital DMAPLU
# ==========================================================

import pandas as pd

# ==========================================================
# FILTRAR POR TEXTO
# ==========================================================

def filtrar_texto(
    df,
    coluna,
    texto
):
    """
    Filtra DataFrame por texto
    """

    if texto is None or texto == "":
        return df

    return df[
        df[coluna]
        .astype(str)
        .str.contains(
            texto,
            case=False,
            na=False
        )
    ]

# ==========================================================
# FILTRAR POR VALOR EXATO
# ==========================================================

def filtrar_valor(
    df,
    coluna,
    valor
):
    """
    Filtra por igualdade
    """

    if valor is None or valor == "":
        return df

    return df[
        df[coluna] == valor
    ]

# ==========================================================
# FILTRAR POR LISTA
# ==========================================================

def filtrar_lista(
    df,
    coluna,
    lista_valores
):
    """
    Filtra DataFrame usando lista
    """

    if (
        lista_valores is None
        or len(lista_valores) == 0
    ):
        return df

    return df[
        df[coluna]
        .isin(lista_valores)
    ]

# ==========================================================
# FILTRAR POR INTERVALO DE ANOS
# ==========================================================

def filtrar_intervalo_anos(
    df,
    coluna,
    ano_inicial=None,
    ano_final=None
):
    """
    Filtra intervalo de anos
    """

    resultado = df.copy()

    if ano_inicial is not None:

        resultado = resultado[
            resultado[coluna] >= ano_inicial
        ]

    if ano_final is not None:

        resultado = resultado[
            resultado[coluna] <= ano_final
        ]

    return resultado

# ==========================================================
# FILTRAR POR PALAVRAS-CHAVE
# ==========================================================

def filtrar_palavras_chave(
    df,
    coluna,
    palavras
):
    """
    Busca múltiplas palavras
    """

    if palavras is None or palavras == "":
        return df

    lista = [
        p.strip()
        for p in palavras.split(",")
    ]

    mascara = False

    for palavra in lista:

        mascara |= (
            df[coluna]
            .astype(str)
            .str.contains(
                palavra,
                case=False,
                na=False
            )
        )

    return df[mascara]

# ==========================================================
# ORDENAR DATAFRAME
# ==========================================================

def ordenar_dataframe(
    df,
    coluna,
    crescente=True
):
    """
    Ordena DataFrame
    """

    if coluna not in df.columns:
        return df

    return df.sort_values(
        by=coluna,
        ascending=crescente
    )

# ==========================================================
# PAGINAÇÃO
# ==========================================================

def paginar_dataframe(
    df,
    pagina=1,
    itens_por_pagina=20
):
    """
    Retorna página do DataFrame
    """

    inicio = (
        (pagina - 1)
        * itens_por_pagina
    )

    fim = inicio + itens_por_pagina

    return df.iloc[inicio:fim]

# ==========================================================
# OBTER VALORES ÚNICOS
# ==========================================================

def valores_unicos(
    df,
    coluna
):
    """
    Retorna valores únicos ordenados
    """

    if coluna not in df.columns:
        return []

    valores = (
        df[coluna]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    valores = sorted(valores)

    return valores

# ==========================================================
# FILTRO COMBINADO
# ==========================================================

def aplicar_filtros(
    df,
    texto=None,
    tema=None,
    pais=None,
    ano_inicial=None,
    ano_final=None
):
    """
    Aplica múltiplos filtros
    """

    resultado = df.copy()

    # ======================================================
    # TEXTO
    # ======================================================

    if texto:

        colunas_busca = [
            "titulo",
            "autores",
            "resumo",
            "palavras_chave"
        ]

        mascara = False

        for col in colunas_busca:

            if col in resultado.columns:

                mascara |= (
                    resultado[col]
                    .astype(str)
                    .str.contains(
                        texto,
                        case=False,
                        na=False
                    )
                )

        resultado = resultado[mascara]

    # ======================================================
    # TEMA
    # ======================================================

    if tema and "tema" in resultado.columns:

        resultado = resultado[
            resultado["tema"] == tema
        ]

    # ======================================================
    # PAÍS
    # ======================================================

    if pais and "pais" in resultado.columns:

        resultado = resultado[
            resultado["pais"] == pais
        ]

    # ======================================================
    # ANOS
    # ======================================================

    if "ano" in resultado.columns:

        if ano_inicial is not None:

            resultado = resultado[
                resultado["ano"] >= ano_inicial
            ]

        if ano_final is not None:

            resultado = resultado[
                resultado["ano"] <= ano_final
            ]

    return resultado

# ==========================================================
# RESUMO ESTATÍSTICO
# ==========================================================

def resumo_dataframe(df):
    """
    Retorna resumo estatístico simples
    """

    resumo = {
        "linhas": len(df),
        "colunas": len(df.columns),
        "colunas_numericas": len(
            df.select_dtypes(
                include=["number"]
            ).columns
        ),
        "colunas_texto": len(
            df.select_dtypes(
                include=["object"]
            ).columns
        )
    }

    return resumo