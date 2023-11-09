import requests

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

def recognize_emotions(image_path):

    image_file = {'image_file': open(image_path, 'rb')}

    response = requests.post(url, files=image_file, data=params)
    if response.status_code == 200:
        data = response.json()
        if 'faces' in data:
            for idx, face in enumerate(data['faces']):
                if 'attributes' in face and 'emotion' in face['attributes']:
                    emocion = face['attributes']['emotion']
                    print(f"Emoción del rostro {idx + 1}:", emocion)
                else:
                    print(f"No se encontraron emociones para el rostro {idx + 1}")
        else:
            print("No se detectaron rostros en la imagen")
    else:
        print(f'Error: {response.status_code}, {response.text}')
