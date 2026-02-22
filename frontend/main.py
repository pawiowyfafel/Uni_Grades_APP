import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMenu, QComboBox)
from PyQt5.QtCore import Qt

class Grades_app(QWidget):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("Manage your grades!", self)
        self.subject = QLineEdit(self)
        self.semester = QLineEdit(self)
        self.grade = QLineEdit(self)
        self.operation = QComboBox(self)
        self.action = QPushButton("ACTION", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Grades Manager")

        self.operation.addItems(["ADD", "FIND", "DELETE"])
        self.subject.setPlaceholderText("Subject")
        self.semester.setPlaceholderText("Semester")
        self.grade.setPlaceholderText("Grade")

        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.subject)
        vbox.addWidget(self.semester)
        vbox.addWidget(self.grade)
        vbox.addWidget(self.operation)
        vbox.addWidget(self.action)

        self.setLayout(vbox)

        self.title_label.setAlignment(Qt.AlignCenter)
        self.subject.setAlignment(Qt.AlignCenter)
        self.semester.setAlignment(Qt.AlignCenter)
        self.grade.setAlignment(Qt.AlignCenter)

        self.action.clicked.connect(self.operation_manager)

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

                requests.post(add_url, json=add_data)

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
                self.display_error("Connection Eroor:\nCheck your internet connection")
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
                self.display_error("Connection Eroor:\nCheck your internet connection")
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
                requests.delete(delete_url)

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
                self.display_error("Connection Eroor:\nCheck your internet connection")
            except requests.exceptions.Timeout:
                self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many redirects:\nCheck the URL")                 
            except requests.exceptions.RequestException as reqerror:
                self.display_error(f"Request Error:\n{reqerror}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    grades_app = Grades_app()
    grades_app.show()
    sys.exit(app.exec_())