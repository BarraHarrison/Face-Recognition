# Facial Recognition using DeepFace 🎭🔍

## Introduction
Welcome to the Facial Recognition using DeepFace project! 🧑‍💻 This project dives into the world of facial recognition technology, leveraging the power of the DeepFace library to perform real-time face verification.

## The verify_face Function 🧐
The *verify_face* function is the heart of the facial recognition logic. Here's what it does:

- **Functionality**: It takes a frame from the video feed, a reference image, and a result container as inputs. Using the DeepFace library, it compares the face in the frame with the face in the reference image to verify if they match.

- **Implementation**: It's designed to run in a separate thread every 30 frames to ensure smooth real-time operation without slowing down the video feed. If there's no face detected or if the comparison fails, it safely sets the result to False to avoid errors.

## The main Function 🎬
The *main* function orchestrates the entire process:

- **Initialization**: It sets up the video capture, loads the reference image, and initializes variables for tracking results.

- **Main Loop**: Runs in a continuous loop, capturing frames from the camera. Every 30 frames, it triggers the verify_face function in a separate thread for performance efficiency.

- **Display**: Based on the verification result, it overlays "MATCH!" in green or "NO MATCH!" in red on the video feed, providing real-time feedback to the user.

- **Exit**: The loop breaks when the user presses 'q', ensuring a graceful shutdown by releasing the camera and closing all OpenCV windows.

## DeepFace Import and Its Role 🌐

- **Import**: *from deepface import DeepFace* brings the powerful DeepFace library into our project.

- **Role**: DeepFace is crucial for this project as it provides pre-trained models for facial recognition, specifically the VGG-Face model which I used for our verification process. It simplifies the complex task of facial recognition by abstracting away the deep learning intricacies, allowing us to focus on application logic.

## Difficulties with DeepFace Dependency 📥
One of the significant challenges I encountered was related to the DeepFace dependency, particularly with downloading the *vgg_face_weights.h5* file:

- **Download Issues**: Initially, the automatic download process for the model weights failed multiple times, likely due to network issues or permissions. This caused repeated attempts to download the file, which I observed in the terminal output.

- **Solution**: I resolved this by manually downloading the weights file and placing it in the project directory, ensuring the script could find and load it properly. This workaround was necessary since DeepFace didn't accept custom paths for the weights directly in the function call at the time.

## End Results 📈

- **Recognizes Faces**: When I looked directly into the camera, the system recognized my face and displayed "MATCH!" in green, confirming a successful verification.

- **Handles Profile Views**: However, when I turned my head to the side, the system couldn't match my profile view, which is typical for many face recognition models trained primarily on frontal images. This provides an avenue for future enhancement.

-- **Testing Images**: In the *face_recognition_results* directory, testing images from one up until four were when the program did not function correctly. Testing images from five to seven are examples of how the program was able to recognize and unrecognize my face based on the reference_image.jpg.

## Conclusion 🎉
I learned not just about implementing AI in practical applications but also about managing dependencies, handling real-time data, and dealing with the nuances of model performance. While our system works well for direct face recognition, there's room for growth, especially in improving profile recognition.