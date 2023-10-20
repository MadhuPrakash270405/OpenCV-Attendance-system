import re
import cv2
import face_recognition
import pickle
import os
import utils as UT
from icecream import ic

ic.configureOutput(prefix=f"[{UT.CURRENT_TIME}]", includeContext=True)
IMAGES_PATH = "resources/images"


student_images = UT.get_images(IMAGES_PATH)
student_ids = UT.get_student_ids(IMAGES_PATH)
ic(student_ids)


def findEncodings(student_images):
    ic("Encoding Started")
    encodingList = []
    for student_img in student_images:
        student_img_rgb = cv2.cvtColor(student_img, cv2.COLOR_BGR2RGB)
        encode_img = face_recognition.face_encodings(student_img_rgb)[0]
        encodingList.append(encode_img)
    ic("Encoding Ended")
    return encodingList


def save_to_pickle(encoded_studentImagesWithIds):
    pickle_file = open("EncodedPickle.p", "wb")
    pickle.dump(encoded_studentImagesWithIds, pickle_file)
    pickle_file.close()
    ic("Pickle File Saved")


def read_from_pickle():
    pickle_file = open("EncodedPickle.p", "rb")
    return pickle.load(pickle_file)


encoded_studentImages = findEncodings(student_images)
encoded_studentImagesWithIds = [encoded_studentImages, student_ids]
save_to_pickle(encoded_studentImagesWithIds)
