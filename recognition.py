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

def recognize_emotions(image_file):
    response = requests.post(url, files=image_file, data=params)
    if response.status_code == 200:
        data = response.json()
        if data['faces']:
            for idx, face in enumerate(data['faces']):
                if 'attributes' in face and 'emotion' in face['attributes']:
                    emocion = face['attributes']['emotion']
                    print(f"Emotion of the face {idx + 1}:", emocion)
                else:
                    print(f"No emotions were found for the face {idx + 1}")
        else:
            print("No faces detected")
    else:
        print(f'Error: {response.status_code}, {response.text}')   
