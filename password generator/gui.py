import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QCheckBox, QSlider, QSpinBox, 
    QFrame, QApplication, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard, QIcon
import pyperclip
from generator import PasswordGenerator
from styles import DARK_THEME

class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generator = PasswordGenerator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Advanced Password Generator")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet(DARK_THEME)

        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card Frame
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(500)
        main_layout.addWidget(card)

        # Card Layout
        layout = QVBoxLayout(card)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel("Password Generator")
        title_label.setObjectName("Title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Password Display
        self.password_display = QLabel("Click Generate")
        self.password_display.setObjectName("PasswordDisplay")
        self.password_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.password_display.setToolTip("Your generated password will appear here")
        layout.addWidget(self.password_display)

        # Strength Indicator
        self.strength_label = QLabel("Strength: N/A")
        self.strength_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.strength_label)

        # Controls Container
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(15)
        layout.addLayout(controls_layout)

        # Length Control
        length_layout = QHBoxLayout()
        length_label = QLabel("Length:")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(4, 64)
        self.length_slider.setValue(12)
        self.length_slider.setToolTip("Slide to adjust password length")
        
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(4, 64)
        self.length_spinbox.setValue(12)
        self.length_spinbox.setToolTip("Enter exact password length")

        # Connect slider and spinbox
        self.length_slider.valueChanged.connect(self.length_spinbox.setValue)
        self.length_spinbox.valueChanged.connect(self.length_slider.setValue)

        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_slider)
        length_layout.addWidget(self.length_spinbox)
        controls_layout.addLayout(length_layout)

        # Options
        self.check_upper = QCheckBox("Uppercase (A-Z)")
        self.check_upper.setChecked(True)
        self.check_upper.setToolTip("Include uppercase letters")
        
        self.check_lower = QCheckBox("Lowercase (a-z)")
        self.check_lower.setChecked(True)
        self.check_lower.setToolTip("Include lowercase letters")
        
        self.check_digits = QCheckBox("Numbers (0-9)")
        self.check_digits.setChecked(True)
        self.check_digits.setToolTip("Include numbers")
        
        self.check_symbols = QCheckBox("Symbols (!@#$)")
        self.check_symbols.setChecked(True)
        self.check_symbols.setToolTip("Include special characters")

        controls_layout.addWidget(self.check_upper)
        controls_layout.addWidget(self.check_lower)
        controls_layout.addWidget(self.check_digits)
        controls_layout.addWidget(self.check_symbols)

        # Exclusion Input
        exclusion_layout = QHBoxLayout()
        exclusion_label = QLabel("Exclude Characters:")
        self.exclusion_input = QLineEdit()
        self.exclusion_input.setPlaceholderText("e.g. l1O0")
        self.exclusion_input.setToolTip("Enter characters you want to exclude from the password")
        
        exclusion_layout.addWidget(exclusion_label)
        exclusion_layout.addWidget(self.exclusion_input)
        controls_layout.addLayout(exclusion_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.clicked.connect(self.generate_password)
        self.generate_btn.setToolTip("Generate a new password based on settings")
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setObjectName("CopyButton")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setToolTip("Copy the current password to clipboard")

        buttons_layout.addWidget(self.generate_btn)
        buttons_layout.addWidget(self.copy_btn)
        
        layout.addLayout(buttons_layout)
        # Removed addStretch since we want the card to be compact
        
        # Initial Generation
        self.generate_password()

    def generate_password(self):
        length = self.length_spinbox.value()
        use_upper = self.check_upper.isChecked()
        use_lower = self.check_lower.isChecked()
        use_digits = self.check_digits.isChecked()
        use_symbols = self.check_symbols.isChecked()
        exclude_chars = self.exclusion_input.text()

        password = self.generator.generate(length, use_upper, use_lower, use_digits, use_symbols, exclude_chars)
        self.password_display.setText(password)

        # Update Strength
        if "Error" not in password:
            strength, color = self.generator.check_strength(password)
            self.strength_label.setText(f"Strength: {strength}")
            self.strength_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        else:
            self.strength_label.setText("Error")
            self.strength_label.setStyleSheet("color: #ff4d4d; font-weight: bold;")

    def copy_to_clipboard(self):
        password = self.password_display.text()
        if "Error" not in password:
            pyperclip.copy(password)
            original_text = self.copy_btn.text()
            self.copy_btn.setText("Copied!")
            # Reset button text after 2 seconds (using QTimer would be better but keeping it simple or just leave it)
            # For a proper GUI, we should use QTimer.
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy to Clipboard"))
