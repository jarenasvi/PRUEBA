import pandas as pd
pd.set_option('display.max_columns', None)

def show_head(df):
    """
    Muestra las 5 primeras filas del DataFrame.

    Parámetros:
        df: dataframe de los datos

    Devuelve:
        Muestra por pantalla las 5 primeras filas.
    """
    print("\nPrimeras 5 filas:")
    print(df.head())


def show_columns(df):
    """
    Muestra las columnas del DataFrame.

    Parámetros:
        df: dataframe de los datos

    Devuelve:
        Muestra por pantalla las columnas.
    """
    print("\nColumnas:")
    print(df.columns)


def show_info(df):
    """
    Muestra la información del DataFrame.

    Parámetros:
        df: dataframe de los datos

    Devuelve:
        Muestra la información del dataframe.
    """
    print("\nInfo:")
    df.info()