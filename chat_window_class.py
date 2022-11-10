from PyQt6.QtWidgets import \
    QApplication, QPushButton, QVBoxLayout, QLineEdit, QWidget, QLabel, QDialog
import sys


class ServerWindow(QDialog):
    def __init__(self):
        super(ServerWindow, self).__init__()
        self.setWindowTitle('IRC-Chat')
        self.resize(600, 400)
        self.setMaximumSize(1200, 800)
        self.setStyleSheet('background-image: url(second_back.png);')
        self.text = QLabel('Здесь должен быть сервер: \n'
                           'каналы, чаты, пользователи')
        self.text.setStyleSheet('font-size : 40px;')
        self.text.setMinimumSize(500, 50)
        self.text.setMaximumSize(600, 100)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.text)

        self.show()
