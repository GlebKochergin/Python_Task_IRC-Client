from PyQt6.QtWidgets import \
    QApplication, QPushButton, QVBoxLayout, QLineEdit, QWidget, QLabel, \
    QDialog, QScrollArea
from PyQt6.QtCore import Qt


class ChatWindow(QDialog):
    def __init__(self, handler):
        super(ChatWindow, self).__init__()
        self.setWindowTitle('IRC-Chat')
        self.resize(1200, 800)
        self.setMaximumSize(1200, 800)
        self.IRCHandler = handler
        self.setStyleSheet('background-image: url(second_back.png);')
        self.chat = QLabel()
        self.chat.setStyleSheet('background-color: #0F0F0F; '
                                'font-size : 15px;')
        self.chat.setMinimumSize(600, 200)
        self.chat.setMaximumSize(1200, 400)
        self.line = QLineEdit()
        self.line.setStyleSheet('background-color: #D2FFF2; '
                                'font-size : 30px;')
        self.send_message_button = QPushButton('Send!')
        self.send_message_button.clicked.connect(self.set_text_in_chat)
        self.line.setMinimumSize(600, 50)
        self.line.setMaximumSize(1200, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.chat)
        layout.addWidget(self.line)
        layout.addWidget(self.send_message_button)

        self.show()

        # while True:
        #     mes = self.IRCHandler.receive_messages()
        #     self.chat.setText(mes)
        #     self.IRCHandler.message = self.chat.text()

    def set_text_in_chat(self):
        # self.IRCHandler.send_message(self.line.text())
        self.chat.setText(self.line.text())
