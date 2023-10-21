from sklearn.neighbors import KNeighborsClassifier

import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime as dt

from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video = cv2.VideoCapture(0) # 0 for inbuilt webcam
facesdetect = cv2.CascadeClassifier('C:\\College\\College Hackathon (20-10-23)\\FaceData\\haarcascade_frontalface_default.xml')

with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\names.pkl', 'rb') as l:
    LABELS = pickle.load(l)
with open('C:\\College\\College Hackathon (20-10-23)\\FaceData\\facesData.pkl', 'rb') as f:
    FACES = pickle.load(f)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

COL_NAMES = ["NAMES", "TIME"]

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facesdetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cropImg = frame[y:y+h, x:x+w, :]
        resizedImg = cv2.resize(cropImg, (50, 50)).flatten().reshape(1,-1)
        person = knn.predict(resizedImg)
        ts = time.time()
        date = dt.fromtimestamp(ts).strftime("%d-%m-%y")
        timestamp = dt.fromtimestamp(ts).strftime("%H:%M:%S")
        existIN = os.path.isfile("IN\\IN_"+ date +".csv")
        existOUT = os.path.isfile("OUT\\OUT_"+ date +".csv")
        cv2.putText(frame, str(person[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0)) 
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
        inOut = [str(person[0]), str(timestamp)]
    cv2.imshow("MFW", frame)
    k = cv2.waitKey(1)   # sets k to be something that is not ascii of 'q'
    if k == ord('i'):
        speak("CHECKED IN")
        if existIN:
            with open("C:\\College\\College Hackathon (20-10-23)\\IN\\IN_"+date+".csv", 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(inOut)
            csvfile.close()
        else:
            with open("C:\\College\\College Hackathon (20-10-23)\\IN\\IN_"+date+".csv", 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'IN TIME'])
                writer.writerow(inOut)
            csvfile.close()
        break
    if k == ord('o'):
        speak("CHECKED OUT")
        if existOUT:
            with open("C:\\College\\College Hackathon (20-10-23)\\OUT\\OUT_"+date+".csv", 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(inOut)
            csvfile.close()
        else:
            with open("C:\\College\\College Hackathon (20-10-23)\\OUT\\OUT_"+date+".csv", 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Name', 'OUT TIME'])
                writer.writerow(inOut)
            csvfile.close() 
        break
    if k == ord('q'):    # ord() return ascoo of 'q'. if q pressed, k will become ascii of q and loop break
        break
video.release()
cv2.destroyAllWindows()
