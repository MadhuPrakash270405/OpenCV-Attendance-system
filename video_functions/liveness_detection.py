import cv2
import numpy as np
import mediapipe as mp


# Initialize mediapipe face detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)
face_mesh = mp.solutions.face_mesh.FaceMesh()


# Initialize mediapipe face detection and pose estimation
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.2, min_tracking_confidence=0.5
)


# A function to calculate the rotation vector from the landmarks
def get_rotation_vector(landmarks):
    image_points = np.array(
        [
            (landmarks[4].x, landmarks[4].y),  # Nose tip
            (landmarks[454].x, landmarks[454].y),  # Chin
            (landmarks[234].x, landmarks[234].y),  # Left eye left corner
            (landmarks[10].x, landmarks[10].y),  # Right eye right corner
            (landmarks[68].x, landmarks[68].y),  # Left mouth corner
            (landmarks[292].x, landmarks[292].y),  # Right mouth corner
        ],
        dtype="double",
    )

    model_points = np.array(
        [
            (0.0, 0.0, 0.0),  # Nose tip
            (0.0, -330.0, -65.0),  # Chin
            (-210.0, 135.0, -135.0),  # Left eye left corner
            (210.0, 135.0, -135.0),  # Right eye right corner
            (-150.0, -150.0, -125.0),  # Left mouth corner
            (150.0, -150.0, -125.0),  # Right mouth corner
        ]
    )
    size = (480, 640)  # Use appropriate resolution here
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
        dtype="double",
    )

    dist_coeffs = np.zeros((4, 1))
    _, rotation_vector, _ = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE,
    )
    return rotation_vector


def detect_faces(frame):
    # Process the frame and get the face detection results
    results = face_detection.process(frame)
    if results.detections:
        for face in results.detections:
            # Draw the face detection annotations on the frame
            mp_drawing.draw_detection(frame, face)
    num_faces = len(results.detections) if results.detections else 0
    # Display the frame with face detection annotations
    cv2.putText(
        frame,
        f"No of Face: {num_faces}",
        (10, 30),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        1,
        (0, 255, 0),
        1,
        cv2.LINE_AA,
    )


def liveness_detection(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(rgb_frame)

    if results.face_landmarks:
        landmarks = results.face_landmarks.landmark
        rotation_vector = get_rotation_vector(landmarks)

        # Determine if there's significant movement in any rotation direction
        threshold = 0.3
        if (
            abs(rotation_vector[0]) > threshold
            or abs(rotation_vector[1]) > threshold
            or abs(rotation_vector[2]) > threshold
        ):
            return "Live"

    return "Not Live"
