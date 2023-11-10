from flask import Flask, render_template, request
from multiprocessing import Process, Queue
import time
import pyautogui
import os
from PIL import Image, ImageDraw
import requests
import pygetwindow as gw  # Importa la biblioteca pygetwindow

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

def recognize_emotions(image_path):
    try:
        files = {'image_file': open(image_path, 'rb')}
        response = requests.post(url, params=params, files=files)
        response.raise_for_status()
        result = response.json()

        if 'faces' in result and len(result['faces']) > 0:
            face = result['faces'][0]['face_rectangle']
            emotions = result['faces'][0]['attributes']['emotion']
            print(f"Emociones detectadas: {emotions}")
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

def capturar_pantalla(window_title, image_queue):
    while True:
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            window.activate()

            screenshot = window.screenshot()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'window_screenshot.png')
            screenshot.save(img_path)

            face_position = recognize_emotions(img_path)

            image_queue.put(img_path)
            time.sleep(1 / 15)
        except IndexError:
            print(f"No se encontró ninguna ventana con el título: {window_title}")
        except Exception as e:
            print(f"Error en el bucle principal: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    app_name = request.form['app_name']
    window_title = "Nombre de tu ventana"  # Reemplaza con el título de tu ventana

    image_queue = Queue()

    capture_process = Process(target=capturar_pantalla, args=(window_title, image_queue,))
    capture_process.start()

    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        capture_process.terminate()
        capture_process.join()

    return f'Configuración recibida. Nombre de la aplicación: {app_name}'

if __name__ == '__main__':
    print("Iniciando la aplicación...")
    app.run(debug=True)
