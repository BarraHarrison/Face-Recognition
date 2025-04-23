# Python Program for Face Recognition
import threading
import cv2
import os
from deepface import DeepFace

DeepFace.build_model("VGG-Face")

def verify_face(frame, reference_image, result_container):
    """
    Performs face verification using DeepFace.
    result_container updated with Boolean result.
    """
    try:
        for ref_img in reference_image:
            verification = DeepFace.verify(frame, ref_img, model_name="VGG-Face")["verified"]
            if verification:
                result_container["face_match"] = True
                return
        result_container["face_match"] = False
    except ValueError:
        result_container["face_match"] = False


def main():
    capture_object = cv2.VideoCapture(0)
    capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    reference_images = [
        cv2.imread("reference_image.jpg"),
        cv2.imread("reference_left.jpg"),
        cv2.imread("reference_right.jpg")
        ]

    reference_images = [img for img in reference_images if img is not None]

    if not reference_images:
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
                thread = threading.Thread(
                    target=verify_face,
                    args=(frame_copy, reference_images, result_container),
                    daemon=True
                )
                thread.start()


            counter += 1

            if result_container["face_match"]:
                cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            cv2.imshow("Result", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        capture_object.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()