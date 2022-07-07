import cv2
import numpy as np

class MediapipeLandmark:
    import mediapipe as mp
    def __init__(self,max_num_hands=2,model_complexity=1,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.hands=self.mp.solutions.hands.Hands(False,max_num_hands,model_complexity,min_detection_confidence,min_tracking_confidence)
        
    def Coordinates(self,frame):
        val=int()
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks!=None:
            for hand in results.multi_hand_landmarks:
                val=int(hand.landmark[8].x*1366)
        return abs(val)
