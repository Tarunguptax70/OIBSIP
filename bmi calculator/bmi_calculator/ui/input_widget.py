from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QMessageBox, QFormLayout
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPainter, QPixmap
import os

class InputWidget(QWidget):
    calculate_signal = pyqtSignal(float, float) # weight, height
    user_changed_signal = pyqtSignal(int) # user_id
    add_user_signal = pyqtSignal(str) # username

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.background_image = QPixmap(os.path.join(os.path.dirname(__file__), "background.png"))
        self.init_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_image.isNull():
            painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)

    def init_ui(self):
        layout = QVBoxLayout()

        # User Selection
        user_layout = QHBoxLayout()
        self.user_combo = QComboBox()
        self.user_combo.currentIndexChanged.connect(self.on_user_changed)
        self.add_user_btn = QPushButton("Add User")
        self.add_user_btn.clicked.connect(self.add_user)
        user_layout.addWidget(QLabel("User:"))
        user_layout.addWidget(self.user_combo)
        user_layout.addWidget(self.add_user_btn)
        layout.addLayout(user_layout)

        # Input Form
        form_layout = QFormLayout()
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("kg")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("meters")
        
        form_layout.addRow("Weight (kg):", self.weight_input)
        form_layout.addRow("Height (m):", self.height_input)
        layout.addLayout(form_layout)

        # Calculate Button
        self.calc_btn = QPushButton("Calculate BMI")
        self.calc_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calc_btn)

        self.setLayout(layout)
        self.refresh_users()

    def refresh_users(self):
        self.user_combo.blockSignals(True)
        self.user_combo.clear()
        users = self.db_manager.get_users()
        for user_id, name in users:
            self.user_combo.addItem(name, user_id)
        self.user_combo.blockSignals(False)
        
        if self.user_combo.count() > 0:
            self.on_user_changed()

    def add_user(self):
        # In a real app, use QInputDialog, but for simplicity we can use a separate dialog or just a simple input here.
        # For now, let's assume we want to trigger a dialog in the main window or handle it here.
        # Let's use a simple input dialog here for ease.
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Add User", "Enter user name:")
        if ok and name:
            self.add_user_signal.emit(name)

    def on_user_changed(self):
        user_id = self.user_combo.currentData()
        if user_id is not None:
            self.user_changed_signal.emit(user_id)

    def calculate(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            self.calculate_signal.emit(weight, height)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for weight and height.")
