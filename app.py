from flask import Flask, render_template, request
from multiprocessing import Process, Queue
from screenDetection import capturar_pantalla

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
    capture_process = Process(target=capturar_pantalla, args=(app_window_title, image_queue))
    capture_process.start()

    try:
        # Mantener la aplicación en funcionamiento para manejar la interfaz web
        app.run(debug=True)
    except KeyboardInterrupt:
        # Terminar los procesos en caso de interrupción del teclado
        capture_process.terminate()
        capture_process.join()

    return f'Configuración recibida. Nombre de la aplicación: {app_name}, Título de la ventana: {app_window_title}'

if __name__ == '__main__':
    app.run(debug=True)
