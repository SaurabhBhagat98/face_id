# -*- coding: utf-8 -*-
"""
Created on Thu May  2 20:19:45 2019

@author: Omkar Shidore
https://www.github.com/OmkarShidore
"""

import os
import cv2
import numpy as np
from PIL import Image
import time
from functions import createFolder

def modelTrainer():
    print('\nModule Versions: ')
    print('OpenCv: '+cv2.__version__, '\nNumpy: '+np.__version__,'\nPillow>>Image: '+Image.__version__)
    print('\nTraining Initialized...')
    start_time = time.time()
    #Creatung directories

        
    createFolder('./Model/') 

    #recognizer = cv2.face.createLBPHFaceRecognizer()
    #recognizer = cv2.face.LBPHFaceRecognizer_create()
    #OpenCv: 4.1.2
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        #empty lists for storing Lables and features
        faceSamples=[]
        Ids=[]
        for imagePath in imagePaths:
        
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces=detector.detectMultiScale(imageNp)
            for (x,y,w,h) in faces:
                faceSamples.append(imageNp[y:y+h,x:x+w])
                Ids.append(Id)
        return faceSamples,Ids
    start_time = time.time()
    faces,Ids = getImagesAndLabels('./EmployeeDetails/dataSet')

    #training model on dataSet
    recognizer.train(faces, np.array(Ids))
    #trainer.yml stored in the folder trainer
    recognizer.save('Model/model.yml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('Model/model.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    print("----Training Done in : %s seconds----" % (time.time() - start_time))
