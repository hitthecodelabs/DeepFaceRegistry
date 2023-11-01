from deepface import DeepFace
import csv
from datetime import datetime

# Función para detectar a la persona e iniciar sesión en el archivo de registro.
def detect_and_log(image_path, camera_location, camera_ip):
    try:
        result = DeepFace.detectFace(image_path)

        if result.shape[0] > 0:  # Compruebe si se detecta al menos una cara
            detected_name = "Persona Detectada"  # Cambie esto según su lógica para obtener el nombre
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Registre la información en el archivo CSV
            with open('bitacora.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([detected_name, camera_location, camera_ip, current_time])

            print("Persona detectada y registrada en la bitácora.")

        else:
            print("No se pudo detectar una cara en la imagen.")

    except Exception as e:
        print("Error:", e)

# Ruta de la imagen, ubicación de la cámara y dirección IP de la cámara
image_path = 'Anthony.jpg'
camera_location = 'Ubicación de la cámara'
camera_ip = '192.168.1.1'

detect_and_log(image_path, camera_location, camera_ip)