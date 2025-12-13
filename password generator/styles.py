DARK_THEME = """
QMainWindow {
    border-image: url("background.png") 0 0 0 0 stretch stretch;
}

QFrame#Card {
    background-color: rgba(30, 30, 46, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
}

QLabel {
    color: #cdd6f4;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    background: transparent;
}

QLabel#Title {
    font-size: 28px;
    font-weight: bold;
    color: #89b4fa;
    margin-bottom: 20px;
}

QLabel#PasswordDisplay {
    background-color: rgba(49, 50, 68, 0.6);
    border: 2px solid #45475a;
    border-radius: 12px;
    color: #a6e3a1;
    font-family: 'Consolas', monospace;
    font-size: 20px;
    padding: 15px;
    selection-background-color: #585b70;
}

QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #89b4fa, stop:1 #b4befe);
    color: #1e1e2e;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 15px;
}

QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b4befe, stop:1 #89b4fa);
}

QPushButton:pressed {
    background-color: #74c7ec;
}

QPushButton#CopyButton {
    background-color: rgba(69, 71, 90, 0.8);
    color: #cdd6f4;
    border: 1px solid #585b70;
}

QPushButton#CopyButton:hover {
    background-color: rgba(88, 91, 112, 0.9);
}

QCheckBox {
    color: #cdd6f4;
    font-size: 14px;
    spacing: 10px;
    background: transparent;
}

QCheckBox::indicator {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid #45475a;
    background-color: rgba(49, 50, 68, 0.6);
}

QCheckBox::indicator:checked {
    background-color: #89b4fa;
    border-color: #89b4fa;
    /* Removed complex SVG to avoid parsing errors */
}

QSlider::groove:horizontal {
    border: 1px solid #45475a;
    height: 8px;
    background: rgba(49, 50, 68, 0.6);
    margin: 2px 0;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #89b4fa;
    border: 1px solid #89b4fa;
    width: 20px;
    height: 20px;
    margin: -7px 0;
    border-radius: 10px;
}

QSpinBox {
    background-color: rgba(49, 50, 68, 0.6);
    border: 2px solid #45475a;
    border-radius: 8px;
    color: #cdd6f4;
    padding: 6px;
    font-size: 14px;
}

QLineEdit {
    background-color: rgba(49, 50, 68, 0.6);
    border: 2px solid #45475a;
    border-radius: 8px;
    color: #cdd6f4;
    padding: 6px;
    font-size: 14px;
}
"""
