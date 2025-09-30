# demo_runner
import time
from datetime import datetime
from demo_runner.gesture_controller import GestureController
from state_manager import StateManager
from confirmation_system import ConfirmationSystem
from precondition_feedback import PreconditionFeedback
from performance_metrics import PerformanceMetrics

class DemoRunner:
    def __init__(self):
        self.controller = GestureController()
        self.state_manager = StateManager()
        self.confirmation = ConfirmationSystem()
        self.feedback = PreconditionFeedback()
        self.metrics = PerformanceMetrics()
        self.simulated_gestures = [
            ("call_nurse", 0.95),
            ("adjust_volume", 0.88),
            ("toggle_tv", 0.92),
            ("adjust_volume", 0.90),  # TV off — deve falhar
            ("adjust_volume", 0.93),  # TV ligada — deve funcionar
        ]

    def run(self):
        print("🔧 Iniciando modo demonstração...\n")
        for gesture, confidence in self.simulated_gestures:
            start = time.time()
            valid, reason = self.state_manager.validate_action(gesture)

            if not valid:
                self.feedback.show_block_message(None, reason)
                self.metrics.log_failure(gesture, confidence, reason)
            else:
                self.state_manager.update_state(gesture)
                self.confirmation.confirm_action(None, gesture, self.state_manager.states)
                self.metrics.log_success(gesture, confidence, time.time() - start)

            time.sleep(2)  # simula tempo entre gestos

        self.metrics.generate_report()

if __name__ == "__main__":
    demo = DemoRunner()
    demo.run()

# performance_metrics.
from datetime import datetime

class PerformanceMetrics:
    def __init__(self):
        self.success_log = []
        self.failure_log = []

    def log_success(self, gesture, confidence, response_time):
        self.success_log.append((gesture, confidence, response_time))

    def log_failure(self, gesture, confidence, reason):
        self.failure_log.append((gesture, confidence, reason))

    def generate_report(self):
        with open("report.txt", "w") as f:
            f.write("📊 RELATÓRIO DE DESEMPENHO\n")
            f.write(f"Gerado em: {datetime.now()}\n\n")

            f.write("✅ Sucessos:\n")
            for gesture, conf, rt in self.success_log:
                f.write(f"{gesture} - Confiança: {conf:.2f} - Tempo: {rt:.2f}s\n")

            f.write("\n❌ Falhas:\n")
            for gesture, conf, reason in self.failure_log:
                f.write(f"{gesture} - Confiança: {conf:.2f} - Motivo: {reason}\n")

            f.write("\n📈 Taxa de acerto: {:.2f}%\n".format(
                100 * len(self.success_log) / (len(self.success_log) + len(self.failure_log))
            ))
