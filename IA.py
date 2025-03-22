import sys
import time
import keyboard
import pyautogui
from PySide6 import QtWidgets, QtCore


class KeyPresserApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Key Presser')
        self.setGeometry(100, 100, 300, 100)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.label = QtWidgets.QLabel("Presiona Ctrl+Shift+L para seleccionar la aplicación")
        layout.addWidget(self.label)

        # Inicializar variables
        self.target_window = None
        self.key_to_press = 'k'  # Puedes cambiar esta tecla según tu preferencia
        self.key_pressed = False

        # Configurar el timer para verificar la ventana en foco
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_focus)
        self.timer.start(100)  # Verificar cada 100ms

        # Configurar atajos de teclado
        keyboard.add_hotkey('ctrl+shift+l', self.select_application)
        keyboard.add_hotkey('ctrl+shift+k', self.toggle_key_press)

    def select_application(self):
        # Obtener la ventana en foco
        self.target_window = pyautogui.getActiveWindow()
        if self.target_window:
            self.label.setText(f'Aplicación seleccionada: {self.target_window.title}')

    def toggle_key_press(self):
        if self.target_window and self.key_to_press:
            if self.key_pressed:
                keyboard.release(self.key_to_press)
                self.key_pressed = False
                self.label.setText(f'Tecla {self.key_to_press} liberada')
            else:
                keyboard.press(self.key_to_press)
                self.key_pressed = True
                self.label.setText(f'Tecla {self.key_to_press} presionada')

    def check_focus(self):
        # Verificar si la ventana en foco es la ventana objetivo
        active_window = pyautogui.getActiveWindow()
        if active_window != self.target_window:
            if self.key_pressed:
                keyboard.release(self.key_to_press)
                self.key_pressed = False
            self.label.setText('Focus fuera de la aplicación seleccionada')

    def closeEvent(self, event):
        keyboard.unhook_all_hotkeys()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = KeyPresserApp()
    window.show()
    sys.exit(app.exec())
