import threading
import cv2
import os
from deepface import DeepFace
import numpy as np 
import mediapipe as mp

DeepFace.build_model("VGG-Face")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
mp_face_mesh = mp.solutions.face_mesh

def detect_and_crop_face(image):
    """
    Aligns the face, then detects and crops it
    """

    aligned_image = align_face_mediapipe(image)
    if aligned_image is None:
        return None

    gray = cv2.cvtColor(aligned_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None
    
    x, y, w, h = sorted(faces, key=lambda box: box[2]*box[3], reverse=True)[0]
    return image[y:y+h, x:x+w]


def align_face_mediapipe(image):
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return None
        
        landmarks = results.multi_face_landmarks[0]

        ih, iw, _ = image.shape
        left_eye = landmarks.landmark[33]
        right_eye = landmarks.landmark[263]

        left = np.array([left_eye.x * iw, left_eye.y * ih])
        right = np.array([right_eye.x * iw, right_eye.y * ih])

        delta = right - left
        angle = np.degrees(np.arctan2(delta[1], delta[0]))

        center_x = int((left[0] + right[0]) / 2)
        center_y = int((left[1] + right[1]) / 2)
        center = (center_x, center_y)

        rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        aligned_image = cv2.warpAffine(image, rot_matrix, (iw, ih), flags=cv2.INTER_LINEAR)

        return aligned_image


def verify_face(frame, reference_images, result_container):
    """
    Crops faces and performs DeepFace verification.
    """
    frame_face = detect_and_crop_face(frame)
    if frame_face is None:
        result_container["face_match"] = False
        return

    try:
        for ref_img in reference_images:
            verification = DeepFace.verify(frame_face, ref_img, model_name="VGG-Face")["verified"]
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

    reference_paths = ["reference_image.jpg", "reference_left.jpg", "reference_right.jpg"]
    reference_images = []

    for path in reference_paths:
        img = cv2.imread(path)
        if img is not None:
            cropped = detect_and_crop_face(img)
            if cropped is not None:
                reference_images.append(cropped)

    if not reference_images:
        print("Error: No valid reference faces found.")
        return
    
    result_container = {"face_match": False}
    counter = 0

    try:
        while True:
            ret, frame = capture_object.read()
            if not ret:
                print("Error: Failed to read from webcam.")
                break

            if counter % 30 == 0:
                thread = threading.Thread(
                    target=verify_face,
                    args=(frame.copy(), reference_images, result_container),
                    daemon=True
                )
                thread.start()

            counter += 1

            label = "MATCH" if result_container["face_match"] else "NO MATCH!"
            color = (0, 255, 0) if result_container["face_match"] else (0, 0, 255)
            cv2.putText(frame, label, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        capture_object.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()