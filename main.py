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


