# testes para funções com dados reais ou simulados para validar

def calculate_accuracy(true_labels, predicted_labels):
    correct = sum(t == p for t, p in zip(true_labels, predicted_labels))
    return correct / len(true_labels)

def confusion_matrix(true_labels, predicted_labels, gesture_names):
    # Gera matriz de confusão para análise
def gesture_confidence(landmarks):
    # Exemplo: distância entre ponta do dedo e base
    return 1.0 - abs(landmarks[8].y - landmarks[5].y)
