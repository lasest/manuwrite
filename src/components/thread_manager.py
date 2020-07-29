import subprocess

from PyQt5.QtCore import QThread, QObject, pyqtSignal


class ManubotCiteThread(QThread):

    def __init__(self, parent, citekey: str):
        super().__init__(parent)
        self.citekey = citekey
        self.citation = ""

    def run(self):
        manubot = subprocess.run(["manubot", "cite", "--render", self.citekey], capture_output=True)
        manubot.check_returncode()
        self.citation = manubot.stdout.decode()


class ThreadManager(QObject):

    manubotCiteThreadFinished = pyqtSignal(str, str)

    def __init__(self, max_threads: int = 4):

        super().__init__()

        self.running_threads = []
        self.pending_threads = []
        self.running_thread_count = 0
        self.max_threads = max_threads

    def get_citation(self, citekey: str):
        thread = ManubotCiteThread(self, citekey)
        thread.finished.connect(self.on_manubot_cite_thread_finished)

        if self.running_thread_count < self.max_threads:
            self.running_threads.append(thread)
            self.running_thread_count += 1
            thread.start()
        else:
            self.pending_threads.append(thread)

    def on_manubot_cite_thread_finished(self):
        sender = QObject.sender(self)
        self.running_threads.remove(sender)
        self.running_thread_count -= 1
        self.run_next_thread()

        citekey = sender.citekey
        citation = sender.citation

        self.manubotCiteThreadFinished.emit(citekey, citation)

    def run_next_thread(self):
        if self.pending_threads:
            self.running_threads.append(self.pending_threads[-1])
            self.running_thread_count += 1
            self.pending_threads[-1].run()
            del self.pending_threads[-1]
