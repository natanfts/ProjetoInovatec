import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from datetime import datetime
import pygame

print("Tudo pronto para começar!")

              #Fase1 configuração inicial, captura básica de vídeo.
import cv2

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Captura de Vídeo", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        break
cap.release()
cv2.destroyAllWindows()

              #Fase1.2 testar detecção de mãos com mediapipe
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Detecção de Mãos", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
             #Fase1.3 Ponto de entrada do projeto. Captura vídeo e chama o detector.
import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from gesture_detector import GestureDetector

def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(3, FRAME_WIDTH)
    cap.set(4, FRAME_HEIGHT)

    detector = GestureDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = detector.detect(frame)
        cv2.imshow("Detecção de Mãos", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    
cv2.putText(frame, "Gesto: Mão Aberta", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

# state_manager.py
from datetime import datetime

class StateManager:
    def __init__(self):
        self.states = {
            "tv_on": False,
            "volume": 10,
            "last_action": None,
            "last_timestamp": None
        }
        self.history = []

    def can_perform(self, action):
        if action == "increase_volume" and not self.states["tv_on"]:
            return False, "TV precisa estar ligada para ajustar volume"
        return True, ""

    def update_state(self, action):
        now = datetime.now()
        if self.states["last_action"] == action and (now - self.states["last_timestamp"]).total_seconds() < 2:
            return False  # debounce: ignora repetições em menos de 2s

        self.states["last_action"] = action
        self.states["last_timestamp"] = now
        self.history.append((now, action))
        return True
def draw_panel(frame, state_manager):
    status = f"TV: {'Ligada' if state_manager.states['tv_on'] else 'Desligada'} | Volume: {state_manager.states['volume']}"
    cv2.putText(frame, status, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    
can_do, reason = state_manager.can_perform("increase_volume")
if not can_do:
    cv2.putText(frame, reason, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
else:
    if state_manager.update_state("increase_volume"):
        state_manager.states["volume"] += 1

def export_history(state_manager):
    with open("logs/action_history.txt", "w") as f:
        for timestamp, action in state_manager.history:
            f.write(f"{timestamp} - {action}\n")
            
# Fase 4 texto na tela com nome do gesto
cv2.putText(frame, "Gesto: Mão Aberta", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#- Cor de fundo ou borda alterada por gesto
#- Verde para gesto válido
#- Vermelho para gesto inválido ou fora de contexto
#- Ícones ou imagens sobrepostos
#- Exibir ícones como 🔊 para volume, 🖱️ para clique, etc.
#- Use cv2.imread() para carregar imagens da pasta assets/images/
#- Barra de confiança
#- Exibir uma barra que representa a confiança do reconhecimento (0–100%)

cv2.rectangle(frame, (10, 60), (10 + int(confidence * 200), 80), (0,255,0), -1)
# Painel de controle virtual
# Já iniciado na Fase 3, pode ser expandido com botões simulados, estados e ícones

import pygame
pygame.mixer.init()
pygame.mixer.Sound("assets/sounds/confirm.wav").play()
#🔊 Elementos de Feedback Sonoro
# Sons de confirmação
# Som curto ao reconhecer gesto válido
# Som de erro ao rejeitar gesto ou violar pré-condição
# Voz sintetizada (opcional)
# Pode usar pyttsx3 para dizer “Volume aumentado” ou “TV desligada”
# Integração com pygame.mixer

# feedback_system.py
import pygame
import cv2

class FeedbackSystem:
    def __init__(self):
        pygame.mixer.init()

    def visual_feedback(self, frame, gesture_name, confidence):
        cv2.putText(frame, f"{gesture_name} ({confidence:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        return frame

    def sound_feedback(self, gesture_name):
        sound_map = {
            "open_hand": "confirm.wav",
            "fist": "click.wav",
            "invalid": "error.wav"
        }
        sound_file = sound_map.get(gesture_name, "default.wav")
        pygame.mixer.Sound(f"assets/sounds/{sound_file}").play()
        
#Fase 4.1 Feedback visual expandido
       
#Gesto detectado: Mão Aberta        
cv2.putText(frame, f"Gesto: {gesture_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#Ação correspondente: Aumentar Volume
cv2.putText(frame, f"Ação: {action_name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
#Status atual do sistema
cv2.putText(frame, f"TV: {'Ligada' if state['tv_on'] else 'Desligada'} | Volume: {state['volume']}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200,200,200), 2)
#Barra de confiança  
cv2.putText(frame, f"Confiança: {confidence:.2f}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,150,255), 2)
cv2.rectangle(frame, (10, 140), (10 + int(confidence * 200), 160), (0,150,255), -1)
#Status dos dispositivos virtuais
cv2.putText(frame, "Dispositivos:", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
cv2.putText(frame, f"TV: {'Ligada' if state['tv_on'] else 'Desligada'}", (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)
cv2.putText(frame, f"Luzes: {'Ativas' if state['lights_on'] else 'Inativas'}", (500, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)
#Histórico de ações recentes
for i, (timestamp, action) in enumerate(state_manager.history[-5:]):
    cv2.putText(frame, f"{timestamp.strftime('%H:%M:%S')} - {action}", (500, 100 + i*20), cv2.FONT_HERSHEY_PLAIN, 1, (200,200,200), 1)
#Indicadores de pré-condição
if not state['tv_on']:
    cv2.putText(frame, "⚠ TV desligada - Volume bloqueado", (500, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
#Animações sutis / pulsar ao detectar gesto
if gesture_detected:
    radius = int(10 + 5 * math.sin(time.time() * 5))
    cv2.circle(frame, (600, 300), radius, (0,255,255), -1)

#Fase 4.2 sistema de confirmação
# confirmation_system.py
import cv2
import pygame

class ConfirmationSystem:
    def __init__(self):
        pygame.mixer.init()
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def show_message(self, frame, message, color=(0, 255, 0)):
        cv2.putText(frame, message, (50, 250), self.font, 1.2, color, 3)
        return frame

    def play_sound(self, sound_file):
        pygame.mixer.Sound(f"assets/sounds/{sound_file}").play()

    def confirm_action(self, frame, gesture_name, state):
        if gesture_name == "call_nurse":
            msg = "ENFERMEIRO CHAMADO! - Aguarde assistência"
            sound = "alert.wav"
        elif gesture_name == "toggle_tv":
            status = "Ligando" if not state["tv_on"] else "Desligando"
            msg = f"ALTERANDO ESTADO DA TV - {status}"
            sound = "tv_toggle.wav"
        elif gesture_name == "adjust_volume":
            msg = f"VOLUME AJUSTADO - Novo nível: {state['volume']}%"
            sound = "volume.wav"
        else:
            msg = "Ação reconhecida"
            sound = "default.wav"

        frame = self.show_message(frame, msg)
        self.play_sound(sound)
        return frame
    
    #após detectar gesto e validar ação
    frame = confirmation_system.confirm_action(frame, gesture_name, state_manager.states)
# Mensagem aparece no centro da tela por 2 segundos
# Som correspondente é reproduzido

#Fase 4.3 Validação de pré-condições
#Objetivo: Evitar ações inválidas ou fora de contexto, e fornecer feedback claro.

#Adicione uma função para verificar pré-condições antes de executar uma ação
def validate_action(self, action):
    now = datetime.now()
    if self.states["last_action"] == action and (now - self.states["last_timestamp"]).total_seconds() < 2:
        return False, "AGUARDE - Ação anterior ainda em processamento"

    if action == "adjust_volume" and not self.states["tv_on"]:
        return False, "TV DESLIGADA - Ligue a TV primeiro para ajustar volume"

    return True, ""
# precondition_feedback.py
import cv2
import pygame

class PreconditionFeedback:
    def __init__(self):
        pygame.mixer.init()

    def show_block_message(self, frame, message):
        cv2.putText(frame, message, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        pygame.mixer.Sound("assets/sounds/error.wav").play()
        return frame
#Antes de executar qualquer ação:
valid, reason = state_manager.validate_action("adjust_volume")
if not valid:
    frame = precondition_feedback.show_block_message(frame, reason)
    continue  # pula execução da ação

#Fase 5 - Métricas de Desempenho
#módulo performance_metrics.py / taxa de acerto por gesto
def accuracy_per_gesture(true_labels, predicted_labels):
    from collections import Counter
    correct = Counter()
    total = Counter()
    for t, p in zip(true_labels, predicted_labels):
        total[t] += 1
        if t == p:
            correct[t] += 1
    return {g: correct[g] / total[g] for g in total}
#- Use time.time() para medir intervalo entre gesto detectado e feedback exibido
#- Teste com:
#- Iluminação baixa
#- Fundo movimentado
#- Mão parcialmente visível
#- Registre taxa de erro e confiança média

#modo desmontração automática
if args.demo:
    run_demo_sequence()

      

# Relatório Final
#Gere um report.txt com:
# Lista de gestos testados
# Taxa de acerto por gesto
# Média de tempo de resposta
# Observações sobre estabilidade
