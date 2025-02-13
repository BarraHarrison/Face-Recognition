# Python Program for Face Recognition
import threading
import cv2
from deepface import DeepFace




def verify_face(frame, reference_image, result_container):
    """
    Performs face verification using DeepFace.
    result_container updated with Boolean result.
    """
    try:
        verification = DeepFace.verify(frame, reference_image)["verified"]
        result_container["face_match"] = verification
    except ValueError:
        result_container["face_match"] = False


def __main__():
    capture_object = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    reference_image = cv2.imread("reference_image.jpg")
    if reference_image is None:
        print("Error: Could not load reference_image.jpg")
        return
    
    result_container = {"face_match": False}

    counter = 0

    try:
        while True:
            ret, frame = capture_object.read()
            if not ret:
                print("Error: Failed to read from capture device.")
                break

            if counter % 30 == 0:
                frame_copy = frame.copy()
                thread = threading.Thread(target=verify_face,args=(frame_copy, reference_image.copy(), result_container), daemon=True)
                thread.start()

            counter += 1

            if result_container["face_match"]:
                cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            cv2.imshow("Result", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break