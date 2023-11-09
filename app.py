from flask import Flask, render_template, request
import time
import pyautogui
import os
import pygetwindow as gw
from recognition import recognize_emotions
from multiprocessing import Process

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    app_name = request.form['app_name']
    app_window_title = request.form['app_window_title']

    # Crear un proceso separado para la captura de pantalla
    capture_process = Process(target=capturar_pantalla, args=(app_name, app_window_title))
    capture_process.start()

    try:
        # Proceso principal maneja el reconocimiento de emociones
        reconocimiento()
    except KeyboardInterrupt:
        # Termina el proceso de captura en la interrupción del teclado
        capture_process.terminate()
        capture_process.join()

    return f'Configuración recibida. Nombre de la aplicación: {app_name}, Título de la ventana: {app_window_title}'

def capturar_pantalla(app_name, app_window_title):
    app_window = gw.getWindowsWithTitle(app_window_title)

    if app_window:
        app_window = app_window[0]
        app_window.activate()

        # Increase the sleep duration to allow the application window to open
        time.sleep(3)

        while True:
            screenshot = pyautogui.screenshot(region=(app_window.left, app_window.top, app_window.width, app_window.height))
            # Guarda la imagen
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'faces_screenshot.png')
            screenshot.save(img_path)
            time.sleep(1 / 15)
    else:
        print(f"Application window not found: {app_name}")

def reconocimiento():
    while True:
        # llama a la función de reconocimiento
        image_file = {'image_file': open('faces_screenshot.png', 'rb')}
        recognize_emotions(image_file)

if __name__ == '__main__':
    app.run(debug=True)
