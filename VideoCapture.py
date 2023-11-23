import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
import logging

from email_notification import send_email

# Setup logging
log_filename = "face_attendance.log"
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create file handler which logs even debug messages
file_handler = logging.FileHandler(log_filename, mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)


# Add handlers to the root logger
logging.getLogger("").addHandler(file_handler)


# GLOBAL VARIABLES
BUCKET = None
imgModeList, studentImages, encodeListKnown, studentIds = {}, {}, [], []
MODE_TYPE = "active"
COUNTER = 0
opened_windows = []


# Initialize Firebase
def initialize_firebase():
    global BUCKET
    try:
        cred = credentials.Certificate("SecretKey.json")
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": "https://faceattendance-fa7ef-default-rtdb.firebaseio.com/",
                "storageBucket": "faceattendance-fa7ef.appspot.com",
            },
        )
        BUCKET = storage.bucket()
        logging.info("Firebase initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing Firebase: {e}")
        raise e


initialize_firebase()


# Load Resources
def load_resources():
    global imgModeList, encodeListKnown, studentIds
    try:
        imgBackground = cv2.imread("./resources/background.png")

        folderModePath = "resources/Modes"
        modePathList = os.listdir(folderModePath)
        for path in modePathList:
            filename = path.replace(".png", "")
            imgModeList[filename] = cv2.imread(os.path.join(folderModePath, path))

        logging.info("Loading Encode File...")
        with open("EncodeFile.p", "rb") as file:
            encodeListKnownWithIds = pickle.load(file)
        encodeListKnown, studentIds = encodeListKnownWithIds
        logging.info("Encode File Loaded")
        return imgBackground
    except Exception as e:
        logging.error(f"Error loading resources: {e}")
        raise e


def mode_image(imgBackground, MODE_TYPE):
    imgBackground[44 : 44 + 633, 808 : 808 + 414] = imgModeList[MODE_TYPE]


# Get Student Info from Firebase
def get_student_info(student_id):
    return db.reference(f"Students/{student_id}").get()


def get_student_image(student_id):
    if student_id not in studentImages:
        blob = BUCKET.get_blob(f"resources/images/{student_id}.png")
        array = np.frombuffer(blob.download_as_string(), np.uint8)
        studentImages[student_id] = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
    return studentImages[student_id]


def attendence_info(imgBackground, student_id):
    student_info = get_student_info(student_id)
    cv2.putText(
        imgBackground,
        str(student_info["total_attendance"]),
        (861, 125),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 255, 255),
        1,
    )
    cv2.putText(
        imgBackground,
        str(student_info["major"]),
        (1006, 550),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )
    cv2.putText(
        imgBackground,
        str(student_id),
        (1006, 493),
        cv2.FONT_HERSHEY_COMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )
    cv2.putText(
        imgBackground,
        str(student_info["standing"]),
        (910, 625),
        cv2.FONT_HERSHEY_COMPLEX,
        0.6,
        (100, 100, 100),
        1,
    )
    cv2.putText(
        imgBackground,
        str(student_info["year"]),
        (1025, 625),
        cv2.FONT_HERSHEY_COMPLEX,
        0.6,
        (100, 100, 100),
        1,
    )
    cv2.putText(
        imgBackground,
        str(student_info["starting_year"]),
        (1125, 625),
        cv2.FONT_HERSHEY_COMPLEX,
        0.6,
        (100, 100, 100),
        1,
    )
    (w, h), _ = cv2.getTextSize(student_info["name"], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
    offset = (414 - w) // 2
    cv2.putText(
        imgBackground,
        str(student_info["name"]),
        (808 + offset, 445),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (50, 50, 50),
        1,
    )
    send_email(
        student_name=student_info["name"],
        student_id=student_id,
        class_name="CIS 634-Software Engineering",
    )
    imgBackground[175 : 175 + 216, 909 : 909 + 216] = get_student_image(student_id)


# Update Attendance in Firebase
def update_attendance(imgBackground, student_id):
    global COUNTER, MODE_TYPE
    studentInfo = get_student_info(student_id)
    print(studentInfo)
    # Update data of attendance
    datetimeObject = datetime.strptime(
        studentInfo["last_attendance_time"], "%Y-%m-%d %H:%M:%S"
    )
    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
    print(secondsElapsed)
    if secondsElapsed > 30:
        ref = db.reference(f"Students/{student_id}")
        studentInfo["total_attendance"] += 1
        ref.child("total_attendance").set(studentInfo["total_attendance"])
        ref.child("last_attendance_time").set(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    else:
        MODE_TYPE = "already_marked"
        COUNTER = 0
        mode_image(imgBackground, MODE_TYPE)


# Function to check if any window is open
def is_any_window_open():
    return any(cv2.getWindowProperty(name, 0) >= 0 for name in opened_windows)


# Function to open a new window
def open_window(name, image):
    cv2.imshow(name, image)
    if name not in opened_windows:
        opened_windows.append(name)


def attendance_system(device_index, webcam_active):
    global MODE_TYPE, COUNTER, imgModeList, studentImages, encodeListKnown, studentIds
    studentId = ""
    cap = cv2.VideoCapture(device_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    try:
        x_offset, y_offset = 55, 162
        block_width, block_height = 640, 480
        imgBackground = load_resources()
        print(f"WEBCAM ACTIVE:{webcam_active}")
        while webcam_active:
            success, img = cap.read()
            if not success:
                logging.warning("Failed to capture image from camera.")
                continue
            img = cv2.flip(img, 1)
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            resized_frame = cv2.resize(img, (block_width, block_height))
            imgBackground[
                y_offset : y_offset + block_height, x_offset : x_offset + block_width
            ] = resized_frame
            mode_image(imgBackground, MODE_TYPE)

            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
            if faceCurFrame:
                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(
                        encodeListKnown, encodeFace
                    )
                    faceDis = face_recognition.face_distance(
                        encodeListKnown, encodeFace
                    )
                    matchIndex = np.argmin(faceDis)
                    if matches[matchIndex]:
                        studentId = studentIds[matchIndex]
                        if COUNTER == 0:
                            COUNTER = 1
                            MODE_TYPE = "student_info"

                if COUNTER != 0:
                    if COUNTER == 1:
                        update_attendance(imgBackground, studentId)
                    if MODE_TYPE != "already_marked":
                        if 10 < COUNTER < 20:
                            MODE_TYPE = "marked"
                        mode_image(imgBackground, MODE_TYPE)
                        if COUNTER <= 10:
                            attendence_info(imgBackground, studentId)
                        COUNTER += 1
                        if COUNTER >= 20:
                            COUNTER = 0
                            MODE_TYPE = "active"
                            studentInfo = []
                            imgStudent = []
                            mode_image(imgBackground, MODE_TYPE)
            else:
                MODE_TYPE = "active"
                COUNTER = 0
            # cv2.imshow("Webcam", img)
            # cv2.imshow("Face Attendance", imgBackground)
            open_window("Face Attendance", imgBackground)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logging.info("Face attendance system shut down.")
