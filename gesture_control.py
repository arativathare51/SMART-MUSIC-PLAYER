#gesture_control.py
import cv2 #importing opencv library for video capture and image processing
import mediapipe as mp#to detect hand,faces, poses very easily
import time  # to track time and control cooldown between gestures 
from music_controller import pause, play_next, play_previous, is_paused
from gui import update_play_count

class GestureController:
    def __init__(self):# constructor
        self.cap = cv2.VideoCapture(0) #starts the webcam
        self.mp_hands = mp.solutions.hands #loads hand detection solution
        self.hands = self.mp_hands.Hands( #sets how hands are detected
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5 
        )
        self.last_gesture_time = 0 #to remember when last gesture was processed
        self.cooldown = 1.0  # Minimum 1 second gap between two actions

    #function to count fingers
    def count_fingers(self, landmarks):
        #takes hand landmarks( detected points on hand)
        fingers = 0
        # Check fingers (excluding thumb for better reliability)
        for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:  # Index to Pinky
            if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
                fingers += 1
        return fingers

    def run(self): #main loop of the program
        while self.cap.isOpened():  #while camera is on 
            ret, frame = self.cap.read()  
            if not ret:
                break

            frame = cv2.flip(frame, 1) #flips the image so that your left is left, not reversed 
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts bgr to rgb format just what mediapipe needs
            #detect hand
            results = self.hands.process(rgb_frame) #send the frame to mediapipe
            current_time = time.time()  # get current time

            if results.multi_hand_landmarks: #if hand is detected
                hand = results.multi_hand_landmarks[0] #picks the first hand detected
                fingers = self.count_fingers(hand)#counts how many finngers are up

                # Time-based cooldown check instead of frame count
                if (current_time - self.last_gesture_time) > self.cooldown:
                    if fingers == 0:  # Fist
                        pause()  #apuses /resumes accordingly
                        update_play_count()
                        self.last_gesture_time = current_time
                    elif fingers == 2:  # Two fingers
                        play_next()
                        update_play_count()
                        self.last_gesture_time = current_time
                    elif fingers == 1:  # One finger
                        play_previous()
                        update_play_count()
                        self.last_gesture_time = current_time

                # Draw hand landmarks
                #draws dots and lines showing hand skeleton on screen
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand, self.mp_hands.HAND_CONNECTIONS)

            # Display instructions on screen 
            cv2.putText(frame, "FIST: Pause/Resume", (10, 30), #location to start writing
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)#font, font height, colour, thickness of text
            cv2.putText(frame, "TWO FINGERS: Next", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "ONE FINGER: Previous", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            #show the video
            cv2.imshow('Gesture Control (ESC to quit)', frame)#show modified frame on window
            if cv2.waitKey(10) & 0xFF == 27:#press esc to exit 
                break

        self.cap.release()#release webcam
        cv2.destroyAllWindows()#close the window  safely

if __name__ == "__main__":   #if you want to run only gesture_control.py
    GestureController().run()

'''
this code uses the webcam to detetct hand gestures and controls the music by caling functions like play_next()
pause() play_previous()
'''
