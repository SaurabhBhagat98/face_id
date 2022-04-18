import os
import pandas as pd
import csv
import numpy as np
from datetime import datetime
from functions import createFolder,main_attendance_database,employee_attendance_database

def directory():
    #creating hierarchy of directories as Attendance/Year/Month/Day
    print("--Creating Main Attendance Directory.--")

    createFolder('./Attendance/main_attendance')

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

    today_path='./Attendance/main_attendance/'+year_dir+'/'+month_dir
    createFolder(today_path)
    date_string=year_dir+'-'+month_dir+'-'+day_dir
    filename=date_string+'_'+weekday

    #student details csv
    student_csv_path='./EmployeeDetails/employee_details.csv'

    #adding more columns to students csv and saving the sheet for main_attendance
    main_attendance_csv_path=today_path+'/'+filename+'.csv'
    df=pd.read_csv(student_csv_path)
    df["Attendance"]='Absent'
    df["Attend_DateTime"]=int(0)
    df["Attend_TimeStamp"]=float(0.0)
    df["Leave_DateTime"]=int(0)
    df["Leave_TimeStamp"]=float(0.0)
    df.to_csv(main_attendance_csv_path,index=False)
    print('--csv file created for main attendance--')


    #creating csv and directory for 
    if os.path.exists('./Attendance/employee_attendance'):

        for i in range(0,len(df)):
            student_csv_path='./Attendance/employee_attendance/'+str(df.iloc[i][0])+'_'+df.iloc[i][1]+'.csv'

            if os.path.exists(student_csv_path):
                pass
            else:
                data=['Name','Date','Day','Attendance','Attend_DateTime','Attend_TimeStamp','Leave_DateTime','Leave_TimeStamp']
                df1=pd.DataFrame(columns=data)
                df1.to_csv(student_csv_path,index=False)
                print('--csv file created for: '+df.iloc[i][1]+'--')

    else:
        createFolder('./Attendance/employee_attendance')
        print("--Created Student Attendance Directory--")
        data=['Name','Date','Day','Attendance','Attend_DateTime','Attend_TimeStamp','Leave_DateTime','Leave_TimeStamp']
        for i in range(0,len(df)):
            student_csv_path='./Attendance/employee_attendance/'+str(df.iloc[i][0])+'_'+df.iloc[i][1]+'.csv'
            df1=pd.DataFrame(columns=data)
            df1.to_csv(student_csv_path,index=False)
            print('--csv file created for: '+df.iloc[i][1]+'--')
        print('\n-----DONE-----')
    main_attendance_database()
    employee_attendance_database()