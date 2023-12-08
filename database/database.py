from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, storage,db
import numpy as np
import cv2
import logging
import base64
import io
from PIL import Image
import os

imgModeList, studentImages, encodeListKnown, studentIds = {}, {}, [], []

# Initialize Firebase
def initialize_firebase():
    global BUCKET, database
    try:
        secret_key_path = os.path.abspath('SecretKey.json')
        cred = credentials.Certificate(secret_key_path)
        
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": "https://faceattendance-fa7ef-default-rtdb.firebaseio.com/",
                "storageBucket": "faceattendance-fa7ef.appspot.com",
            },
        )
        BUCKET = storage.bucket()
        database = firestore.client()
        logging.info("Firebase initialized successfully.")
    except Exception as e:
        logging.error("initialize_firebase: Error initializing Firebase", exc_info=True)
        raise e

# Function to get data from Firebase
def get_student_data():
    ref = db.reference('Students')# Adjust this to your specific database structure
    return ref.get()

# Get Student Info from Firebase
def get_student_info(student_id):
    try:
        return db.reference(f"Students/{student_id}").get()
    except Exception as e:
        logging.error("get_student_info: Error getting student info", exc_info=True)
        return None

def get_student_image(student_id):
    try:
        if student_id not in studentImages:
            blob = BUCKET.blob(f"resources/images/{student_id}.png")
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            studentImages[student_id] = cv2.imdecode(array, cv2.IMREAD_COLOR)
        return studentImages[student_id]
    except Exception as e:
        logging.error("get_student_image: Error getting student image", exc_info=True)
        return None

# Check if the student is already registered
def is_student_registered(student_id):
    try:
        doc_ref = db.reference(f"RegisteredStudents/{student_id}")
        return True if doc_ref.get() else False
    except Exception as e:
        logging.error("is_student_registered: Error checking registration", exc_info=True)
        return False

# Register user
def register_user(student_id, image_url):
    try:
        ref = db.reference(f"RegisteredStudents/{student_id}")
        ref.set({
            "image_url": image_url,
            "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        logging.error("register_user: Error registering user", exc_info=True)

def save_image_to_firebase(student_id, image_data):
    try:
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        unknown_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        unknown_image = cv2.resize(unknown_image, (216, 216))

        resources_dir = 'resources/images'
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)

        local_image_path = os.path.join(resources_dir, f'{student_id}.png')
        cv2.imwrite(local_image_path, unknown_image)

        pil_image = Image.fromarray(cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB))
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)

        blob = BUCKET.blob(f'resources/images/{student_id}.png')
        blob.upload_from_file(buffer, content_type='image/png')
    except Exception as e:
        logging.error("save_image_to_firebase: Error saving image", exc_info=True)

def update_student_info(student_id, student_attendance):
    try:
        ref = db.reference(f"Students/{student_id}")
        ref.update({
            "total_attendance": int(student_attendance),
            "last_attendance_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        logging.error("update_student_info: Error updating student info", exc_info=True)


def upload_file_to_firebase(fileName):
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)