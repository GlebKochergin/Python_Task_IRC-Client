from PyQt6.QtWidgets import \
    QApplication, QPushButton, QVBoxLayout, QLineEdit, QWidget, QLabel, \
    QDialog, QScrollArea
from PyQt6.QtCore import Qt


class ChatWindow(QDialog):
    def __init__(self):
        super(ChatWindow, self).__init__()
        self.setWindowTitle('IRC-Chat')
        self.resize(1200, 800)
        self.setMaximumSize(1200, 800)
        self.setStyleSheet('background-image: url(second_back.png);')
        self.chat = QLabel('Guest1 : Приветик!')
        self.chat.setStyleSheet('background-color: #0F0F0F; '
                                'font-size : 15px;')
        self.chat.setMinimumSize(600, 200)
        self.chat.setMaximumSize(1200, 400)
        self.line = QLineEdit()
        self.line.setStyleSheet('background-color: #D2FFF2; '
                                'font-size : 30px;')
        self.line.setMinimumSize(600, 50)
        self.line.setMaximumSize(1200, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.chat)
        layout.addWidget(self.line)

        self.show()