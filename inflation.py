def ajustar_precios_por_inflacion(df, inflacion):
    # Ajustar el precio y guardar en una nueva columna sin modificar la original
    df['Precio Ajustado por Inflación'] = df['Precio (ARS)'] * (1 + inflacion)
    return df