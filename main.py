import os
import pickle
import time
import cvzone
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import  db
from firebase_admin import  storage
from datetime import  datetime


cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendacerealtime-2657a-default-rtdb.firebaseio.com/",
    "storageBucket":"faceattendacerealtime-2657a.appspot.com"
})
bucket=storage.bucket()


modeType=0
counter =0
id=-1
imagestudent=[]


cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)
backgroundimg = cv2.imread('Resources/background.png')

# importing all the resource mode images url into imageModeList variable
folderModePath='Resources/Modes'
modelPathList = os.listdir(folderModePath)
imagemodeList=[]
# print(modelPathList)
for path in modelPathList:
    imagemodeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imagemodeList))

# load the encoding file
print("loading encode file")
file=open("encodeFile.p","rb")
encodeListKnownIds=pickle.load(file)
file.close()
encodeListKnown,studentid = encodeListKnownIds
print(studentid)
print("encod file loaded")



while True:
    sucess,img = cap.read()

    imageS=cv2.resize(img,(0,0),None,0.25,0.25)
    imageS=cv2.cvtColor(imageS,cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imageS)
    encodeCurrFrame = face_recognition.face_encodings(imageS,faceCurrFrame)

    backgroundimg[162:162+480,55:55+640]=img
    backgroundimg[44:44+641, 808:808+416] = imagemodeList[modeType]

    # if faceCurrFrame:

    for encodeFace,faceLoc in zip(encodeCurrFrame,faceCurrFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
        # print("matches",matches)
        # print("faceDIs",faceDis)
        matchindex=np.argmin(faceDis)
        # print(matchindex)
        if(matches[matchindex]):
            y1,x2,y2,x1=faceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
            bbox=55+x1,162+y1,x2-x1,y2-y1
            backgroundimg=cvzone.cornerRect(backgroundimg,bbox)
            id=studentid[matchindex]

            if counter==0:
                cvzone.putTextRect(backgroundimg,"Loading..",(275,400))
                cv2.imshow("Attendance System", backgroundimg)
                cv2.waitKey(1)
                counter=1
                modeType=1

    if counter!=0:
        if counter==1:
            # get the data into dictionary
            studentinfo=db.reference(f'Students/{id}').get()
            print(studentinfo)
            # get the image
            blob=bucket.get_blob(f'images/{id}.jpg')
            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imagestudent=cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

            # update the attendance
            # datetimeobj=datetime.strptime(studentinfo['last_attendance_time'],"%Y-%m-%d %H:%M:S")
            # secondelapsed=(datetime.now()-datetimeobj).total_seconds()
            datetimeobj=datetime.strptime(studentinfo['last_attendance_time'],"%Y-%m-%d %H:%M:%S")
            secondelapsed = (datetime.now() - datetimeobj).total_seconds()
            print(secondelapsed)
            if secondelapsed>10:
                ref = db.reference(f'Students/{id}')
                studentinfo['total_attendance']+=1
                ref.child('total_attendance').set(studentinfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                modeType=3
                counter=0
                backgroundimg[44:44 + 641, 808:808 + 416] = imagemodeList[modeType]
        if modeType!=3:
            if 10<counter<20:
                modeType=2
            backgroundimg[44:44 + 641, 808:808 + 416] = imagemodeList[modeType]


            if counter<=10:

                cv2.putText(backgroundimg,str(studentinfo["total_attendance"]),(861,125),
                            cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),2)

                cv2.putText(backgroundimg, str(studentinfo["major"]), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
                cv2.putText(backgroundimg, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
                cv2.putText(backgroundimg, str(studentinfo["standings"]), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
                cv2.putText(backgroundimg, str(studentinfo["year"]), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
                cv2.putText(backgroundimg, str(studentinfo["starting_year"]), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)
                (w,h),_ =cv2.getTextSize(studentinfo['name'],cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,1)
                offset=(414-w)//2
                cv2.putText(backgroundimg, str(studentinfo["name"]), (808+offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                backgroundimg[175:175+216,909:909+216]=imagestudent

            counter+=1



            if counter>=20:
                counter=0
                modeType=0
                studentinfo=[]
                imagestudent=[]
                backgroundimg[44:44 + 641, 808:808 + 416] = imagemodeList[modeType]

    # cv2.imshow("Face Read",img)
    cv2.imshow("Attendance System",backgroundimg)
    cv2.waitKey(1)



