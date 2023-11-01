import cv2
from deepface import DeepFace

# Configuración de las direcciones IP de las cámaras
camera1_url = "rtsp://admin:Abc12345@192.168.100.124:554/video"
camera2_url = "rtsp://admin:Abc12345@192.168.100.125:554/video"

# Inicializar los objetos de captura de las cámaras
camera1 = cv2.VideoCapture(camera1_url)
camera2 = cv2.VideoCapture(camera2_url)

# Ciclo principal
while True:
    # Capturar un frame de cada cámara
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()

    if not ret1 or not ret2:
        print("No se pudo capturar el frame de una de las cámaras.")
        break

    # Convertir los frames a escala de grises (para la detección de rostros)
    gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Utilizar el detector de rostros de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    detected_faces1 = face_cascade.detect_faces(gray_frame1)
    detected_faces2 = face_cascade.detect_faces(gray_frame2)

    # Dibujar rectángulos alrededor de los rostros detectados
    for face in detected_faces1:
        (x, y, w, h) = face['box']
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)

    for face in detected_faces2:
        (x, y, w, h) = face['box']
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Mostrar los frames con las detecciones
    cv2.imshow("Cámara 1", frame1)
    cv2.imshow("Cámara 2", frame2)

    # Detener el programa si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
camera1.release()
camera2.release()
cv2.destroyAllWindows()
