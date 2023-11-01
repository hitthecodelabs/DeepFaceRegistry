import cv2
from deepface import DeepFace
import csv
from datetime import datetime

# Function to extract faces and log in the log file
def extract_and_log(frame, camera_location, camera_ip):
    try:
        result = DeepFace.extractFace(frame, enforce_detection=true)

        if result.shape[0] > 0:  # Check if at least one face is detected
            detected_name = "Persona Detectada"  # Change this according to your logic for getting the name

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Log the information in the CSV file
            with open('bitacora.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([detected_name, camera_location, camera_ip, current_time])

            print("Persona detectada y registrada en la bitácora.")

        else:
            print("No se pudo detectar una cara en la imagen.")

    except Exception as e:
        print("Error:", e)

# Camera IP address and RTSP URL
camera_ip = '192.168.100.124'
rtsp_url = f'rtsp://admin:Abc12345@{camera_ip}:554'

# Open RTSP stream
cap = cv2.VideoCapture(rtsp_url)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Perform face extraction and logging
    extract_and_log(frame, "Ubicación de la cámara", camera_ip)
    
    # Display the frame (optional)
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()