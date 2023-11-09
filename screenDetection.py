#imports
import time
import pyautogui
import os
import pygetwindow as gw
from recognition import recognize_emotions

app_name = "Discord"  
app_window = gw.getWindowsWithTitle('Lounge | Indagatorias SO - Discord')#nombre de la ventana a la que se le va a tomar el screenshot

if app_window:
    app_window = app_window[0]
    app_window.activate()
    time.sleep(1) # para que se abra la aplicacion de la reunion
    screenshot = pyautogui.screenshot(region=(app_window.left, app_window.top, app_window.width, app_window.height))
    
    # Guarda la imagen 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, 'faces_screenshot.png')
    screenshot.save(img_path)

    #llama a la funcion de recognition
    image_file = {'image_file': open(img_path, 'rb')}
    recognize_emotions(image_file)
    
else:
    print(f"Application window not found: {app_name}")