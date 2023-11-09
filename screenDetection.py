#imports
import time
import pyautogui
import os
import pygetwindow as gw
from recognition import recognize_emotions
from multiprocessing import Process

''' app_name = "Discord"  
app_window = gw.getWindowsWithTitle('Lounge | Indagatorias SO - Discord')#nombre de la ventana a la que se le va a tomar el screenshot '''

app_name = "Meet"
def capturar_pantalla():
    app_window = gw.getWindowsWithTitle('Meet: huw-jymu-qjk - Google Chrome')

    if app_window:
        app_window = app_window[0]
        app_window.activate()
        time.sleep(1) # para que se abra la aplicacion de la reunion
        
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
        #llama a la funcion de recognition
        image_file = {'image_file': open('faces_screenshot.png', 'rb')}
        recognize_emotions(image_file)

if __name__ == '__main__':
    # Create a separate process for screen capture
    capture_process = Process(target=capturar_pantalla)
    capture_process.start()
    try:
        # Main process handles emotion recognition
        reconocimiento()
    except KeyboardInterrupt:
        # Terminate the capture process on keyboard interrupt
        capture_process.terminate()
        capture_process.join()        