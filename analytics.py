import pandas as pd
import os
import glob

def cargar_datos_mensuales(upload_folder):
    archivos = glob.glob(os.path.join(upload_folder, 'productos_precios_*.csv'))
    datos = []

    for archivo in archivos:
        mes = archivo.split('_')[-1].replace('.csv', '')
        df = pd.read_csv(archivo)
        df['Mes'] = mes
        datos.append(df)

    df_combined = pd.concat(datos)
    return df_combined

def obtener_estadisticas(df_combined):
    # Promedio de precios originales y ajustados por inflación para cada producto y mes
    precios_mensuales = df_combined.groupby(['Mes', 'Producto'])['Precio (ARS)'].mean().unstack()
    precios_ajustados = df_combined.groupby(['Mes', 'Producto'])['Precio Ajustado por Inflación'].mean().unstack()
    
    # Productos con mayor cantidad vendida en cada mes
    cantidad_vendida_mensual = df_combined.groupby(['Mes', 'Producto'])['Cantidad Vendida por Mes'].sum().unstack()

    # Determinar el producto más vendido y calcular la cantidad recomendada para el próximo mes
    total_vendido = cantidad_vendida_mensual.sum(axis=0)
    producto_mas_vendido = total_vendido.idxmax()
    cantidad_vendida_producto = total_vendido.max()
    cantidad_recomendada = int(cantidad_vendida_producto * 1.2)  # Aumentar un 20% para el próximo mes

    cantidad_historica_promedio = int(cantidad_vendida_mensual[producto_mas_vendido].mean())

    return precios_mensuales, precios_ajustados, cantidad_vendida_mensual, producto_mas_vendido, cantidad_recomendada, cantidad_historica_promedio