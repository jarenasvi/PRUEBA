import pandas as pd

def load_dataset(file_path=None):
    """
    Carga el fichero introducido como parámetro, si está vacío pregunta.

    Parámetros:
        file_path: ruta del archivo

    Devuelve:
        pd.DataFrame
    """
    # Si se pasa un path, cargamos directamente
    if file_path:
        return pd.read_excel(file_path)

    # Si no, preguntamos al usuario qué dataset cargar
    print("¿Qué dataset quieres cargar?")
    print("1 = Tasa de rendimiento")
    print("2 = Tasa de abandono")

    option = input("Introduce 1 o 2: ")

    if option == "1":
        return pd.read_excel("data/rendiment_estudiants.xlsx")
    if option == "2":
        return pd.read_excel("data/taxa_abandonament.xlsx")

    # Si la opción es incorrecta
    raise ValueError("Opción no válida")