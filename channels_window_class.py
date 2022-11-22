from PyQt6.QtWidgets import \
    QApplication, QPushButton, QVBoxLayout, QLineEdit, QWidget, QLabel, \
    QDialog, QScrollArea


class ServerWindow(QScrollArea):
    def __init__(self, func):
        super(ServerWindow, self).__init__()
        self.setWindowTitle('IRC-Chat')
        self.resize(1200, 800)
        self.setMaximumSize(1200, 800)
        self.setStyleSheet('background-image: url(second_back.png);')
        self.channels = ['#server1', '#server2', '#server3',
                         '#server4', '#server5']

        layout = QVBoxLayout()
        self.setLayout(layout)

        for i in range(len(self.channels)):
            server_button = QPushButton(f'{self.channels[i]}')
            server_button.setStyleSheet('background-color: #2DBC91;'
                                        'font-size: 20px;')
            server_button.setMinimumSize(500, 50)
            server_button.setMaximumSize(600, 50)
            layout.addWidget(server_button)
            server_button.clicked.connect(func)

        self.show()
