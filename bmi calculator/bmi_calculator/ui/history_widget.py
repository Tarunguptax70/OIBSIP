from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtGui import QPainter, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import datetime
import os

class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.background_image = QPixmap(os.path.join(os.path.dirname(__file__), "history_background.png"))
        self.init_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_image.isNull():
            painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)

    def init_ui(self):
        layout = QVBoxLayout()

        # Graph
        self.figure = Figure()
        self.figure.patch.set_alpha(0.0) # Transparent figure background
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")
        layout.addWidget(self.canvas)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Weight", "Height", "BMI"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Make table transparent
        self.table.setStyleSheet("background-color: rgba(30, 30, 30, 150); color: #E0E0E0; gridline-color: #555;")
        layout.addWidget(self.table)

        # Clear Data Button
        from PyQt6.QtWidgets import QPushButton
        self.clear_btn = QPushButton("Clear History")
        self.clear_btn.setStyleSheet("background-color: #CF6679; color: black;") # Reddish for danger
        layout.addWidget(self.clear_btn)

        self.setLayout(layout)

    def update_data(self, records):
        # Update Table
        self.table.setRowCount(len(records))
        dates = []
        bmis = []

        for i, (weight, height, bmi, date_str) in enumerate(records):
            # Parse date
            try:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                 # Fallback for different formats if needed, or just use current time if parsing fails (shouldn't happen with sqlite default)
                date_obj = datetime.datetime.now()

            self.table.setItem(i, 0, QTableWidgetItem(date_str))
            self.table.setItem(i, 1, QTableWidgetItem(str(weight)))
            self.table.setItem(i, 2, QTableWidgetItem(str(height)))
            self.table.setItem(i, 3, QTableWidgetItem(f"{bmi:.2f}"))
            
            dates.append(date_obj)
            bmis.append(bmi)

        # Update Graph
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Set figure background color to match UI (Dark) but semi-transparent
        self.figure.patch.set_facecolor('none') # Transparent
        ax.set_facecolor('none') # Transparent axis background to see image? Or maybe semi-transparent dark?
        # Let's try semi-transparent dark for readability
        ax.set_facecolor((0.07, 0.07, 0.07, 0.7)) # RGBA tuple for dark background with alpha

        if dates:
            # Plot with neon line and markers
            # Neon Pink line, Neon Cyan markers
            line, = ax.plot(dates, bmis, marker='o', linestyle='-', linewidth=2, markersize=8)
            line.set_color('#CF6679') # Neon/Pastel Red-Pink
            line.set_markerfacecolor('#03DAC6') # Neon Teal
            line.set_markeredgecolor('#018786')
            
            ax.set_title("BMI Trend", color='#E0E0E0', fontsize=12, fontweight='bold')
            ax.set_xlabel("Date", color='#BBBBBB')
            ax.set_ylabel("BMI", color='#BBBBBB')
            
            # Style ticks
            ax.tick_params(axis='x', colors='#BBBBBB')
            ax.tick_params(axis='y', colors='#BBBBBB')
            
            # Style spines
            ax.spines['bottom'].set_color('#333333')
            ax.spines['top'].set_color('#333333')
            ax.spines['left'].set_color('#333333')
            ax.spines['right'].set_color('#333333')

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            self.figure.autofmt_xdate()
            ax.grid(True, color='#333333', linestyle='--')
        
        self.canvas.draw()
