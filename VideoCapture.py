import cv2
import numpy as np
import ImageFunctionalites as IMGFunc
import utils as UT
import EncodeGenerator as EG
from icecream import ic

ic.configureOutput(prefix=f"[{UT.CURRENT_TIME}]", includeContext=True)


MODE_IMAGES_PATH = "resources/Modes"
screen_width, screen_height = IMGFunc.get_screen_resolution()

encoded_studentImages, student_ids = EG.read_from_pickle()

ic(student_ids)

if __name__ == "__main__":
    imgBackground = cv2.imread("resources/background.png")
    imageModeList = UT.get_images(MODE_IMAGES_PATH)
    # Capture video from default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        ic("Error: Could not open video.")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        imgBackground[162 : 162 + 480, 55 : 55 + 640] = frame
        imgBackground[44 : 44 + 633, 808 : 808 + 414] = imageModeList[3]
        ic("Selfie Mode enabled")
        if not ret:
            ic("Failed to fetch frame")
            continue
        # Convert the BGR image to RGB

        result = "alive"
        IMGFunc.add_text_to_frame(frame, result)
        cv2.imshow("Face Detection", imgBackground)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
