import cv2
import pickle
import numpy as np
import os

video = cv2.VideoCapture(0) # 0 for inbuilt webcam
facesdetect = cv2.CascadeClassifier('C:\\College\\College Hackathon (20-10-23)\\FaceData\\haarcascade_frontalface_default.xml')

facesData = []

i = 0
name = input('Enter your name:')

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facesdetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cropImg = frame[y:y+h, x:x+w, :]
        resizedImg = cv2.resize(cropImg, (50, 50))
        if len(facesData)<=100 and i%10==0:
            facesData.append(resizedImg)
        i += 1
        cv2.putText(frame, str(len(facesData)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
    cv2.imshow("MFW", frame)
    k = cv2.waitKey(1)   # sets k to be something that is not ascii of 'q'
    if k == ord('q') or len(facesData) == 100:    # ord() return ascoo of 'q'. if q pressed, k will become ascii of q and loop break
        break
video.release()
cv2.destroyAllWindows()

facesData = np.array(facesData)
facesData = facesData.reshape(100, -1)

if 'names.pkl' not in os.listdir('C:\\College\\College Hackathon (20-10-23)\\FaceData\\'):
    names = [name]*100
    with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\names.pkl', 'rb') as f:
        names = pickle.load(f)
    names += [name]*100
    with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\names.pkl', 'wb') as f:
        pickle.dump(names, f)

if 'faces.pkl' not in os.listdir('C:\\College\\College Hackathon (20-10-23)\\FaceData\\'):
    names = [name]*100
    with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\facesData.pkl', 'wb') as f:
        pickle.dump(facesData, f)
else:
    with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\facesData.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, facesData, axis=0)
    with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\facesData.pkl', 'wb') as f:
        pickle.dump(names, f)