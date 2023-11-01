from deepface import DeepFace
from datetime import datetime

# Función para obtener la fecha y hora actual
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Función para realizar el reconocimiento facial
def perform_face_recognition(image_path):
    try:
        result = DeepFace.analyze(img_path = image_path, actions = ['age', 'gender', 'emotion'])
        return result
    except Exception as e:
        print("Error:", e)
        return None

# Función para registrar la información en la bitácora
def log_entry(person_name, camera_location, camera_ip, date_time, facial_analysis):
    log_entry = f"Person: {person_name}\nLocation: {camera_location}\nCamera IP: {camera_ip}\nDate & Time: {date_time}\nFacial Analysis:\n{facial_analysis}\n"
    with open("bitacora.txt", "a") as log_file:
        log_file.write(log_entry)
        log_file.write("=" * 40 + "\n")

# Información de ejemplo
person_name = "John Doe"
camera_location = "Entrance"
camera_ip = "192.168.1.100"
image_path = "Rodney.jpg"

# Realizar reconocimiento facial
facial_analysis = perform_face_recognition(image_path)

if facial_analysis:
    date_time = get_current_datetime()
    log_entry(person_name, camera_location, camera_ip, date_time, facial_analysis)
    print("Entrada registrada en la bitácora.")
else:
    print("No se pudo realizar el reconocimiento facial.")

