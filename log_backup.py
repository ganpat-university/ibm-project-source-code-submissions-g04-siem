import os
import time
import datetime
import zipfile

#For uploading to Google Drive
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

#Date calculation
timestamp_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

#Today's date
date_today = datetime.datetime.now()
date_today = [date_today.day,date_today.month,date_today.year]
print(date_today)

cwd = os.getcwd()
#print(cwd)
log_dir = os.chdir(cwd+'/Logs')
#print(log_dir)

file_dict = {}

log_files = os.listdir(log_dir) # returns list
for i in log_files:
    #Getting time created/modified of the file (WINDOWS ONLY!!!!)
    timestamp = time.asctime(time.gmtime(os.path.getctime(i)))
    timestamp = timestamp.split(" ")
    
    #Separating the Month with its index,ex: "Sep" and replacing it with '9'
    if timestamp[1] in timestamp_months:
        timestamp[1]= timestamp_months.index(timestamp[1]) + 1
    
    #Checking if timestamp[2]=='', if not, insert ''
    if timestamp[2]!='':
        timestamp.insert(2,'')
        
    #Maintaining a File dictionary with individual dates of each filename as key and timestamp info as value
    #Timestamp format will be DD:MM:YYYY
    file_dict[i]= [int(timestamp[3]),int(timestamp[1]),int(timestamp[5])]

ZipFile = zipfile.ZipFile("Logs as of "+str(date_today[0]-1)+"-"+str(date_today[1])+"-"+str(date_today[2])+".zip", "w" )

#Segragating log files and identifying if they are from yesterday, if yes, then adding them into a zipfile
for i in file_dict:
    #print(i + "\t",file_dict[i])
    
    #Checking if file has yesterday's date
    if(file_dict[i][0]==date_today[0]) and (file_dict[i][1]==date_today[1]) and file_dict[i][2]==date_today[2]:
        #print(i)
        path_for_file = os.getcwd() + "\\"+ i
        #print(path_for_file)
        ZipFile.write(path_for_file, compress_type=zipfile.ZIP_DEFLATED,arcname=i)

ZipFile.close()

print("A zip file of Yesterday's log files has been created at path: ")
print(os.getcwd()+"\\"+"Logs as of "+str(date_today[0]-1)+"-"+str(date_today[1])+"-"+str(date_today[2])+".zip")

#Uploading to Google Drive

print("\n\n\n\n")
print("************************ CALLING THE GOOGLE DRIVE API ************************\n\n")
CLIENT_SECRET_FILE = 'C:\\Users\\Admin\\Desktop\\SEM 7\\Security Incident and Event Management\\Project\\client_secret_187230046648-o49b4bhrj7relt8dn5oha1cjeh5m196d.apps.googleusercontent.com.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

Google_Drive_Folder = "1aL4tIRuN-DbL46lQdNH440byGE58AjK-" #Drive ID of the folder
file_to_upload = "Logs as of "+str(date_today[0]-1)+"-"+str(date_today[1])+"-"+str(date_today[2])+".zip"
file_mime_type = "application/zip"

file_metadata = {
    'name' : file_to_upload,
    'parents' : [Google_Drive_Folder] 
}
log_file_path = os.getcwd()+"\\"+"Logs as of "+str(date_today[0]-1)+"-"+str(date_today[1])+"-"+str(date_today[2])+".zip"
media = MediaFileUpload(log_file_path,mimetype=file_mime_type)

service.files().create(body=file_metadata,media_body=media,fields='id').execute()

