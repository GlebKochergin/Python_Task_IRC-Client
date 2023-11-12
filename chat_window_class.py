import sys
import threading
import traceback

from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QWidget,
    QLabel,
    QDialog,
    QScrollArea,
)
from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
    QRunnable,
    QObject,
    QTimer,
    QThreadPool,
)

from logger import log


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(
                result
            )  # Return the result of the processing
        finally:
            self.signals.finished.emit()


class ChatWindow(QDialog):
    def __init__(self, handler):
        super(ChatWindow, self).__init__()
        self.setWindowTitle("IRC-Chat")
        self.resize(1200, 800)
        self.setMaximumSize(1200, 800)
        self.IRCHandler = handler
        self.setStyleSheet("background-image: url(second_back.png);")
        self.chat = QLabel()
        self.chat.setStyleSheet(
            "background-color: #0F0F0F; " "font-size : 15px;"
        )
        self.chat.setMinimumSize(600, 200)
        self.chat.setMaximumSize(1200, 400)
        self.line = QLineEdit()
        self.line.setStyleSheet(
            "background-color: #D2FFF2; " "font-size : 30px;"
        )
        self.send_message_button = QPushButton("Send!")
        self.send_message_button.clicked.connect(self.set_text_in_chat)
        self.line.setMinimumSize(600, 50)
        self.line.setMaximumSize(1200, 50)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.chat)
        layout.addWidget(self.line)
        layout.addWidget(self.send_message_button)

        self.show()

        self.pool = QThreadPool()
        self.update_message()

    def set_text_in_chat(self):
        worker = Worker(self.IRCHandler.send_message, self.line.text())
        worker.signals.finished.connect(self.set_mes_in_screen)
        worker.signals.error.connect(print)
        self.pool.start(worker)

    def set_mes_in_screen(self):
        self.chat.setText(f"{self.line.text()}")
        log("hello from set")

    def recieve_message(self, *arg):
        log(arg)
        log("hello from receive")
        if len(arg) == 0:
            return

        if arg[0] == None:
            return

        self.chat.setText(str(arg[0]))

    def update_message(self):
        worker = Worker(self.IRCHandler.receive_message)
        worker.signals.result.connect(self.recieve_message)
        worker.signals.error.connect(print)
        worker.signals.finished.connect(self.update_message)
        self.pool.start(worker)
