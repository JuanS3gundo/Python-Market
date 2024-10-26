from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from inflation import ajustar_precios_por_inflacion
from data_processor import procesar_csv
from analytics import cargar_datos_mensuales, obtener_estadisticas
import matplotlib.pyplot as plt
import io
import base64
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta para la página principal
@app.route('/')
def upload_file():
    return render_template('upload.html')

# Ruta para procesar archivos de inflación
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        inflacion = request.form.get('inflacion', type=float) / 100  # Convertir el valor de inflación a decimal

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Cargar y ajustar precios en base a la inflación ingresada
            df = procesar_csv(filepath)
            df_ajustado = ajustar_precios_por_inflacion(df, inflacion=inflacion)

            # Guardar el archivo ajustado sobrescribiendo el original
            df_ajustado.to_csv(filepath, index=False)

            return redirect(url_for('analisis'))

@app.route('/analisis')
def analisis():
    # Cargar y analizar datos mensuales
    df_combined = cargar_datos_mensuales(app.config['UPLOAD_FOLDER'])
    precios_mensuales, precios_ajustados, cantidad_vendida_mensual, producto_mas_vendido, cantidad_recomendada, cantidad_historica_promedio = obtener_estadisticas(df_combined)

    # Convertir los datos a JSON para los gráficos
    precios_json = json.dumps(precios_mensuales.to_dict())
    precios_ajustados_json = json.dumps(precios_ajustados.to_dict())
    cantidad_json = json.dumps(cantidad_vendida_mensual.sum(axis=0).to_dict())

    return render_template(
        'resultados.html',
        precios_json=precios_json,
        precios_ajustados_json=precios_ajustados_json,
        cantidad_json=cantidad_json,
        producto_mas_vendido=producto_mas_vendido,
        cantidad_recomendada=cantidad_recomendada,
        cantidad_historica_promedio=cantidad_historica_promedio
    )




if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)