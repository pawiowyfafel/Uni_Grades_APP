import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QComboBox, QTextBrowser, QMessageBox)
from PyQt5.QtCore import Qt

class Grades_app(QWidget):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Manage your grades!", self)
        self.semester_label = QLabel("Semester:", self)
        self.choose_semester = QComboBox(self)
        self.semester_find_button = QPushButton("FIND", self)
        
        self.semester_results = QTextBrowser(self) 
        
        self.subject = QLineEdit(self)
        self.semester = QLineEdit(self)
        self.grade = QLineEdit(self)
        self.operation = QComboBox(self)
        self.action = QPushButton("ACTION", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Grades Manager")
        self.setMinimumWidth(400) 
        self.setMinimumHeight(600)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 10px;
                color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6; /* Blue border on focus */
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 8px;
                color: #ffffff;
            }
            QComboBox:focus {
                border: 1px solid #3b82f6;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                selection-background-color: #3b82f6;
                border: 1px solid #333333;
            }
            QPushButton {
                background-color: #3b82f6; /* Modern Blue */
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QTextBrowser {
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 8px;
                padding: 10px;
            }
            /* Scrollbar customization */
            QScrollBar:vertical {
                border: none;
                background: #121212;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #3b82f6; margin-bottom: 15px; margin-top: 5px;")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.operation.addItems(["ADD", "FIND", "DELETE"])
        self.choose_semester.addItems(["1","2","3","4","5","6","7"])
        
        self.choose_semester.setFixedWidth(60)
        self.semester_find_button.setFixedWidth(80)

        self.subject.setPlaceholderText("Subject")
        self.semester.setPlaceholderText("Semester")
        self.grade.setPlaceholderText("Grade")

        self.semester_results.setMinimumHeight(180)
        self.semester_results.setPlaceholderText("Click FIND to see subjects from a given semester")

        self.subject.setAlignment(Qt.AlignCenter)
        self.semester.setAlignment(Qt.AlignCenter)
        self.grade.setAlignment(Qt.AlignCenter)
        
        hbox_semester = QHBoxLayout()
        hbox_semester.addStretch() 
        hbox_semester.addWidget(self.semester_label)
        hbox_semester.addWidget(self.choose_semester)
        hbox_semester.addWidget(self.semester_find_button)
        hbox_semester.addStretch() 

        hbox_inputs = QHBoxLayout()
        hbox_inputs.addWidget(self.semester)
        hbox_inputs.addWidget(self.grade)
        hbox_inputs.setSpacing(10) 

        hbox_action = QHBoxLayout()
        hbox_action.addWidget(self.operation)
        hbox_action.addWidget(self.action)
        hbox_action.setSpacing(10)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(25, 25, 25, 25) 
        vbox.setSpacing(15) 

        vbox.addWidget(self.title_label)
        vbox.addLayout(hbox_semester) 
        vbox.addWidget(self.semester_results) 
        
        vbox.addWidget(self.subject)      
        vbox.addLayout(hbox_inputs)       
        vbox.addLayout(hbox_action)       

        self.setLayout(vbox)

        self.action.clicked.connect(self.operation_manager)
        self.semester_find_button.clicked.connect(self.find_semester)

    def display_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStyleSheet("background-color: #1e1e1e; color: white;") 
        msg.exec_()

    def operation_manager(self):
        operation = self.operation.currentText()
        if operation == "ADD":
            subject_name = self.subject.text()
            semester = int(self.semester.text())
            grade = float(self.grade.text())
            add_url = f"http://127.0.0.1:5000/subject/add"
            try:
                add_data = {"subject" : subject_name,
                             "semester" : semester, 
                             "grade" : grade}

                response = requests.post(add_url, json=add_data)
                response.raise_for_status()
                self.find_semester()

            except requests.exceptions.HTTPError as httperror:
                match response.status_code:
                    case 400:
                        self.display_error("Bad request:\nPlease check your input")
                    case 401:
                        self.display_error("Unauthorized:\nInvalid API key")
                    case 403:
                        self.display_error("Forbidden:\nAccess is denied")
                    case 404:
                        self.display_error("Not Found:\nSubject Not Found")
                    case 500:
                        self.display_error("Internal server error:\nPlease try again later")
                    case 502:
                        self.display_error("Bad gateway:\nInvalid response from the server")
                    case 503:
                        self.display_error("Server unavailable:\nServer is down")
                    case 504:
                        self.display_error("Gateway timeout:\nNo response from the server")
                    case _:
                        self.display_error(f"HTTP error ocured:\n{httperror}")
            except requests.exceptions.ConnectionError:
                self.display_error("Connection Error:\nCheck your internet connection")
            except requests.exceptions.Timeout:
                self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many redirects:\nCheck the URL")                 
            except requests.exceptions.RequestException as reqerror:
                self.display_error(f"Request Error:\n{reqerror}")
                
        elif operation == "FIND":
            subject_name = self.subject.text()
            find_url = f"http://127.0.0.1:5000/subject/{subject_name}"
            try:
                find_response = requests.get(find_url)
                find_response.raise_for_status()
                find_data = find_response.json()
                find_subject = find_data["subject"]
                find_semester = str(find_data["semester"])
                find_grade = str(find_data["grade"])

                self.subject.setText(find_subject)
                self.semester.setText(find_semester)
                self.grade.setText(find_grade)
                self.find_semester()

            except requests.exceptions.HTTPError as httperror:
                match find_response.status_code:
                    case 400:
                        self.display_error("Bad request:\nPlease check your input")
                    case 401:
                        self.display_error("Unauthorized:\nInvalid API key")
                    case 403:
                        self.display_error("Forbidden:\nAccess is denied")
                    case 404:
                        self.display_error("Not Found:\nSubject Not Found")
                    case 500:
                        self.display_error("Internal server error:\nPlease try again later")
                    case 502:
                        self.display_error("Bad gateway:\nInvalid response from the server")
                    case 503:
                        self.display_error("Server unavailable:\nServer is down")
                    case 504:
                        self.display_error("Gateway timeout:\nNo response from the server")
                    case _:
                        self.display_error(f"HTTP error ocured:\n{httperror}")
            except requests.exceptions.ConnectionError:
                self.display_error("Connection Error:\nCheck your internet connection")
            except requests.exceptions.Timeout:
                self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many redirects:\nCheck the URL")                 
            except requests.exceptions.RequestException as reqerror:
                self.display_error(f"Request Error:\n{reqerror}")
                
        elif operation == "DELETE":
            subject_name = self.subject.text()
            delete_url = f"http://127.0.0.1:5000/subject/{subject_name}"
            try:
                response = requests.delete(delete_url)
                response.raise_for_status()
                self.find_semester()

            except requests.exceptions.HTTPError as httperror:
                match response.status_code:
                    case 400:
                        self.display_error("Bad request:\nPlease check your input")
                    case 401:
                        self.display_error("Unauthorized:\nInvalid API key")
                    case 403:
                        self.display_error("Forbidden:\nAccess is denied")
                    case 404:
                        self.display_error("Not Found:\nSubject Not Found")
                    case 500:
                        self.display_error("Internal server error:\nPlease try again later")
                    case 502:
                        self.display_error("Bad gateway:\nInvalid response from the server")
                    case 503:
                        self.display_error("Server unavailable:\nServer is down")
                    case 504:
                        self.display_error("Gateway timeout:\nNo response from the server")
                    case _:
                        self.display_error(f"HTTP error ocured:\n{httperror}")
            except requests.exceptions.ConnectionError:
                self.display_error("Connection Error:\nCheck your internet connection")
            except requests.exceptions.Timeout:
                self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many redirects:\nCheck the URL")                 
            except requests.exceptions.RequestException as reqerror:
                self.display_error(f"Request Error:\n{reqerror}")

    def find_semester(self):
        selected_semester = self.choose_semester.currentText()
        url = f"http://127.0.0.1:5000/get_semester/{selected_semester}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                self.semester_results.setHtml(f"<div style='text-align: center; color: #888888; font-size: 16px; margin-top: 20px;'><i>No available subjects in semester {selected_semester}.</i></div>")
                return

            html_content = """
            <table width="100%" cellspacing="0" cellpadding="8" style="font-size: 16px; color: #e0e0e0;">
            """
            for item in data:
                subject_name = item.get("subject", "Nieznany")
                grade = item.get("grade", "Brak")

                html_content += f"""
                <tr>
                    <td width="65%" style="border-right: 2px solid #444444; padding-left: 20px; text-align: left;">
                        {subject_name}
                    </td>
                    <td width="35%" style="padding-left: 20px; text-align: left; color: #3b82f6;">
                        <b>{grade}</b>
                    </td>
                </tr>
                """
            html_content += "</table>"
                
            self.semester_results.setHtml(html_content)

        except requests.exceptions.RequestException as reqerror:
            self.semester_results.setHtml(f"<div style='text-align: center;'><b style='color:#ef4444;'>Connection error:</b><br>{reqerror}</div>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    grades_app = Grades_app()
    grades_app.show()
    sys.exit(app.exec_())