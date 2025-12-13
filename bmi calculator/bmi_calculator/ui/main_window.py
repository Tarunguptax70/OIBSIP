from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMessageBox
from .input_widget import InputWidget
from .history_widget import HistoryWidget
from ..database import DatabaseManager
from ..logic import BMILogic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setGeometry(100, 100, 800, 600)

        self.db_manager = DatabaseManager()
        
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Input Tab
        self.input_widget = InputWidget(self.db_manager)
        self.input_widget.calculate_signal.connect(self.calculate_bmi)
        self.input_widget.user_changed_signal.connect(self.load_history)
        self.input_widget.add_user_signal.connect(self.add_user)
        self.tabs.addTab(self.input_widget, "Calculator")

        # History Tab
        self.history_widget = HistoryWidget()
        self.history_widget.clear_btn.clicked.connect(self.clear_history)
        self.tabs.addTab(self.history_widget, "History & Trends")
        
        # Trigger initial load if users exist
        if self.input_widget.user_combo.count() > 0:
            self.input_widget.on_user_changed()

    def add_user(self, name):
        user_id = self.db_manager.add_user(name)
        if user_id:
            QMessageBox.information(self, "Success", f"User '{name}' added successfully!")
            self.input_widget.refresh_users()
        else:
            QMessageBox.warning(self, "Error", f"User '{name}' already exists!")

    def calculate_bmi(self, weight, height):
        try:
            bmi = BMILogic.calculate_bmi(weight, height)
            category = BMILogic.get_category(bmi)
            
            user_id = self.input_widget.user_combo.currentData()
            if user_id is None:
                QMessageBox.warning(self, "Error", "Please select or add a user first.")
                return

            # Save record
            self.db_manager.add_record(user_id, weight, height, bmi)
            
            # Show result
            QMessageBox.information(self, "BMI Result", f"Your BMI is {bmi:.2f}\nCategory: {category}")
            
            # Refresh history
            self.load_history(user_id)
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def load_history(self, user_id):
        records = self.db_manager.get_records(user_id)
        self.history_widget.update_data(records)

    def clear_history(self):
        user_id = self.input_widget.user_combo.currentData()
        if user_id is None:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete', 
            "Are you sure you want to clear all history for this user?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_records(user_id)
            self.load_history(user_id)
            QMessageBox.information(self, "Success", "History cleared successfully.")
