import cv2
from deepface import DeepFace

def detect_emotion():
    cap = cv2.VideoCapture(0)
    print("Press 'q' to capture your face for emotion detection.")

    frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Emotion Detector", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    try:
        analysis = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        return analysis[0]['dominant_emotion']
    except Exception as e:
        return f"Error: {e}" 