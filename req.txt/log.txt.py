# Log de reconhecimentos
from datetime import datetime

def log_gesture(gesture_name, confidence):
    with open("logs/gesture_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {gesture_name} - Confiança: {confidence:.2f}\n")
