import sys
import numpy as np
import cv2
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QImage
import pyautogui
import keyboard


class ColorDetectionThread(QtCore.QThread):
    color_detected = QtCore.Signal(bool, bool)

    def __init__(self, label, command, parent=None):
        super().__init__(parent)
        self.label = label
        self.command = command

    def run(self):
        while True:
            if not self.label.active:
                self.color_detected.emit(False, self.label.active)
            elif self.detect_color():
                self.color_detected.emit(True, self.label.active)
                pyautogui.press(self.command)
            else:
                self.color_detected.emit(False, self.label.active)
            self.msleep(1)

    def detect_color(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, self.label.x() + 8, self.label.y() + 8, self.label.width() - 13,
                                       self.label.height() - 13)
        q_img = screenshot.toImage()
        q_img = q_img.convertToFormat(QImage.Format_RGB32)

        width = q_img.width()
        height = q_img.height()
        ptr = q_img.bits()
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
        img = cv2.cvtColor(arr, cv2.COLOR_RGBA2RGB)

        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower, upper = self.label.color_range
        mask = cv2.inRange(hsv_img, lower, upper)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        return np.any(mask)


class DraggableLabel(QtWidgets.QLabel):
    def __init__(self, color_name, color_rgb, color_range, parent=None):
        super().__init__(parent)
        self.color_name = color_name
        self.color_range = color_range
        self.original_color_rgb = color_rgb
        self.setStyleSheet(f"border: 5px solid {color_rgb};")
        self.setFixedSize(30, 60)
        self.active = True
        self.drag_start_position = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_start_position = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.MouseButton.LeftButton and self.drag_start_position is not None:
            move_position = event.position().toPoint() - self.drag_start_position
            self.move(self.pos() + move_position)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.drag_start_position is not None:
            print(f"Label {self.color_name} moved to position: ({self.pos().x()}, {self.pos().y()})")
            self.drag_start_position = None

    def move_to_position(self, pos):
        self.move(pos.x(), pos.y())


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.region_height = 200
        self.initUI()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_labels_position)
        self.timer.start(10)  # Update every 10 ms

    def initUI(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        screen = QtWidgets.QApplication.primaryScreen()
        screen_resolution = screen.size()
        self.setGeometry(0, 0, screen_resolution.width(), screen_resolution.height())

        color_infos = {
            "purple": ("#C24B99", ((150, 116, 154), (170, 196, 234)), 'left'),
            "blue": ("#00FFFF", ((80, 215, 215), (100, 255, 255)), 'down'),
            "green": ("#12FA05", ((48, 210, 210), (68, 255, 255)), 'up'),
            "red": ("#F9393F", ((169, 157, 209), (179, 237, 255)), 'right'),
        }

        positions_left = [(273, self.region_height), (562, self.region_height), (856, self.region_height), (1141, self.region_height)]

        self.labels = []
        self.threads = []
        for color_name, (color_rgb, color_range, command), pos in zip(color_infos.keys(), color_infos.values(), positions_left):
            label = DraggableLabel(color_name, color_rgb, color_range, self)
            label.move(*pos)
            self.labels.append(label)
            thread = ColorDetectionThread(label, command)
            thread.color_detected.connect(lambda detected, active, l=label: l.setStyleSheet(
                "border: 5px solid black;" if not active else (
                    "border: 5px solid white;" if detected else f"border: 5px solid {l.original_color_rgb};")))
            thread.start()
            self.threads.append(thread)

        self.toggle_button = QtWidgets.QPushButton("Toggle Activación", self)
        self.toggle_button.clicked.connect(self.toggle_activation)
        self.toggle_button.setGeometry(round(screen_resolution.width() / 2) - 70, 70, 150, 30)

        keyboard.add_hotkey('1', lambda: self.update_color(0))
        keyboard.add_hotkey('2', lambda: self.update_color(1))
        keyboard.add_hotkey('3', lambda: self.update_color(2))
        keyboard.add_hotkey('4', lambda: self.update_color(3))

        self.show()

    def update_labels_position(self):
        if keyboard.is_pressed('shift+1'):
            self.move_label_to_cursor(0)
        if keyboard.is_pressed('shift+2'):
            self.move_label_to_cursor(1)
        if keyboard.is_pressed('shift+3'):
            self.move_label_to_cursor(2)
        if keyboard.is_pressed('shift+4'):
            self.move_label_to_cursor(3)

    def move_label_to_cursor(self, label_index):
        x, y = pyautogui.position()
        self.labels[label_index].move_to_position(QtCore.QPoint(x, y))

    def update_color(self, label_index):
        color = self.get_color_under_mouse()
        if color is not None:
            hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)[0][0]
            lower_bound = np.array([hsv_color[0] - 10, 100, 100])
            upper_bound = np.array([hsv_color[0] + 10, 255, 255])
            self.labels[label_index].color_range = (lower_bound, upper_bound)
            self.labels[label_index].original_color_rgb = f"rgb({color[2]}, {color[1]}, {color[0]})"
            self.labels[label_index].setStyleSheet(f"border: 5px solid {self.labels[label_index].original_color_rgb};")

    def get_color_under_mouse(self):
        x, y = pyautogui.position()
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, x, y, 1, 1)
        q_img = screenshot.toImage()
        q_img = q_img.convertToFormat(QImage.Format_RGB32)
        ptr = q_img.bits()
        arr = np.frombuffer(ptr, np.uint8).reshape((1, 1, 4))
        b, g, r, a = arr[0, 0]
        return (b, g, r)

    def toggle_activation(self):
        for label in self.labels:
            label.active = not label.active

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        for thread in self.threads:
            thread.terminate()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open("styles.qss", "r").read())
    trans_window = TransparentWindow()
    sys.exit(app.exec())
