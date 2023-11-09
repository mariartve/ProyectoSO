import time
import pyautogui
import os
import pygetwindow as gw
from recognition import recognize_emotions
from multiprocessing import Process, Queue

def capturar_pantalla(app_window_title, image_queue):
    app_window = gw.getWindowsWithTitle(app_window_title)

    if app_window:
        app_window = app_window[0]
        app_window.activate()
        time.sleep(1)  # para que se abra la aplicación

        while True:
            screenshot = pyautogui.screenshot(region=(app_window.left, app_window.top, app_window.width, app_window.height))
            script_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(script_dir, 'faces_screenshot.png')
            screenshot.save(img_path)
            image_queue.put(img_path)  # Poner la ruta de la imagen en la cola
            time.sleep(1 / 15)
    else:
        print(f"Application window not found: {app_window_title}")


def reconocimiento(image_queue):
    while True:
        if not image_queue.empty():  # Comprobar si hay una imagen en la cola
            image_path = image_queue.get()  # Obtener la ruta de la imagen capturada
            recognize_emotions(image_path)  # Llamar a la función de reconocimiento

if __name__ == '__main__':
    image_queue = Queue()  # Crear la cola de comunicación entre procesos

    # Crear un proceso separado para capturar pantalla
    capture_process = Process(target=capturar_pantalla, args=('Meet: huw-jymu-qjk - Google Chrome', image_queue))
    capture_process.start()

    try:
        # Proceso principal maneja el reconocimiento de emociones
        reconocimiento(image_queue)  # Pasar la cola al proceso de reconocimiento
    except KeyboardInterrupt:
        # Terminar el proceso en caso de interrupción del teclado
        capture_process.terminate()
        capture_process.join()
