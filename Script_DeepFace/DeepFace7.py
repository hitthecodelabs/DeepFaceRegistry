from deepface import DeepFace
import csv
from datetime import datetime

# Función para realizar la detección y registrar en la bitácora
def detect_and_log(image_path, camera_location, camera_ip):
    try:
        result = DeepFace.detectFace(image_path)

        if result.shape[0] > 0:  # Verificar si se detectó al menos una cara
            detected_name = "Rodney Torres V"  # Cambia esto según tu lógica para obtener el nombre

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Registrar la información en el archivo CSV
            with open('bitacora.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([detected_name, camera_location, camera_ip, current_time])

            print("Persona detectada y registrada en la bitácora.")

        else:
            print("No se pudo detectar una cara en la imagen.")

    except Exception as e:
        print("Error:", e)

# Ruta de la imagen, ubicación de la cámara y dirección IP de la cámara
image_path = 'Rodney.jpg'
camera_location = 'Sala'
camera_ip = '192.168.100.124'

# Llamar a la función para realizar la detección y registro
detect_and_log(image_path, camera_location, camera_ip)
