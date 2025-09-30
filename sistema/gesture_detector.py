#Responsável por inicializar o MediaPipe e detectar mãos.

import cv2
import mediapipe as mp
from config import MEDIAPIPE_HANDS_CONFIG

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

class GestureDetector:
    def __init__(self):
        self.hands = mp_hands.Hands(**MEDIAPIPE_HANDS_CONFIG)

    def detect(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        return frame

#Função para cada gesto

def is_open_hand(landmarks):
    # Verifica se todos os dedos estão estendidos
    return all(landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20])  # pontas dos dedos

def is_fist(landmarks):
    # Verifica se todos os dedos estão dobrados
    return all(landmarks[i].y > landmarks[i - 2].y for i in [8, 12, 16, 20])
