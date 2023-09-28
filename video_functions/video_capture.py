import cv2
from liveness_detection import detect_faces, liveness_detection

# screen_width, screen_height = get_screen_resolution()


if __name__ == "__main__":
    # Capture video from default camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to fetch frame")
            continue
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detect_faces(frame)
        result = liveness_detection(frame)
        cv2.putText(
            frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2
        )
        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
