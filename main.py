from collector import collector
from directory import directory
from createadmin import createadmin
from modelTrainer import modelTrainer
from attend_recognition import attend_recognition
from leave_recognition import leave_recognition
from functions import employee_details_database,date,createFolder

from tkinter import *
import pandas as pd
import time
import os
import re
import csv



font_heading="none 12 bold"
font="none 10 bold"

window=Tk()
window.title("Upasthti")

#collector.py defination
def collector_submit():
    Id=id_entry.get()
    UserName=username_entry.get()
    PhoneNumber=phonenumber_entry.get()
    EmailId=emailid_entry.get()
    
    if os.path.exists('./EmployeeDetails/employee_details.csv'):
        df=pd.read_csv('./EmployeeDetails/employee_details.csv')

        #Input validation and checking if particular detail already exists in database
        if int(Id) in df['Ids'].values:
            output.delete(0.0,END)
            output.insert(END,'Database Error: User ID Already Exists')
        elif len(PhoneNumber)!=10 :
            output.delete(0.0,END)
            output.insert(END,'Input Validation Error: Wrong Phone Number')
        elif int(PhoneNumber) in df['PhoneNumbers'].values:
            output.delete(0.0,END)
            output.insert(END,'Database Error: Phone Number Already Exist')
        elif EmailId in df['EmailIds'].values:
            output.delete(0.0,END)
            output.insert(END,'Database Error: Email Id Already Exist')
        else:
            output.delete(0.0,END)
            try:
                collector(Id,UserName,PhoneNumber,EmailId)
                output_string='New User Created: '+UserName
            except Exception as e:
                print(f"Failure: {e}")
            output.insert(END,output_string)
    else:
        if len(PhoneNumber)!=10 :
            output.delete(0.0,END)
            output.insert(END,'Input Validation Error: Wrong Phone Number')
        output.delete(0.0,END)
        try:
            collector(Id,UserName,PhoneNumber,EmailId)
            
            output_string='New User Created: '+UserName
        except Exception as e:
            print(f"Failure: {e}")
            output_string="Failed"
        output.insert(END,output_string)


#createadmin defination
def createadmin_submit():
    password=password_entry.get()
    if password=='upasthiti@123':
        try:
            window2=Tk()
            window2.title("Admin Pannel")
            
            def createadmin_submit1():

                createFolder('./AdminDetails')
                try:
                    if os.path.exists('./AdminDetails/admin_details.csv'):
                        print('Details directory already exists')
                    else:
                        print("Details directory doesn't Exist")
                        with open('./AdminDetails/admin_details.csv','w') as file:
                            writer=csv.writer(file)
                            writer.writerow(["AdminIds","AdminUserNames","AdminPhoneNumbers","AdminEmailIds","AdminPasswords"])
                        print("Creating new directory for employee_details.csv.")
                except OSError:
                    print("File Already Exists")


                AdminId=admin_id_entry.get()
                AdminUserName=admin_username_entry.get()
                AdminPhoneNumber=admin_phonenumber_entry.get()
                AdminEmailId=admin_emailid_entry.get()
                AdminPassword=admin_password_entry.get()

                df=pd.read_csv('./AdminDetails/admin_details.csv')
                if int(AdminId) in df['AdminIds'].values:
                    output.delete(0.0,END)
                    output.insert(END,'Database Error: Admin ID Already Exists')
                elif len(AdminPhoneNumber)!=10 :
                    output.delete(0.0,END)
                    output.insert(END,'Input Validation Error: Wrong Phone Number')
                elif int(AdminPhoneNumber) in df['AdminPhoneNumbers'].values:
                    output.delete(0.0,END)
                    output.insert(END,'Database Error: Phone Number Already Exist')
                elif AdminEmailId in df['AdminEmailIds'].values:
                    output.delete(0.0,END)
                    output.insert(END,'Database Error: Email Id Already Exist')
                else:
                    output.delete(0.0,END)
                    try:
                        createadmin(AdminId,AdminUserName,AdminPhoneNumber,AdminEmailId,AdminPassword)
                        output_string='New Admin Created: '+AdminUserName
                    except:
                        output_string="Failed to create Admin"
                    output.insert(END,output_string)

            #------------Admin----------------#
            #createadmin.py 
            Label(window2,text=" Create Admin User",font='none 13 bold').grid(row=0,column=0,sticky=W)
            #AdminId label 
            Label(window2,text="Admin Id Number: ",font=font).grid(row=2,column=1,sticky=W)
            #AdminId textbox 
            admin_id_entry=Entry(window2,width=20,bg="white")
            admin_id_entry.grid(row=2,column=2,sticky=W)
            print(type(id_entry))
            #UserName label 
            Label(window2,text="Full Name: ",font=font).grid(row=3,column=1,sticky=W)
            #UserName textbox 
            admin_username_entry=Entry(window2,width=20,bg="white")
            admin_username_entry.grid(row=3,column=2,sticky=W)

            #PhoneNumber label
            Label(window2,text="Phone Number: ",font=font).grid(row=4,column=1,sticky=W)
            #UserName textbox
            admin_phonenumber_entry=Entry(window2,width=20,bg="white")
            admin_phonenumber_entry.grid(row=4,column=2,sticky=W)

            #EmailId label 
            Label(window2,text="Email Id: ",font=font).grid(row=5,column=1,sticky=W)
            #UserName textbox 
            admin_emailid_entry=Entry(window2,width=20,bg="white")
            admin_emailid_entry.grid(row=5,column=2,sticky=W)

            #EmailId label 
            Label(window2,text="Password: ",font=font).grid(row=6,column=1,sticky=W)
            #UserName textbox 
            admin_password_entry=Entry(window2,show='*',width=20,bg="white")
            admin_password_entry.grid(row=6,column=2,sticky=W)


            #submit button
            Button(window2,text="Create Admin",width=10,command=createadmin_submit1).grid(row=7,column=1,sticky=W)
            #------------Collector End----------------#
            #Output Label
            Label(window2,text="Output: ",font=font_heading).grid(row=16,column=0,sticky=W)
            output=Text(window2,width=100,height=6,wrap=WORD,background="white")
            output.grid(row=17,columnspan=10,sticky=W)
            window2.mainloop()
        except:
            output.delete(0.0,END)
            output.insert(END,'Failed to run createadmin script')
        

