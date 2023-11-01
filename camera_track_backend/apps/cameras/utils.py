import cv2
import os
import numpy as np
from django.http import StreamingHttpResponse
from apps.users.models import FaceCapture


def gen_frames(cam, face_cascade, persons, minH, minW, recognizer, font):
    print(persons)
    #iniciate id counter
    id = 0
    while True:
        ret, img = cam.read()
        if not ret:
            break
        #img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            print(id)
            name = ''
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 80):
                #id = persons[id]
                # for person in persons:
                #     if person.get('id') == id:
                #         name = person.get('name')
                #         break
                person = next((diccionario for diccionario in persons if diccionario.get("id") ==id), None)
                print(person)
                name = person.get('name')
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# def video_feed(ip: str, name_ext: str):
def video_feed(cameraModel, users: list):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('./apps/cameras/trainer/trainer.yml')
    # Cargar el archivo XML del clasificador Haar Cascade preentrenado
    face_cascade = cv2.CascadeClassifier('./apps/cameras/object_detector/haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX 
    # Crear una lista de nombres de personas
    # names related to ids: example ==> Marcelo: id=1,  etc
    #names = ['None', 'Marcelo', 'Paula', 'Ilza', 'Z', 'W']
    # person_names = ['None']
    # for person in users:
    #     person_names.append(person.name)
    # persons = list()
    persons = [{'id': person.id, 'name': person.name + ' ' + person.last_name} for person in users]
    #person_names = [person.name for person in users]
    # camera = cv2.VideoCapture(url_capture_camera)
    flask_url = 'http://127.0.0.1:5000/stream/camera'
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(f'{flask_url}?id_camera={cameraModel.id}')
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    return StreamingHttpResponse(
        gen_frames(cam, face_cascade, persons, minH, minW, recognizer, font),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def save_recognition_person(id_user):
    
    cam = cv2.VideoCapture(0,cv2.CAP_MSMF)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    face_detector = cv2.CascadeClassifier('./apps/cameras/object_detector/haarcascade_frontalface_default.xml')

    # For each person, enter one numeric face id
    # face_id = input('\n enter user id end press <return> ==>  ')

    # print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    while (True):

        ret, img = cam.read()
        if not ret:
            break
        # img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     

            # Save the captured image into the datasets folder
            # cv2.imwrite("dataset/User." + str(id_user) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            # cv2.imshow('image', img)
            cv2.imwrite("./camera_track/media/dataset/User." + str(id_user) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            count += 1
            _ = FaceCapture.objects.create(
                capture="dataset/User." + str(id_user) + '.' + str(count) + ".jpg",
                user_id=id_user,
            )
        if count >= 30: # Take 30 face sample and stop video
            break

    cam.release()
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff Save")

def gen_frames_stream_recognition():
    
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    face_detector = cv2.CascadeClassifier('./apps/cameras/object_detector/haarcascade_frontalface_default.xml')
    while (True):

        ret, img = cam.read()
        if not ret:
            break
        # img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)    
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()
    print("\n [INFO] Exiting Program and cleanup stuff")


def stream_recognition():
    return StreamingHttpResponse(
        gen_frames_stream_recognition(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
