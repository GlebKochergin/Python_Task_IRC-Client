import threading
from logger import log

#убрать все в одно место
class IRCDataAnalyzer:
    def __init__(self, get_formatted):
        self._mutex = threading.Lock()
        self._not_formatted_data = str()
        self._formatted_data = []
        self._data_format_func = get_formatted

    async def add_raw_data(self, ans: str):
        self._mutex.acquire()
        self._not_formatted_data += ans
        self._mutex.release()

    def data_analyze(self):
        self._formatted_data = self._data_format_func(self._not_formatted_data)

    async def get_data(self) -> [str]:
        log("!!!!!!!!!!!!!!!!!!!!!!!")
        log(self._not_formatted_data)
        if len(self._formatted_data) == 0:
            self.data_analyze()

        return self._formatted_data
