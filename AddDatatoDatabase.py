import firebase_admin
from firebase_admin import credentials
from firebase_admin import  db


cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://faceattendacerealtime-2657a-default-rtdb.firebaseio.com/"
})

ref= db.reference("Students")

data={
    "202080":{
        "name":"elon Musk",
        "major":"Artificial Int",
        "starting_year":2008,
        "total_attendance":5,
        "standings":"G",
        "year":4,
        "last_attendance_time":"2002-12-23 00:56:31"
    },
    "203270":{
            "name":"Gaurav Zade",
            "major":"CS Engg",
            "starting_year":2020,
            "total_attendance":10,
            "standings":"G",
            "year":4,
            "last_attendance_time":"2002-12-11 00:56:31"
        },
    "202118":{
            "name":"Aman Ramteke",
            "major":"AI Engg",
            "starting_year":2020,
            "total_attendance":10,
            "standings":"G",
            "year":4,
            "last_attendance_time":"2002-12-10 00:56:31"
        },
    "203280":{
            "name":"Dhammadip Mendhe",
            "major":"IT Engg",
            "starting_year":2020,
            "total_attendance":10,
            "standings":"G",
            "year":4,
            "last_attendance_time":"2002-12-10 00:56:31"
        }
}

for key, value in data.items():
    ref.child(key).set(value)