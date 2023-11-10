import json
from flask import Flask, render_template, request
from multiprocessing import Process, Queue
import time
import pyautogui
import os
import requests

# Parámetros para el reconocimiento de emociones
api_key = 'JLwR83pL00f6I39pBi7N2rnoNRkbzH3y'
api_secret = 'XxknnnjxdSZOsRUO1tPE1Mk2rF7j6LKs'
return_landmark = 1
return_attributes = 'emotion'
url = 'https://api-us.faceplusplus.com/facepp/v3/detect'

params = {
    'api_key': api_key,
    'api_secret': api_secret,
    'return_landmark': return_landmark,
    'return_attributes': return_attributes
}

app = Flask(__name__)

# ...

def recognize_emotions(image_path):
    try:
        # Leer la imagen en formato binario
        files = {'image_file': open(image_path, 'rb')}

        # Enviar la solicitud al servicio de Face++
        response = requests.post(url, params=params, files=files)
        response.raise_for_status()

        # Analizar la respuesta JSON
        result = response.json()

        # Verificar si se detectaron rostros en la imagen
        if 'faces' in result and len(result['faces']) > 0:
            # Obtener la posición del primer rostro detectado
            face = result['faces'][0]['face_rectangle']

            # Obtener las emociones detectadas
            emotions = result['faces'][0]['attributes']['emotion']

            # Imprimir las emociones en consola
            print(f"Emociones detectadas: {emotions}")

            # Guardar las emociones en un archivo JSON solo si hay emociones detectadas
            try:
                with open('emociones.json', 'r') as json_file:
                    datos_existente = json.load(json_file)
            except FileNotFoundError:
                datos_existente = []

            # Añadir las emociones a la lista existente
            if emotions:
                datos_existente.append({'emotions': emotions})

            # Guardar la lista actualizada en el archivo JSON
            with open('emociones.json', 'w') as json_file:
                json.dump(datos_existente, json_file, indent=2)
                
            return {
                'left': face['left'],
                'top': face['top'],
                'width': face['width'],
                'height': face['height']
            }
        else:
            print("No se detectaron rostros en la imagen.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud al servicio Face++: {e}")
        return None

def capturar_pantalla(image_queue):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'full_screen_screenshot.png')
            screenshot.save(img_path)

            # Obtener la posición del rostro y las emociones
            recognize_emotions(img_path)

            # No es necesario dibujar un rectángulo en este caso

            image_queue.put(img_path)  # Poner la ruta de la imagen en la cola
            time.sleep(1 / 15)
        except Exception as e:
            print(f"Error en el bucle principal: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    app_name = request.form['app_name']
    # Eliminamos la obtención del título de la ventana, ya que no se utiliza al capturar toda la pantalla

    image_queue = Queue()  # Cola para comunicarse entre procesos

    # Crear un proceso separado para la captura y reconocimiento
    capture_process = Process(target=capturar_pantalla, args=(image_queue,))
    capture_process.start()

    try:
        # Mantener la aplicación en funcionamiento para manejar la interfaz web
        app.run(debug=True)
    except KeyboardInterrupt:
        # Terminar los procesos en caso de interrupción del teclado
        capture_process.terminate()
        capture_process.join()

    return f'Configuración recibida. Nombre de la aplicación: {app_name}'

if __name__ == '__main__':
    print("Iniciando la aplicación...")
    app.run(debug=True)