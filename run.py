from datetime import datetime, timedelta, timezone
from pprint import pprint
import threading
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from database.database import get_student_data, is_student_registered, register_user, save_image_to_firebase, update_student_info
from face_auth_services.ImageFunctionalites import check_face_in_image
from face_auth_services.VideoCapture import attendance_system
from utils.email_notification import send_otp_via_email
import numpy as np


app = Flask(__name__)


app.secret_key = 'your_secret_key'  # Always set a secret key for session management




@app.route("/")
def index():
    data=get_student_data()
    return render_template("index.html",data=data)


@app.route("/start-webcam", methods=["GET", "POST"])
# @jwt_required()
def start_webcam():
    print(f" start-webcam WEBCAM ACTIVE:{session.get('webcam_active')}")
    if not session.get('webcam_active'):
        session['webcam_active'] = True
        print(f" start-webcam WEBCAM ACTIVE:{session.get('webcam_active')}")
        threading.Thread(
            target=attendance_system, args=(session.get('webcam_active'),)
        ).start()
    return "Webcam started"


@app.route("/stop-webcam", methods=["GET", "POST"])
def stop_webcam():
    session.clear()
    session['webcam_active'] = False
    print(f" stop-webcam WEBCAM ACTIVE:{session.get('webcam_active')}")
    # destroy_opencv_windows()
    return "Webcam stopped"


@app.route('/send-otp', methods=['POST'])
def send_otp():
    pprint(request.json)
    student_id = request.json.get('student_id')
    session_data = session.get(f'{student_id}_otp')
    if session_data:
        stored_otp, timestamp = session_data
        if datetime.utcnow() - timestamp.replace(tzinfo=None) < timedelta(minutes=10):
            print(f'stored OTP:{stored_otp}')
            return "OTP Already Sent to your email"
    otp = send_otp_via_email(student_id)
    session[f'{student_id}_otp'] = (otp,datetime.now(timezone.utc))
    # session[f'{student_id}_otp'] = otp  # Store OTP in session?
    return "OTP Sent Successful"  # A form for OTP input



@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    pprint(request.json)
    user_input = int( request.json.get('otp'))
    student_id = request.json.get('student_id')
    session_data = session.get(f'{student_id}_otp')
    if session_data:
        stored_otp, timestamp = session_data
        # Check if the OTP is valid and within 10 minutes
        if user_input == stored_otp and  datetime.utcnow() - timestamp.replace(tzinfo=None) < timedelta(minutes=10):
            return "Valid OTP."
    else:
        return "Invalid OTP."
    


@app.route('/register-student', methods=['POST'])
def register_student():
    print("Registering student...")
    data = request.json
    pprint(data.keys())
    student_id = data.get('student_id')
    image_data = data.get('image').split(",")[1]
    
    try:
        if is_student_registered(student_id):
            return jsonify({"message": "Student already registered"}), 200
        # Ensure directory exists
        if check_face_in_image(image_data) is False:
            return jsonify({"message": "No face detected"}), 200
        save_image_to_firebase(student_id, image_data)
        # Register the user in Firestore
        register_user(student_id, f'resources/images/{student_id}.png')
        
        return jsonify({"message": "Student registered successfully"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500




@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == "admin" and password == "admin":  # Example credentials
        session['username'] = username
        return 'Login Sucessfull'
    else:
        return "Invalid username or password"
    # return render_template('index.html')  # Create a login.html template


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.clear()
    data=get_student_data()
    return render_template("index.html",data=data)


@app.route('/update', methods=['POST'])
def update_data():
    student_id = request.form['student_id']
    total_attendance = request.form['total_attendance']
    update_student_info(student_id, total_attendance)
    # Add more fields as necessary
    # Update other fields as necessary
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
