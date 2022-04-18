# -*- coding: utf-8 -*-
"""
Created on Fri May  3 00:37:50 2019

@author: Omkar Shidore
https://www.github.com/OmkarShidore     
"""
import os
import cv2
import pandas as pd
import csv
import numpy as np
from datetime import datetime
from functions import createFolder,keyValuePairs,employee_attendance_database,main_attendance_database

def leave_recognition():
    #DateTime,TimeStamp,WeekDay Variable
    now=datetime.now()
    year_dir=str(now.year)
    month_dir=str(now.month)
    if len(month_dir)==2:
        pass
    else:
        month_dir='0'+str(now.month)

    day_dir=str(now.day)
    if len(day_dir)==2:
        pass
    else:
        day_dir='0'+str(now.day)
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    weekday=str(weekDays[now.weekday()])
    filename='_'+weekday
    date_string=year_dir+'-'+month_dir+'-'+day_dir
    filename=date_string+'_'+weekday

    #main attendance path and csv file
    today_path='./Attendance/main_attendance/'+year_dir+'/'+month_dir
    main_attendance_csv_path=today_path+'/'+filename+'.csv'
    print(main_attendance_csv_path)
    df=pd.read_csv(main_attendance_csv_path)

    #Loading Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('Model/model.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    #getting Id,Name from Image
    Ids,UserNames,keyValues=keyValuePairs('EmployeeDetails/dataSet')

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.3,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf>40 and conf<100):
                if Id in keyValues.keys():
                    Id1= 'User Id  : '+str(Id)
                    Name=keyValues[Id]
                    Name_=Name
                    Name1='User Name: '+Name
                    conf_=str(conf)

                    leave_datetime=datetime.now()
                    leave_timestamp=datetime.timestamp(leave_datetime)

                    #script for noting main_attendance Leave    
                    a=df.loc[df['Ids']==Id]['Leave_DateTime']=='Not-Marked'
                    if a.all():
                        #issuing attendance in main_attendance
                        print("Marking Leave for ")
                        df.loc[df['Ids']==Id,['Leave_DateTime','Leave_TimeStamp']]=[leave_datetime,leave_timestamp]
                        df.to_csv(main_attendance_csv_path,index=False)
                        main_attendance_database()
                    else:
                        print("Leave already noted!")

                    student_path='./Attendance/employee_attendance/'+str(Id)+'_'+Name+'.csv'
                    df1=pd.read_csv(student_path)
                    b=df1.loc[df1['Date']==date_string]['Leave_DateTime']=='Not-Marked'

                    if b.all():
                        #issuing attendance in main_attendance
                        print("Marking Leave for ")
                        df1.loc[df1['Date']==date_string,['Leave_DateTime','Leave_TimeStamp']]=[leave_datetime,leave_timestamp]
                        df1.to_csv(student_path,index=False)
                        employee_attendance_database()

                    #red bounding box,font for Unknown User
                    cv2.putText(im,Id1,(x,y+h+20),font,0.7,(0,255,0), 2)
                    cv2.putText(im,Name,(x,y+h+38),font,0.7,(0,255,0), 2)
                    cv2.putText(im,conf_,(x,y+h+58),font,0.7,(0,255,0), 2)
                
                
                else:
                    Id1="Null"
                    Name="Unknown"
                    conf_=str(conf)

                    #red bounding box,font for Unknown User
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                    cv2.putText(im,Id1,(x,y+h+20),font,0.7,(0,0,255), 2)
                    cv2.putText(im,Name,(x,y+h+38),font,0.7,(0,0,255), 2)
                    cv2.putText(im,conf_,(x,y+h+58),font,0.7,(0,0,255), 2)
            else:
                Id1="User Id: Unknown"
                Name="User Name: Unknown"
                conf_='NuLL'

                #red bounding box,font for Unknown User
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.putText(im,Id1,(x,y+h+20),font,0.7,(0,0,255), 2)
                cv2.putText(im,Name,(x,y+h+38),font,0.7,(0,0,255), 2)
                cv2.putText(im,conf_,(x,y+h+58),font,0.7,(0,0,255), 2)
            print(Name)
        
        cv2.imshow('im',im) 
        if cv2.waitKey(1)==27:
            break
    cam.release()
    cv2.destroyAllWindows()