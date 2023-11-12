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

bucket = None
imgModeList,studentImages, encodeListKnown, studentIds={},{},[],[]
# Initialize Firebase
def initialize_firebase():
    global bucket
    cred = credentials.Certificate("SecretKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://faceattendance-fa7ef-default-rtdb.firebaseio.com/",
        'storageBucket': "faceattendance-fa7ef.appspot.com"
    })
    bucket = storage.bucket()


# Load Resources
def load_resources():
    global imgModeList, encodeListKnown, studentIds
    imgBackground = cv2.imread('./resources/background.png')

    folderModePath = 'resources/Modes'
    modePathList = os.listdir(folderModePath)
    for path in modePathList:
        filename=path.replace('.png', '')
        imgModeList[filename]=cv2.imread(os.path.join(folderModePath, path))

    print("Loading Encode File...")
    with open('EncodeFile.p', 'rb') as file:
        encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = encodeListKnownWithIds
    print("Encode File Loaded")
    return imgBackground


def mode_image(imgBackground,modeType):
     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

# Get Student Info from Firebase
def get_student_info(student_id):
    return db.reference(f'Students/{student_id}').get()


def get_student_image(student_id):
    if student_id not in studentImages:
        blob = bucket.get_blob(f'resources/images/{student_id}.png')
        array = np.frombuffer(blob.download_as_string(), np.uint8)
        studentImages[student_id] = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
    return studentImages[student_id]

def attendence_info(imgBackground,student_id):
        student_info=get_student_info(student_id)
        cv2.putText(imgBackground, str(student_info['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(student_info['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(student_id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(imgBackground, str(student_info['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(student_info['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(imgBackground, str(student_info['starting_year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        (w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground, str(student_info['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
        imgBackground[175:175 + 216, 909:909 + 216] = get_student_image(student_id)



# Update Attendance in Firebase
def update_attendance(imgBackground,student_id):
        global counter,modeType
        studentInfo = get_student_info(student_id)
        print(studentInfo)
        # Update data of attendance
        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                        "%Y-%m-%d %H:%M:%S")
        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
        print(secondsElapsed)
        if secondsElapsed > 30:
            ref = db.reference(f'Students/{studentId}')
            studentInfo['total_attendance'] += 1
            ref.child('total_attendance').set(studentInfo['total_attendance'])
            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            modeType = 'already_marked'
            counter = 0
            mode_image(imgBackground,modeType)

modeType = 'active'
counter = 0
id = -1
imgStudent = []


if __name__ == "__main__":
    initialize_firebase()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    x_offset,y_offset = 55,162
    block_width,block_height = 640,480
    imgBackground = load_resources()
    while True:
        success, img = cap.read()
        img= cv2.flip(img,1)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(img, (block_width, block_height))
        imgBackground[y_offset:y_offset + block_height, x_offset:x_offset + block_width] = resized_frame
        mode_image(imgBackground,modeType)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    studentId = studentIds[matchIndex]
                    if counter == 0:
                        counter = 1
                        modeType = 'student_info'

            if counter != 0:
                if counter == 1:
                    update_attendance(imgBackground,studentId)
                if modeType != 'already_marked':
                    if 10 < counter < 20:
                        modeType = 'marked'
                    mode_image(imgBackground,modeType)
                    if counter <= 10:
                        attendence_info(imgBackground,studentId)
                    counter += 1
                    if counter >= 20:
                        counter = 0
                        modeType = 'active'
                        studentInfo = []
                        imgStudent = []
                        mode_image(imgBackground,modeType)
        else:
            modeType = 'active'
            counter = 0
        # cv2.imshow("Webcam", img)
        cv2.imshow("Face Attendance", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
