import cv2
import dlib
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import time
import math


model = load_model("C:/Benim programlarim/my_ldp5/rnnmodel.h5")


detector = dlib.get_frontal_face_detector()


cap = cv2.VideoCapture(0)


predictions_last_5_sec = []
time_threshold = 5  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    current_time = time.time()

    
    faces = detector(frame)
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()

        
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > frame.shape[1] or y + h > frame.shape[0]:
            continue

        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        
        face_img = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (64, 64))
        face_img = face_img.astype("float32") / 255.0
        face_img = img_to_array(face_img)
               
        face_img_sequence = np.stack([face_img] * 226, axis=0)  
        face_img_sequence = np.expand_dims(face_img_sequence, axis=0) 

        
        prediction = model.predict(face_img_sequence) 
        gerceklik_orani = prediction[0][0]

        
        predictions_last_5_sec.append((current_time, gerceklik_orani))
        predictions_last_5_sec = [p for p in predictions_last_5_sec if current_time - p[0] < time_threshold]

        
        if predictions_last_5_sec:
            log_sum = sum(math.log(p[1] + 1) for p in predictions_last_5_sec)  
            avg_log = log_sum / len(predictions_last_5_sec)
            avg_prediction = math.exp(avg_log) - 1  
            text = f"Real: {avg_prediction*100:.2f}%" if avg_prediction > 0.5 else f"Fake: {(1-avg_prediction)*100:.2f}%"
        else:
            text = "Checking..."

        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release
cv2.destroyAllWindows()
