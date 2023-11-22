import threading
from flask import Flask, render_template, request
import cv2
from VideoCapture import attendance_system

app = Flask(__name__)

webcam_active = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start-webcam", methods=["GET", "POST"])
def start_webcam():
    global webcam_active
    print(f" start-webcam WEBCAM ACTIVE:{webcam_active}")
    if not webcam_active:
        device_index = 0
        webcam_active = True
        threading.Thread(
            target=attendance_system, args=(device_index, webcam_active)
        ).start()
    return "Webcam started"


@app.route("/stop-webcam", methods=["GET", "POST"])
def stop_webcam():
    global webcam_active
    webcam_active = False
    destroy_opencv_windows()
    return "Webcam stopped"


if __name__ == "__main__":
    app.run(debug=True)
