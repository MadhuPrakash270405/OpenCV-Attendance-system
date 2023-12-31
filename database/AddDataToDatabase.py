import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

secret_key_path = os.path.abspath('../SecretKey.json')
cred = credentials.Certificate(secret_key_path)
firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendance-fa7ef-default-rtdb.firebaseio.com/",
    'storageBucket': "gs://faceattendance-fa7ef.appspot.com"
})

ref = db.reference('Students')

data = {
    "2845381":
        {
            "name": "Madhu Prakash",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2837016":
        {
            "name": "Sai Rohith Avula ",
            "major": "SE",
            "starting_year": 2021,
            "total_attendance": 0,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

    "2860024":
        {
            "name": "Indra Prasanth",
            "major": "SE",
            "starting_year": 2022,
            "total_attendance": 0,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)