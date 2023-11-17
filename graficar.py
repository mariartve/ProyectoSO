import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def guardar_con_fecha_hora():
    # Obtener la fecha y hora actual
    now = datetime.now()
    fecha_hora_str = now.strftime("%Y%m%d%H%M%S")

    # Crear el nombre del archivo con la fecha y hora
    nombre_archivo = f'graficos/grafico_{fecha_hora_str}.png'

    # Guardar la imagen con el nombre generado
    plt.savefig(nombre_archivo)

    return nombre_archivo  # Devolver el nombre del archivo generado

def limpiar_emociones_json():
    # Limpiar la lista de emociones en el archivo
    with open('emociones.json', 'w') as file:
        file.write('[]')

# Cargar datos desde el archivo emociones.json
with open('emociones.json', 'r') as file:
    data = json.load(file)

# Crear listas para almacenar los valores promedio de cada emoción
emotions_labels = ['anger', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
emotions_mean = {emotion: 0 for emotion in emotions_labels}

def graficoBarras():
    if not data:
        print("No hay datos disponibles para generar el gráfico.")
        return

    

    # Calcular el promedio de cada emoción a lo largo de todas las muestras
    for entry in data:
        emotions = entry['emotions']
        for emotion in emotions_labels:
            emotions_mean[emotion] += emotions[emotion]

    total_samples = len(data)

    if total_samples == 0:
        print("No hay suficientes muestras para generar el gráfico.")
        return

    # Verificar que el denominador no sea cero antes de realizar la división
    for emotion in emotions_labels:
        emotions_mean[emotion] /= total_samples if total_samples > 0 else 1

    # Crear un gráfico de barras para el promedio de cada emoción
    fig, ax = plt.subplots(figsize=(10, 6))
    index = np.arange(len(emotions_labels))
    bar_width = 0.5

    ax.bar(index, emotions_mean.values(), bar_width, color='blue', alpha=0.7)

    # Configurar el gráfico
    ax.set_xlabel('Emoción')
    ax.set_ylabel('Promedio (%)')
    ax.set_title('Promedio de emociones en todas las muestras')
    ax.set_xticks(index)
    ax.set_xticklabels(emotions_labels)

    # Guardar la imagen con la fecha y hora
    nombre_archivo = guardar_con_fecha_hora()
    print(f"Imagen guardada: {nombre_archivo}")

    # Limpiar el archivo emociones.json
    limpiar_emociones_json()

    plt.show()

def graficoPastel():

    # Crear un gráfico de pastel para el promedio de emociones
    fig, ax = plt.subplots(figsize=(10, 6))
    wedges, texts, autotexts = ax.pie(emotions_mean.values(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)

    # Agregar una leyenda al cuadro a la derecha del gráfico de pastel
    ax.legend(wedges, emotions_mean.keys(), title="Emociones", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Configurar el título
    ax.set_title('Promedio de emociones en todas las muestras')

    # Guardar la imagen con la fecha y hora
    nombre_archivo = guardar_con_fecha_hora()
    print(f"Imagen guardada: {nombre_archivo}")

    # Limpiar el archivo emociones.json
    limpiar_emociones_json()

    plt.show()