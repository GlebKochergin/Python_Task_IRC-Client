from PyQt6.QtWidgets import \
    QApplication, QPushButton, QVBoxLayout, QLineEdit, QWidget
import sys


app = QApplication(sys.argv)


class MainWindow(QWidget):
    def __init__(self, name: str):
        super(MainWindow, self).__init__()
        self.setWindowTitle(name)
        self.resize(600, 400)
        self.setMaximumSize(1200, 800)
        self.setStyleSheet(stylesheet_start)

        layout = QVBoxLayout()
        self.setLayout(layout)

        irc_server_input = QLineEdit()
        irc_server_input.setMinimumSize(300, 50)
        irc_server_input.setMaximumSize(600, 50)
        irc_server_input.setPlaceholderText('Вставьте ссылку на IRC-сервер')
        irc_server_input.setEchoMode(QLineEdit.EchoMode.Normal)

        nickname = QLineEdit()
        nickname.setMinimumSize(300, 50)
        nickname.setMaximumSize(600, 50)
        nickname.setPlaceholderText('Введите свой никнейм')
        nickname.setEchoMode(QLineEdit.EchoMode.Normal)

        enter_button = QPushButton('&Enter')
        enter_button.setMinimumSize(300, 50)
        enter_button.setMaximumSize(600, 50)

        layout.addWidget(irc_server_input)
        layout.addWidget(nickname)
        layout.addWidget(enter_button)


stylesheet_start = """
        QWidget {
            background-color: white;
            font-size : 30px;
        }
        QPushButton {
            background-color: yellow;
            font-size: 20px;
        }
        MainWindow {
            background-color: pink;
        }    
    """


def start_app():
    window = MainWindow('IRC-Client')
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    start_app()
