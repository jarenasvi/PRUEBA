import pandas as pd

def rename_columns(df, tipo):
    """
    Renombra las columnas del dataset dataset taxa_abandonament.xlsx para que coincida
    con el dataset rendiment_estudiants.xlsx.

    Parámetros
        df: dataset a renombrar.
        tipo: 'abandono'.

    Devuelve:
        Dataset taxa_abandonament.xlsx con columnas renombradas.
    """
    # Copiamos el df
    df = df.copy()

    if tipo == 'abandono':
        # Renombramos las columnas para que coincidan con el dataset de rendimiento
        df.rename(columns={
            'Sexe Alumne': 'Sexe',
            'Naturalesa universitat responsable': 'Tipus universitat',
            'Universitat Responsable': 'Universitat',
            'Tipus de centre': 'Integrat S/N'
        }, inplace=True)
    # En caso contrario devolvemos el df tal cual
    return df


def drop_columns(df, tipo):
    """
    Elimina columnas innecesarias.

    Parámetros:
        df: dataframe al que se quiere eliminar columnas.
        tipo: 'rendiment' o 'abandono'.

    Devuelve:
        Dataframe sin las columnas.
    """
    # Copiamos el dataframe
    df = df.copy()

    # Columnas comunes a eliminar
    columns_to_drop = ['Universitat', 'Unitat']

    # Filtramos por el dataframe indicado y eliminamos las columnas
    if tipo == 'rendiment':
        columns_to_drop += ['Crèdits ordinaris superats', 'Crèdits ordinaris matriculats']

    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

    # Devolvemos el resultado
    return df


def group_by_branch(df, tipo):
    """
    Agrupa el dataset por ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi',
    'Branca', 'Sexe', 'Integrat S/N'] y calcula la media de la métrica relevante.

    Parámetros:
        df: dataframe a agrupar.
        tipo:
            'rendiment': calcula media de 'Taxa rendiment'.
            'abandono': calcula media de '% Abandonament a primer curs'.

    Devuelve
        Dataframe agrupado.
    """
    # Copiamos el df
    df = df.copy()
    # Columnas generales
    group_cols = ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi',
                  'Branca', 'Sexe', 'Integrat S/N']

    # Filtramos para las columnas específicas
    if tipo == 'rendiment':
        metric_col = 'Taxa rendiment'
    elif tipo == 'abandono':
        metric_col = '% Abandonament a primer curs'
    else:
        raise ValueError("tipo debe ser 'rendiment' o 'abandono'")

    # Agrupamos
    grouped = df.groupby(group_cols)[metric_col].mean().reset_index()
    return grouped


def merge_datasets(df_rendiment, df_abandono):
    """
    Fusiona ambos datasets (rendimiento y abandono) solo con filas coincidentes.

    Parámetros:
        df_rendiment
        df_abandono

    Devuelve:
        Dataset fusionado.
    """
    # Columnas comunes
    merge_cols = ['Curs Acadèmic', 'Tipus universitat', 'Sigles', 'Tipus Estudi',
                  'Branca', 'Sexe', 'Integrat S/N']

    merged = pd.merge(df_rendiment, df_abandono, how='inner', on=merge_cols)
    return merged
