import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFormLayout, QGroupBox, QSpinBox, QScrollArea, QStatusBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from enregy_aware_scheduler import Task, HybridScheduler


class SchedulerWorker(QThread):
    output_signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, scheduler_method, duration):
        super().__init__()
        self.scheduler_method = scheduler_method
        self.duration = duration

    def run(self):
        self.scheduler_method(self.duration, self.output_signal)
        self.finished.emit()


class SchedulerGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the hybrid scheduler instance
        self.scheduler = HybridScheduler()

        # Setup the UI
        self.setWindowTitle("Hybrid Scheduler GUI")
        self.setGeometry(100, 100, 850, 650)
        self.setWindowIcon(QIcon("icons/scheduler.png"))

        # Main layout
        main_layout = QVBoxLayout()

        # Task input group
        task_input_group = self.create_task_input_section()
        main_layout.addWidget(task_input_group)

        # Scheduler control group
        control_group = self.create_scheduler_control_section()
        main_layout.addWidget(control_group)

        # Energy monitoring output
        self.monitor_output = QTextEdit(self)
        self.monitor_output.setReadOnly(True)
        self.monitor_output.setStyleSheet("font-family: Monospace;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.monitor_output)
        main_layout.addWidget(scroll_area)

        # Set central widget and layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Threading
        self.worker_thread = None

        # Apply modern QSS stylesheet
        self.setStyleSheet(self.load_styles())

    def create_task_input_section(self):
        """Create task input form."""
        group_box = QGroupBox("Add Task")
        group_box.setFont(QFont("Arial", 12))
        layout = QFormLayout()

        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")

        self.task_period_input = QSpinBox()
        self.task_execution_time_input = QSpinBox()
        self.task_deadline_input = QSpinBox()

        for widget in [self.task_period_input, self.task_execution_time_input, self.task_deadline_input]:
            widget.setMaximum(100)

        # Create a custom label with white text
        def create_label(text):
            label = QLabel(text)
            label.setStyleSheet("color: white;")  # Set text color to white
            return label

        layout.addRow(create_label("Task Name:"), self.task_name_input)
        layout.addRow(create_label("Task Period (seconds):"), self.task_period_input)
        layout.addRow(create_label("Execution Time (seconds):"), self.task_execution_time_input)
        layout.addRow(create_label("Deadline (seconds):"), self.task_deadline_input)

        add_task_btn = QPushButton("Add Task")
        add_task_btn.setIcon(QIcon("icons/add.png"))
        add_task_btn.clicked.connect(self.add_task)
        layout.addWidget(add_task_btn)

        group_box.setLayout(layout)
        return group_box

    def create_scheduler_control_section(self):
        """Create control section with buttons."""
        group_box = QGroupBox("Scheduler Controls")
        group_box.setFont(QFont("Arial", 12))
        layout = QVBoxLayout()

        button_style = "padding: 10px; font-size: 14px; margin: 5px;"

        def add_button(text, callback):
            btn = QPushButton(text)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        add_button("Run Round Robin", self.run_round_robin)
        add_button("Run Priority-Based", self.run_priority)
        add_button("Run RMS", self.run_rms)
        add_button("Run EDF", self.run_edf)
        add_button("Run Hybrid", self.run_hybrid)
        add_button("Compare Algorithms", self.compare_algorithms)

        group_box.setLayout(layout)
        return group_box

    def add_task(self):
        """Add a task to the scheduler."""
        task_name = self.task_name_input.text()
        period = self.task_period_input.value()
        execution_time = self.task_execution_time_input.value()
        deadline = self.task_deadline_input.value()

        if task_name:
            task = Task(name=task_name, period=period, execution_time=execution_time, deadline=deadline)
            self.scheduler.add_task(task)
            self.monitor_output.append(f"<b>Task added:</b> {task_name}")
            self.status_bar.showMessage(f"Task '{task_name}' added successfully.", 3000)
        else:
            self.monitor_output.append("<b style='color: red;'>Please enter a task name.</b>")
            self.status_bar.showMessage("Task name is required.", 3000)

    def run_scheduler_in_thread(self, scheduler_method, duration):
        """Run the scheduler in a thread."""
        if self.worker_thread:
            self.worker_thread.quit()

        self.worker_thread = SchedulerWorker(scheduler_method, duration)
        self.worker_thread.output_signal.connect(self.update_output)
        self.worker_thread.start()

    def update_output(self, message):
        """Update output display."""
        self.monitor_output.append(message)

    def run_round_robin(self):
        self.monitor_output.append("<b>Running Round Robin...</b>")
        self.run_scheduler_in_thread(self.scheduler.run_round_robin, 10)

    def run_priority(self):
        self.monitor_output.append("<b>Running Priority-Based...</b>")
        self.run_scheduler_in_thread(self.scheduler.run_priority_based, 10)

    def run_rms(self):
        self.monitor_output.append("<b>Running RMS...</b>")
        self.run_scheduler_in_thread(self.scheduler.run_rms, 10)

    def run_edf(self):
        self.monitor_output.append("<b>Running EDF...</b>")
        self.run_scheduler_in_thread(self.scheduler.run_edf, 10)

    def run_hybrid(self):
        self.monitor_output.append("<b>Running Hybrid...</b>")
        self.run_scheduler_in_thread(self.scheduler.run_hybrid, 10)

    def compare_algorithms(self):
        self.monitor_output.append("<b>Comparing algorithms...</b>")
        self.run_scheduler_in_thread(self.scheduler.compare_algorithms, 10)

    def load_styles(self):
        """Load QSS stylesheet."""
        return """
            QMainWindow {
                background-color: #232629;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #3a3f44;
                color: white;
                border-radius: 8px;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #50565b;
            }
            QTextEdit {
                background-color: #2b2b2b;
                color: #dcdcdc;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: #1c1c1c;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #f0f0f0;
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Apply Fusion style for a modern look
    gui = SchedulerGUI()
    gui.show()
    sys.exit(app.exec_())
