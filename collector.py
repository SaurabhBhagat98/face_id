# -*- coding: utf-8 -*-
"""
Created on Thu May  2 19:19:15 2019

@author: Omkar Shidore
https://www.github.com/OmkarShidore
"""
import cv2
import os
import pandas as pd
import csv
from functions import createFolder, employee_details_database,employee_access_details_database

def collector(Id,UserName,PhoneNumber,EmailId):
    #created folder for saving dataset images of user
    createFolder('./EmployeeDetails/dataSet')
    
    #creating employee_details
    try:
        if os.path.exists('./EmployeeDetails/employee_details.csv'):
            print('Details directory already exists')
        else:
            print("Details directory doesn't Exist")
            with open('./EmployeeDetails/employee_details.csv','w') as file:
                writer=csv.writer(file)
                writer.writerow(["Ids","UserNames","PhoneNumbers","EmailIds"])
            print("Creating new directory for employee_details.csv.")
    except OSError:
        print("File Already Exists")

    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    print("\n")
    Id=int(Id)
    UserName=UserName
    PhoneNumber=PhoneNumber
    EmailId=EmailId
    df=pd.read_csv('./EmployeeDetails/employee_details.csv')

    if int(Id) in df.values:
        print("\nEmployee already exists!!!")
        print("\nExiting.")
    else:
        print("\nCreating New User.")
        data=[{'Ids':Id,'UserNames':UserName,'PhoneNumbers':PhoneNumber,'EmailIds':EmailId}]
        df=pd.read_csv('./EmployeeDetails/employee_details.csv')
        df=df.append(data,ignore_index=True,sort=False)
        df.to_csv('./EmployeeDetails/employee_details.csv', index=False )
        df.drop(labels=['PhoneNumbers','UserNames'],axis=1,inplace=True)
        df=df.rename(columns={"Ids":"Passwords"})
        df.to_csv('./EmployeeDetails/employee_access_details.csv', index=False)

        sampleNum=0
        while True:
            ret, img = cam.read()
            ret, img1 = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        
                #incrementing sample number 
                sampleNum=sampleNum+1
                sampleNum1=str(sampleNum)
                text=sampleNum
                #saving the captured face in the dataset folder
                cv2.imwrite("EmployeeDetails/dataSet/User."+str(Id) +'.'+ UserName+'.'+str(sampleNum)+'.'+ ".jpg", gray[y:y+h,x:x+w])
        
                cv2.putText(img1,sampleNum1, (70, 150), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255), 3)
                cv2.imshow('Scans',img1)
        
            if cv2.waitKey(1)==27:
                break
            # break if the sample number is morethan 20
            elif sampleNum>99:
                break
        cam.release()
    cv2.destroyAllWindows()
    print("----Done----")
    employee_details_database()
    employee_access_details_database()