#directory.py defination
def directory_submit():
    try:
        directory()
        filename=date()
        output.delete(0.0,END)
        output_string='Sheet Created For: '+filename
    except:
        output_string='Failed to create Directory'
    output.delete(0.0,END)
    output.insert(END,output_string)   

def modelTrainer_submit():
    output.delete(0.0,END)
    output.insert(END,'Training Initialized, Please Wait...') 
    try:
        start_time = time.time()
        modelTrainer()
        output_string="----Training Done in : %s seconds----" % (time.time() - start_time)
    except Exception as e:
        print(f"Training failde: {e}")
        output_string='Failed to create Directory'
    output.delete(1.0,END)
    output.insert(END,output_string)  


#attend recognition
def attend_recognition_submit():
    output.delete(0.0,END)
    #output.insert(END,'Attend Facial Recognition Initialized') 
    try:
        attend_recognition()
    except:
        output_string='Failed to run attend_recognition script'
        output.insert(0.0,output_string)
    output.insert(0.1,'Done Attend Recognition') 

#leave recognition
def leave_recognition_submit():
    output.delete(0.0,END)
    #output.insert(END,'Leave Facial Recognition Initialized') 
    try:
        leave_recognition()
    except:
        output_string='Failed to run leave_recognition script'
        output.insert(0.0,output_string)
    output.insert(0.0,'Done Leave Recognition') 

def close_window():
    window.destory()
    exit()

#heading label
Label(window,text="Upasthiti-ai",font="none 16 bold").grid(row=1,column=0,sticky=W)

#------------Collector----------------#
#collector.py R0 C0
Label(window,text="1. Create New User",font=font_heading).grid(row=1,column=0,sticky=W)
#Id label R1 C0
Label(window,text="User Id Number: ",font=font).grid(row=2,column=1,sticky=W)
#Id textbox R1 C1
id_entry=Entry(window,width=20,bg="white")
id_entry.grid(row=2,column=2,sticky=W)
print(type(id_entry))
#UserName label R1 C2
Label(window,text="Full Name: ",font=font).grid(row=2,column=3,sticky=W)
#UserName textbox R1 C3
username_entry=Entry(window,width=20,bg="white")
username_entry.grid(row=2,column=4,sticky=W)

#PhoneNumber label R1 C4
Label(window,text="Phone Number: ",font=font).grid(row=2,column=5,sticky=W)
#UserName textbox R1 C5
phonenumber_entry=Entry(window,width=20,bg="white")
phonenumber_entry.grid(row=2,column=6,sticky=W)

#EmailId label R1 C6
Label(window,text="Email Id: ",font=font).grid(row=2,column=7,sticky=W)
#UserName textbox R1 C7
emailid_entry=Entry(window,width=20,bg="white")
emailid_entry.grid(row=2,column=8,sticky=W)


#submit button
Button(window,text="Create User",width=10,command=collector_submit).grid(row=2,column=10,sticky=W)



#------------Collector End----------------#



#------------modelTrainer----------------#



Label(window,text="2. Train Machine Learning Model ",font=font_heading).grid(row=4,column=0,sticky=W)

Button(window,text="Train Model",width=10,command=modelTrainer_submit).grid(row=5,column=10,sticky=W)


#------------modelTrainer End----------------#

#------------Directory----------------#

#directory.py R0 C0

#press button label
Label(window,text="3. Create Todays Attendance Sheet ",font=font_heading).grid(row=7,column=0,sticky=W)

#submit button
Button(window,text="Create Sheet",width=10,command=directory_submit).grid(row=8,column=10,sticky=W)

#------------Directory End----------------#



#------------attend_recognition----------------#

#directory.py R0 C0

#press button label
Label(window,text="4. Facial Attend Recognition ",font=font_heading).grid(row=10,column=0,sticky=W)

#submit button
Button(window,text="Attend Start",width=10,command=attend_recognition_submit).grid(row=11,column=10,sticky=W)

#------------attendRcognition end----------------#


#------------attend_recognition----------------#

#directory.py R0 C0

#press button label
Label(window,text="5. Facial Leave Recognition ",font=font_heading).grid(row=13,column=0,sticky=W)

#submit button
Button(window,text="Leave Start",width=10,command=leave_recognition_submit).grid(row=14,column=10,sticky=W)



#------------attendRcognition end----------------#




#Output Label
Label(window,text="Output: ",font=font_heading).grid(row=16,column=0,sticky=W)
output=Text(window,width=100,height=6,wrap=WORD,background="white")
output.grid(row=17,columnspan=10,sticky=W)


#admin label
Label(window,text="Password: ",font=font).grid(row=18,column=9,sticky=W)
#admin text
password_entry=Entry(window,show='*',width=20,bg="white")
password_entry.grid(row=18,column=10,sticky=W)

#admin button
Button(window,text="Create Admin",width=10,command=createadmin_submit).grid(row=19,column=10,sticky=W)

window.mainloop()