import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import  db
from firebase_admin import  storage


cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendacerealtime-2657a-default-rtdb.firebaseio.com/",
    "storageBucket":"faceattendacerealtime-2657a.appspot.com"
})


# importing all the student images url into imageModeList variable
folderPath='images'
PathList = os.listdir(folderPath)
print(PathList)
imageList=[]
studentid=[]
# print(modelPathList)
for path in PathList:
    imageList.append(cv2.imread(os.path.join(folderPath,path)))
    studentid.append(os.path.splitext(path)[0])

    filename=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)

# print(len(imageList))
# print((studentid))


def findEncodings(imageList):
    encodeList=[]
    for img in imageList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)


    return encodeList

print("encode start")
encodeListKnown=findEncodings(imageList)
encodeListKnownIds=[encodeListKnown,studentid]
print("encode complete")
print(encodeListKnown)


file=open("encodeFile.p","wb")
pickle.dump(encodeListKnownIds,file)
file.close()
print("file saved")