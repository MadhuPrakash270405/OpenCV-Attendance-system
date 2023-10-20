import cv2
from icecream import ic
from datetime import datetime

import numpy as np

# Get the current time in 12-hour format
current_time = datetime.now().strftime("%I:%M:%S %p")
ic.configureOutput(prefix=f"[{current_time}]", includeContext=True)

import image_functions.image_functionalities as IMGFunc

screen_width, screen_height = IMGFunc.get_screen_resolution()


if __name__ == "__main__":
    imgBackground = cv2.imread("resources/images/background.png")
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
