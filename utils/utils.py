import re
import cv2
import os
from datetime import datetime

# Get the current time in 12-hour format
CURRENT_TIME = datetime.now().strftime("%I:%M:%S %p")

PATTERN = re.compile(r"\.\w+$")


def get_images(folderPath):
    PathList = os.listdir(folderPath)
    return [cv2.imread(os.path.join(folderPath, path)) for path in PathList]


def get_student_ids(folderPath):
    PathList = os.listdir(folderPath)
    return [re.sub(PATTERN, "", filename) for filename in PathList]
