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

def attend_recognition():
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

                    attend_datetime=datetime.now()
                    attend_timestamp=datetime.timestamp(attend_datetime)
                
                
                    df=pd.read_csv(main_attendance_csv_path)

                    a=df.loc[df['Ids']==Id]['Attendance']=='Absent'
                    if a.all():

                        #issuing attendance in main_attendance
                        print("Marking Present for ")
                        df.loc[df['Ids']==Id,['Attendance','Attend_DateTime','Attend_TimeStamp','Leave_DateTime','Leave_TimeStamp']]=['Present',attend_datetime,attend_timestamp,'Not-Marked','Not-Marked']
                        df.to_csv(main_attendance_csv_path,index=False)
                    
                        main_attendance_database()
                    else:
                        print("Attendance already noted!")

                    student_path='./Attendance/employee_attendance/'+str(Id)+'_'+Name+'.csv'
                    df1=pd.read_csv(student_path)

                    data_row=[{'Name':Name,'Date':date_string,'Day':weekday,'Attendance':'Present'
                        ,'Attend_DateTime':attend_datetime,'Attend_TimeStamp':attend_timestamp,'Leave_DateTime':'Not-Marked','Leave_TimeStamp':'Not-Marked'}]
            
                    date_list=[]    #checking for list of dates in particular students csv file for marking new attendance
                    for i in df1.iloc[:,1]:
                        date_list.append(i)
                    if date_string in date_list:
                        print(Name)
                    else:
                        df1=df1.append(data_row)
                        df1.to_csv(student_path,index=False)
                        print('attendance saved for: '+Name)
                        employee_attendance_database()

                    cv2.putText(im,Id1,(x,y+h+20),font,0.7,(0,255,0), 2)
                    cv2.putText(im,Name,(x,y+h+38),font,0.7,(0,255,0), 2)
                    cv2.putText(im,conf_,(x,y+h+58),font,0.7,(0,255,0), 2)

                

                
                else:
                    Id1="Null"
                    Name="Unknown"
                    conf_=str(conf)
                
                    cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                    cv2.putText(im,Id1,(x,y+h+20),font,0.7,(0,0,255), 2)
                    cv2.putText(im,Name,(x,y+h+38),font,0.7,(0,0,255), 2)
                    cv2.putText(im,conf_,(x,y+h+58),font,0.7,(0,0,255), 2)
            else:
                Id1="User Id: Unknown"
                Name="User Name: Unknown"
                conf_='NuLL'
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.putText(im,Id1,(x,y+h+20),font,0.7,(0,0,255), 2)
                cv2.putText(im,Name,(x,y+h+38),font,0.7,(0,0,255), 2)
                cv2.putText(im,conf_,(x,y+h+58),font,0.7,(0,0,255), 2)
            #saving datetime and timestamp of the recognized frame


            print(Name)
        
        cv2.imshow('im',im)
        if cv2.waitKey(1)==27:
            break
    cam.release()
    cv2.destroyAllWindows()
