import mss
import cv2
import time
import os


def eliminar_capturas(carpeta):
    try:
        for archivo in os.listdir(carpeta):
            archivo_path = os.path.join(carpeta, archivo)
            if os.path.isfile(archivo_path):
                os.remove(archivo_path)
        print("Capturas eliminadas correctamente.")
    except Exception as e:
        print(f"Error al eliminar capturas: {str(e)}")

def capturar_pantalla_con_guardado(duracion_segundos, fps_deseados, carpeta_guardado):
    tiempo_inicio = time.time()
    tiempo_final = tiempo_inicio + duracion_segundos

    if not os.path.exists(carpeta_guardado):
        os.makedirs(carpeta_guardado)

    with mss.mss() as sct:
        contador = 1
        while time.time() < tiempo_final:
            frame = sct.shot(output=os.path.join(carpeta_guardado, f'captura{contador:04d}.png'))
            contador += 1

            img = cv2.imread(frame)

            ''' cv2.imshow('Captura de pantalla', img) '''

            if cv2.waitKey(1000 // fps_deseados) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

# Duración de la captura
duracion_segundos = 10  # Duración de la captura
fps_deseados = 15  # FPS deseados
carpeta_guardado = 'capturas'  # Nombre de la carpeta de guardado

''' capturar_pantalla_con_guardado(duracion_segundos, fps_deseados, carpeta_guardado)
 '''
eliminar_capturas(carpeta_guardado)


