from deepface import DeepFace
result = DeepFace.verify("Rodney.jpg", "Vanessa.jpg")
print("Is verified: ", result["verified"])