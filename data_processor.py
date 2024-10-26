import pandas as pd
import numpy as np

def procesar_csv(filepath):
    # Cargar el archivo CSV
    df = pd.read_csv(filepath)

    df['Cantidad Vendida por Mes'] = np.random.randint(20, 1000, size=len(df))

    return df