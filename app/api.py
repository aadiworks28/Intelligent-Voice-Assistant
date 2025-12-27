import sys
import threading
from fastapi import FastAPI
from pydantic import BaseModel
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QObject, pyqtSignal

class StateBus(QObject):
    state_changed = pyqtSignal(str)

state_bus = StateBus()

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.label = QLabel("Zara is idle", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
            color: white;
            font-size: 18px;
            background-color: rgba(0,0,0,180);
            padding: 14px 24px;
            border-radius: 28px;
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.resize(320, 56)
        self.move(40, 40)

        state_bus.state_changed.connect(self.set_state)

    def set_state(self, state: str):
        mapping = {
            "idle": "Zara is idle",
            "listening": "Zara is listening",
            "thinking": "Zara is thinking",
            "speaking": "Zara is speaking"
        }
        self.label.setText(mapping.get(state, "Zara"))

app = FastAPI()

class State(BaseModel):
    state: str

@app.post("/state")
def update_state(s: State):
    state_bus.state_changed.emit(s.state)
    return {"ok": True}

def start_api():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888, log_level="warning")

if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    threading.Thread(target=start_api, daemon=True).start()
    sys.exit(qt_app.exec())

