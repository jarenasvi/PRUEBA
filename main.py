from src.modules.data_loader import load_dataset
from src.modules.eda import show_head, show_columns, show_info
from src.modules.cleaning import rename_columns, drop_columns, group_by_branch, merge_datasets
from src.modules.visualization import plot_temporal
from src.modules.analysis import analyze_dataset



def main():
    # -------------- EJERCICIO 1 --------------
    df = load_dataset() # Formato: "data/file_name.xlsx"
    show_head(df)
    show_columns(df)
    show_info(df)

    # -------------- EJERCICIO 2 --------------
    # Cargamos los datasets
    df_rendiment = load_dataset("data/rendiment_estudiants.xlsx")
    df_abandono = load_dataset("data/taxa_abandonament.xlsx")

    # Renombramos columnas
    df_rendiment = rename_columns(df_rendiment, 'rendiment')
    df_abandono = rename_columns(df_abandono, 'abandono')

    # Eliminamos columnas
    df_rendiment = drop_columns(df_rendiment, 'rendiment')
    df_abandono = drop_columns(df_abandono, 'abandono')

    # Agrupamos por rama
    df_rendiment = group_by_branch(df_rendiment, 'rendiment')
    df_abandono = group_by_branch(df_abandono, 'abandono')

    # Fusionamos datasets
    df_merged = merge_datasets(df_rendiment, df_abandono)

    # Mostramos información
    show_head(df_merged)
    show_columns(df_merged)
    show_info(df_merged)

    # -------------- EJERCICIO 3 --------------
    plot_temporal(df_merged)

    # -------------- EJERCICIO 4 --------------
    analyze_dataset(df_merged)

if __name__ == "__main__":
    main()