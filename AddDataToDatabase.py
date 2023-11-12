import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("SecretKey.json")
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
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2837016":
        {
            "name": "Sai Rohith Avula ",
            "major": "SE",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)