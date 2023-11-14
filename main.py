import json
import signal
from flask import Flask, render_template, request
from multiprocessing import Process, Queue
import time
import pyautogui
import pygetwindow as gw
import os
import requests
from graficar import graficoBarras, graficoPastel

def ejecutar_graficos():
    graficoBarras()
    graficoPastel()

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

def capturar_pantalla(image_queue, user_duration):
    try:
        start_time = time.time()

        while not exit_flag:
            screenshot = pyautogui.screenshot()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'full_screen_screenshot.png')
            screenshot.save(img_path)

            # Obtener la posición del rostro y las emociones
            recognize_emotions(img_path)

            # No es necesario dibujar un rectángulo en este caso

            image_queue.put(img_path)  # Poner la ruta de la imagen en la cola
            time.sleep(1 / 15)

            elapsed_time = time.time() - start_time
            if elapsed_time >= user_duration * 60:
                break

    except Exception as e:
        print(f"Error en el bucle principal: {e}")
    finally:
        ejecutar_graficos()
        capture_process.terminate()
        capture_process.join()
        print("Proceso de captura terminado.")

def signal_handler(sig, frame):
    global capture_process  # Acceso a la variable global
    global exit_flag
    print("Interrupción de teclado detectada. Ejecutando gráficos...")
    ejecutar_graficos()

    exit_flag = True  # Indicar al proceso de captura que debe finalizar

    if capture_process is not None:
        capture_process.terminate()
        capture_process.join()
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