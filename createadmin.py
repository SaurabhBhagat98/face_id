import cv2
import os
import pandas as pd
import csv
from functions import createFolder,admin_details_database

def createadmin(AdminId,AdminUserName,AdminPhoneNumber,AdminEmailId,AdminPassword):
    


    AdminId=int(AdminId)
    AdminUserName=AdminUserName
    AdminPhoneNumber=AdminPhoneNumber
    AdminEmailId=AdminEmailId
    AdminPassword=AdminPassword

    df=pd.read_csv('./AdminDetails/admin_details.csv')

    if int(AdminId) in df['AdminIds'].values:
        print("\nAdmin already exists!!!")
        print("\nExiting.")
    else:
        print("\nCreating New Admin.")
        data=[{'AdminIds':AdminId,'AdminUserNames':AdminUserName,'AdminPhoneNumbers':AdminPhoneNumber,'AdminEmailIds':AdminEmailId,'AdminPasswords':AdminPassword}]
        df=pd.read_csv('./AdminDetails/admin_details.csv')
        df=df.append(data,ignore_index=True,sort=False)
        df.to_csv('./AdminDetails/admin_details.csv', index=False )
    admin_details_database()