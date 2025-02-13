# Python Program for Face Recognition
import threading
import cv2
from deepface import DeepFace

capture_object = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False

reference_image = cv2.imread("reference_image.jpg")

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify([frame, reference_image.copy()]):
            pass
    except ValueError:
        pass

while True:
    ret, frame = capture_object.read()
    
    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        
        counter += 1

        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("Result", frame)
    
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()