# Proyecto Principios de Sistemas Operativos - TEC
Este proyecto programado es un programa en Python que utiliza Flask para crear una aplicación web que captura emociones a través de una cámara web, reconoce las emociones utilizando la API de Face++, y muestra los resultados en tiempo real. Los datos de emociones se guardan en un archivo JSON, y también se han implementado funciones para generar gráficos de barras y de pastel basados en los datos de emociones recopilados.

# Principales características:

## Recopilación y Almacenamiento de Datos:

La aplicación Flask permite a los usuarios especificar la ventana de la aplicación a monitorear.
La función capturar_pantalla captura continuamente la pantalla, guarda capturas de pantalla y detecta emociones en las imágenes capturadas utilizando la API de Face++.
Las emociones reconocidas se guardan en un archivo JSON llamado 'emociones.json'.
Generación de Gráficos:

Se generan dos tipos de gráficos, gráficos de barras (graficoBarras) y gráficos de pastel (graficoPastel), basados en los datos promedio de emociones recopilados con el tiempo.
La función guardar_con_fecha_hora se utiliza para guardar los gráficos generados con una marca de tiempo.

## Aplicación Web con Flask:
La aplicación Flask tiene dos rutas: '/' para la página de inicio y '/procesar' para procesar las entradas del usuario.
Los usuarios pueden especificar el título de la ventana de la aplicación a través de un formulario en la página de inicio.
La ruta procesar inicia un proceso separado (capturar_pantalla) para capturar continuamente emociones mientras mantiene en funcionamiento la aplicación principal de Flask.

## Manejo de Señales:
El script maneja interrupciones de teclado (Ctrl+C) ejecutando la función signal_handler.
Cuando se interrumpe, ejecuta la función ejecutar_graficos para generar gráficos y termina el proceso de captura.

## Dependencias:
El script depende de varias bibliotecas de Python, incluyendo Flask, Matplotlib, NumPy y requests.
También requiere la API de Face++ para el reconocimiento de emociones.

Este software proporciona un marco básico para capturar y visualizar emociones en tiempo real. Asegúrate de tener las dependencias necesarias instaladas y de configurar correctamente la clave y el secreto de la API de Face++. 
Además, es importante verificar que el administrador de ventanas requerido (pygetwindow) y la biblioteca de capturas de pantalla (pyautogui) sean compatibles con el sistema, en el que se ejecuta, puesto que en sistemas operativos como Linux no es compatible.