import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_temporal(df):
    """
    Genera una figura on dos subplots:
        1. Evolución del % de abandono por curso académico.
        2. Evolución de la tasa de rendimiento por curso académico.

    Parámetros
        df: dataframe resultado de la unicón.

    Devuelve:
        Genera el gráfico y lo guarda en 'src/img/' como .png.
    """
    # Creamos el directorio
    output_dir = "img"
    os.makedirs(output_dir, exist_ok=True)

    # Configuramos el gráfico
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Seleccionamos los grupos de carreras y los colores que usaremos
    ramas = df['Branca'].unique()
    colores = plt.cm.tab10.colors

    # Gráfico 1: % Abandono
    ax1 = axes[0]
    for i, rama in enumerate(ramas):
        rama_data = df[df['Branca'] == rama]
        rama_grouped = rama_data.groupby('Curs Acadèmic')['% Abandonament a primer curs'].mean()
        ax1.plot(rama_grouped.index, rama_grouped.values, label=rama, color=colores[i % len(colores)])
    ax1.set_ylabel('% Abandono')
    ax1.set_title('Evolución del % de Abandono por curso académico')
    ax1.grid(True)
    ax1.legend()

    # Gráfico 2: Tasa de rendimiento
    ax2 = axes[1]
    for i, rama in enumerate(ramas):
        rama_data = df[df['Branca'] == rama]
        rama_grouped = rama_data.groupby('Curs Acadèmic')['Taxa rendiment'].mean()
        ax2.plot(rama_grouped.index, rama_grouped.values, label=rama, color=colores[i % len(colores)])
    ax2.set_ylabel('Tasa de rendimiento')
    ax2.set_xlabel('Curso Académico')
    ax2.set_title('Evolución de la Tasa de Rendimiento por curso académico')
    ax2.grid(True)
    ax2.legend()

    # Guardamos la imagen
    output_path = os.path.join(output_dir, f"evolucion_JavierArenasVillanueva.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Figura guardada en: {output_path}")


