import pandas as pd
from datetime import datetime
from scipy.stats import pearsonr, linregress
import os
import json

def analyze_dataset(merged_df):
    """
    Realiza un análisis estadístico del dataset fusionado y genera un JSON
    con la metadata, estadísticas globales , análisis por rama y rankings.

    Parámetros:
        merged_df: dataframe fusionado.

    Devuelve:
        Genera el JSON.
    """
    # APARTADO METADATA
    metadata = {
        "fecha_analisis": datetime.now().strftime("%Y-%m-%d"),
        "num_registros": len(merged_df),
        "periodo_temporal": sorted(merged_df['Curs Acadèmic'].unique())
    }

    # ESTADÍSTICAS GLOBALES
    # Calculamos las métricas
    abandono_medio = merged_df['% Abandonament a primer curs'].mean()
    rendimiento_medio = merged_df['Taxa rendiment'].mean()
    corr, _ = pearsonr(
        merged_df['% Abandonament a primer curs'].dropna(),
        merged_df['Taxa rendiment'].dropna()
    )

    estadisticas_globales = {
        "abandono_medio": abandono_medio,
        "rendimiento_medio": rendimiento_medio,
        "correlacion_abandono_rendimiento": corr
    }

    # ANÁLISIS POR RAMA
    # Seleccionamos las ramas que hay y creamos el diccionario vacío
    ramas = merged_df['Branca'].unique()
    analisis_por_rama = {}

    for rama in ramas:
        branch_data = merged_df[merged_df['Branca'] == rama]

        # Estadísticas básicas
        abandono_mean = branch_data['% Abandonament a primer curs'].mean()
        abandono_std = branch_data['% Abandonament a primer curs'].std()
        abandono_min = branch_data['% Abandonament a primer curs'].min()
        abandono_max = branch_data['% Abandonament a primer curs'].max()

        rendimiento_mean = branch_data['Taxa rendiment'].mean()
        rendimiento_std = branch_data['Taxa rendiment'].std()
        rendimiento_min = branch_data['Taxa rendiment'].min()
        rendimiento_max = branch_data['Taxa rendiment'].max()

        # Agrupamos los datos por año académico
        branch_by_year = branch_data.groupby('Curs Acadèmic').agg({
            '% Abandonament a primer curs': 'mean'
        }).reset_index()

        # Extraemos las listas de años y valores
        years = branch_by_year['Curs Acadèmic'].tolist()
        valores_abandono = branch_by_year['% Abandonament a primer curs'].tolist()

        # Calculamos la regresión lineal
        slope_ab, intercept_ab, r_value_ab, p_value_ab, std_err_ab = linregress(
            range(len(years)),  # posiciones 0,1,2...
            valores_abandono
        )

        # Interpretamos el resultado
        if slope_ab > 0.01:
            tendencia_abandono = "creciente"
        elif slope_ab < -0.01:
            tendencia_abandono = "decreciente"
        else:
            tendencia_abandono = "estable"

        # Repetimos para el rendimiento (ya que en el JSON de ejemplo aparec)
        branch_by_year_r = branch_data.groupby('Curs Acadèmic').agg({
            'Taxa rendiment': 'mean'
        }).reset_index()
        valores_rend = branch_by_year_r['Taxa rendiment'].tolist()

        slope_r, intercept_r, r_value_r, p_value_r, std_err_r = linregress(
            range(len(years)),
            valores_rend
        )

        if slope_r > 0.01:
            tendencia_rend = "creciente"
        elif slope_r < -0.01:
            tendencia_rend = "decreciente"
        else:
            tendencia_rend = "estable"

        analisis_por_rama[rama] = {
            "abandono_medio": abandono_mean,
            "abandono_std": abandono_std,
            "abandono_min": abandono_min,
            "abandono_max": abandono_max,
            "rendimiento_medio": rendimiento_mean,
            "rendimiento_std": rendimiento_std,
            "rendimiento_min": rendimiento_min,
            "rendimiento_max": rendimiento_max,
            "tendencia_abandono": tendencia_abandono,
            "tendencia_rendimiento": tendencia_rend
        }

    # RANKINGS
    # Creamos los rankings
    rendimiento_ranking = merged_df.groupby('Branca')['Taxa rendiment'].mean().sort_values()
    abandono_ranking = merged_df.groupby('Branca')['% Abandonament a primer curs'].mean().sort_values()

    # Seleccionamos el mayor y el peor
    ranking_ramas = {
        "mejor_rendimiento": [rendimiento_ranking.idxmax()],
        "peor_rendimiento": [rendimiento_ranking.idxmin()],
        "mayor_abandono": [abandono_ranking.idxmax()],
        "menor_abandono": [abandono_ranking.idxmin()]
    }

    #JSON FINAL Y CREAMOS CARPETA
    # Agrupamos los resultados
    resultado = {
        "metadata": metadata,
        "estadisticas_globales": estadisticas_globales,
        "analisis_por_rama": analisis_por_rama,
        "ranking_ramas": ranking_ramas
    }

    # Creamos la carpeta report si no existe
    output_dir = "report"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"evolucion_JavierArenasVillanueva.json")

    # Guardamos JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"Análisis estadístico guardado en: {output_path}")


