# DeepFaceRegistry

This project offers a robust solution for real-time face recognition using IP cameras, integrating technologies like Django, Vue.js, DeepFace, OpenCV, and MediaPipe. The core feature allows for real-time logging of recognized faces against a pre-registered database of users.

## Features

- **User Registration**: Register users and store their facial information for later recognition.
- **IP Camera Integration**: Link IP cameras to the system for real-time face tracking.
- **Real-time Face Recognition**: Every face captured by the IP cameras is compared against the user database in real-time.
- **Automatic Logging**: If a recognized face matches a registered user, the information gets logged in real-time. Faces that aren't in the database are ignored.

## Technologies Used

- **Backend**: Django, Flask
- **Frontend**: Vue.js
- **Face Recognition**: DeepFace, OpenCV, MediaPipe

## Directory Structure

- `camera_track_backend`: Contains all backend code, built with Django.
- `camera_track_frontend`: Contains frontend code, developed using Vue.js.

## Local Setup

To run this project locally, you need to set up both frontend and backend.

### Frontend

Navigate to the `camera_track_frontend` directory:

```bash
cd camera_track_frontend
npm run serve -- --port 4000
```

### Backend
Ensure you have poetry installed. Navigate to the `camera_track_backend` directory:

```bash
cd camera_track_backend
poetry run python manage.py runserver localhost:8000
```
This will start the backend server on http://localhost:8000/
