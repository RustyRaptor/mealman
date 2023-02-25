import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QProgressBar, QTableWidget, QTableWidgetItem
import subprocess

from PyQt5.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Calorie Counter"
        self.left = 100
        self.top = 100
        self.width = int(1280 * 0.7)
        self.height = int(720 * 0.7)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # File picker button
        self.file_picker_button = QPushButton("Choose Meal Plan File", self)
        self.file_picker_button.move(20, 50)
        self.file_picker_button.resize(200,20)
        self.file_picker_button.clicked.connect(self.choose_file)

        # File path label
        self.file_path_label = QLabel("No file chosen.", self)
        self.file_path_label.move(160, 25)
        self.file_path_label.resize(400,20)

        # Submit button
        self.button = QPushButton("Submit", self)
        self.button.move(160, 100)
        self.button.clicked.connect(self.submit)

        # Status label
        self.status_label = QLabel("", self)
        self.status_label.move(20, 150)
        self.status_label.resize(360, 20)

        # Status progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.move(20, 175)
        self.progress_bar.resize(360, 20)

    def choose_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Meal Plan File", "", "CSV Files (*.csv)", options=options)
        if file_path:
            self.file_path_label.setText(file_path)



    def submit(self):
        mealplan_path = self.file_path_label.text()

        # Call the command line tool
        cmd = "./mealman.py " + mealplan_path
        try:
            output = subprocess.check_output(cmd, shell=True)
            output_str = output.decode("utf-8")
            self.status_label.setText("")

            # Get calories allowed today and calories in plan from the output
            output_lines = output_str.split("\n")
            max_calories = int(output_lines[0].split(": ")[1])
            calories_in_plan = int(output_lines[1].split(": ")[1])
            excess_calories = int(output_lines[2].split(": ")[1])

            # Update progress bar with percentage of calories in plan
            percentage = calories_in_plan / max_calories * 100
            self.progress_bar.setValue(int(percentage))

            # Display output in table
            table = QTableWidget(self)
            table.setColumnCount(2)
            table.setRowCount(3)

            table.setItem(0, 0, QTableWidgetItem("Calories Allowed Today"))
            table.setItem(0, 1, QTableWidgetItem(str(max_calories)))

            table.setItem(1, 0, QTableWidgetItem("Calories In Plan"))
            table.setItem(1, 1, QTableWidgetItem(str(calories_in_plan)))

            table.setItem(2, 0, QTableWidgetItem("Excess Calories"))
            table.setItem(2, 1, QTableWidgetItem(str(excess_calories)))

            # Set alternating row colors
            table.setAlternatingRowColors(True)

            # Set column header colors
            header = table.horizontalHeader()
            header.setStyleSheet("background-color: #570d00")

            # Set cell colors
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    if row % 2 == 0:
                        table.item(row, col).setBackground(QColor("#320049"))
                    else:
                        table.item(row, col).setBackground(QColor("#01381e"))

            table.move(20, 200)
            table.resize(600, 150)
            table.horizontalHeader().setDefaultSectionSize(200)
            table.verticalHeader().setDefaultSectionSize(20)
            table.show()

        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", e.output.decode("utf-8"))    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
