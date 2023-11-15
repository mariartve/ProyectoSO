import json
import signal
from flask import Flask, render_template, request
from multiprocessing import Process, Queue
import time
from datetime import datetime
import pyautogui
import pygetwindow as gw
import os
import requests
from graficar import graficoBarras, graficoPastel, limpiar_emociones_json

def ejecutar_graficos(period):
    graficoBarras(period)
    graficoPastel(period)

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
capture_process = None  # Variable global
exit_flag = False  # Variable global para indicar al proceso de captura cuándo debe finalizar

def getTime():
    start_time = datetime.now()
    start_time_str = start_time.strftime("%H:%M:%S")
    return start_time_str

def recognize_emotions(image_path, period):
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
                datos_existente.append({'emotions': emotions, 'period': period})


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

def capturar_pantalla(image_queue, user_duration):
    global capture_process
    try:
        print(f"Proceso iniciado a {getTime()}")
        start_time = time.time()
        while not exit_flag:
            screenshot = pyautogui.screenshot()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'full_screen_screenshot.png')
            screenshot.save(img_path)

            if user_duration == 5:
                capture_interval = 1
            else:
                capture_interval = 3

            elapsed_time = time.time() - start_time
            # Obtener la posición del rostro y las emociones
            if elapsed_time <= capture_interval * 60:  # Antes
                recognize_emotions(img_path, "Antes")
            elif capture_interval * 60 < elapsed_time <= (user_duration - capture_interval) * 60:  # Durante
                recognize_emotions(img_path, "Durante")
            elif (user_duration - capture_interval) * 60 < elapsed_time < user_duration * 60: # Despues
                recognize_emotions(img_path, "Despues")
            elif elapsed_time >= user_duration * 60:
                break
            # No es necesario dibujar un rectángulo en este caso

            image_queue.put(img_path)  # Poner la ruta de la imagen en la cola
            time.sleep(1 / 15)

    except Exception as e:
        print(f"Error en el bucle principal: {e}")
    finally:
        ejecutar_graficos("Antes")
        ejecutar_graficos("Durante")
        ejecutar_graficos("Despues")
        ejecutar_graficos("General")
        if capture_process is not None:
            capture_process.terminate()
            capture_process.join(user_duration)
            limpiar_emociones_json()
            print("Proceso de captura terminado a las {getTime()}.")

def signal_handler(sig, frame):
    global capture_process  # Acceso a la variable global
    global exit_flag
    print("Interrupción de teclado detectada. Ejecutando gráficos...")
    ejecutar_graficos("General")

    exit_flag = True  # Indicar al proceso de captura que debe finalizar

    if capture_process is not None:
        capture_process.terminate()
        capture_process.join()
        limpiar_emociones_json()
        print("Proceso terminado.")
    
    exit(0)

def abrir_ventana(nombre):
    try:
        # Busca la ventana por su título
        ventana = gw.getWindowsWithTitle(nombre)[0]
        # Cambia el enfoque a la ventana
        try:
            # Activa la ventana en la barra de tareas para restaurarla
            ventana.minimize()  # Minimiza la ventana
            ventana.restore()   # Restaura la ventana

            # Espera un breve período para que la ventana se restaure completamente
            time.sleep(1)

            # Simula un clic en el icono de la barra de tareas
            pyautogui.click(ventana.left + 10, ventana.top + ventana.height // 2)
            time.sleep(1)
        except gw.PyGetWindowException as e:
            print(f"Error al abrir la ventana: {e}")

    except IndexError:
        print(f"No se encontró una ventana con el título '{nombre}'")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():

    global capture_process  # Acceso a la variable global

    app_name = request.form['app_name']
    app_window = request.form['app_window_title']
    user_duration = int(request.form['duration'])

    #Abrir la ventana que se desea capturar
    abrir_ventana(app_window)

    image_queue = Queue()  # Cola para comunicarse entre procesos

    # Crear un proceso separado para la captura y reconocimiento
    capture_process = Process(target=capturar_pantalla, args=(image_queue, user_duration))
    capture_process.start()

    try:
        # Mantener la aplicación en funcionamiento para manejar la interfaz web
        #app.run(debug=True)
        pass
    except KeyboardInterrupt:
        # Terminar los procesos en caso de interrupción del teclado
        signal_handler(signal.SIGINT, None) 

    return f'Configuración recibida. Nombre de la aplicación: {app_name}'

if __name__ == '__main__':
    print("Iniciando la aplicación...")
    # Configurar el manejador de señales para la interrupción de teclado
    signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True, use_reloader=False)