from flask import Flask, render_template, request
import time
import pyautogui
import os
import pygetwindow as gw
import requests
from recognition import recognize_emotions
from multiprocessing import Process, Queue

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    app_name = request.form['app_name']
    app_window_title = request.form['app_window_title']

    image_queue = Queue()  # Cola para comunicarse entre procesos

    # Crear un proceso separado para la captura y reconocimiento
    capture_process = Process(target=capturar_y_reconocer, args=(app_name, app_window_title, image_queue))
    capture_process.start()

    # Obtener respuestas del reconocimiento
    while not image_queue.empty():
        response = image_queue.get()
        print("Respuesta de reconocimiento:", response)  # Puedes manejar la respuesta como desees

    return f'Configuración recibida. Nombre de la aplicación: {app_name}, Título de la ventana: {app_window_title}'

def capturar_y_reconocer(app_name, app_window_title, image_queue):
    app_window = gw.getWindowsWithTitle(app_window_title)

    if app_window:
        app_window = app_window[0]
        app_window.activate()

        time.sleep(3)  # Permitir que la ventana de la aplicación se abra

        while True:
            screenshot = pyautogui.screenshot(region=(app_window.left, app_window.top, app_window.width, app_window.height))
            # Guardar la imagen en una carpeta
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'captured_images', 'faces_screenshot.png')
            screenshot.save(img_path)

            # Enviar la imagen al reconocimiento
            image_file = {'image_file': open(img_path, 'rb')}
            recognition_response = recognize_emotions(image_file)  # Reconocimiento en la nube

            image_queue.put(recognition_response)  # Poner la respuesta en la cola para enviarla de vuelta

            time.sleep(1 / 15)
    else:
        print(f"Ventana de la aplicación no encontrada: {app_name}")

if __name__ == '__main__':
    app.run(debug=True)
