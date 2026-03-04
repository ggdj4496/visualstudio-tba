import cv2
import numpy as np

def assimilate_face(frame, overlay_img):
    # Detección básica para evitar duplicidad de elementos
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Redimensionar el overlay al tamaño de la cara detectada
        roi_color = frame[y:y+h, x:x+w]
        overlay_res = cv2.resize(overlay_img, (w, h))
        
        # Mezcla suave para evitar el efecto de "tres ojos"
        result = cv2.addWeighted(roi_color, 0.4, overlay_res, 0.6, 0)
        frame[y:y+h, x:x+w] = result
        
    return frame