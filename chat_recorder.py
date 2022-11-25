import threading

class ChatRecorder:
    def __init__(self, file_name: str):
        self.file_name = file_name
        file = open(file_name, "w")
        file.close()


    def add_record(self, record: str):
        rec = self._apply_record_format(record)
        with open(self.file_name, "a") as f:
            f.write(rec+"\n")

    @staticmethod
    def _apply_record_format(record: str):

        return record
