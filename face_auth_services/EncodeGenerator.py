import cv2
import face_recognition
import pickle
import os

from database.database import upload_file_to_firebase

# Importing student images
folderPath = os.path.abspath('resources/images')
pathList = os.listdir(folderPath)
print(pathList)
imgList = []



    # print(path
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


def encode_pickle_file():
    studentIds = []
    for path in pathList:
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        studentIds.append(os.path.splitext(path)[0])

        fileName = f'{folderPath}/{path}'
        upload_file_to_firebase(fileName)
    print("Encoding Started ...")
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Complete")
    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File Saved")


if __name__ == '__main__':
    encode_pickle_file()