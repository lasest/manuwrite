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

class PandocThread(QThread):

    def __init__(self, parent, markdown: str):
        super().__init__(parent)
        self.markdown = markdown
        self.html = ""

    def run(self):
        pandoc = subprocess.run(["pandoc", "--to", "html"], input=self.markdown.encode(), capture_output=True)
        pandoc.check_returncode()
        self.html = pandoc.stdout.decode()


class ThreadManager(QObject):

    manubotCiteThreadFinished = pyqtSignal(str, str)
    pandocThreadFinished = pyqtSignal(str)

    def __init__(self, max_threads: int = 4):

        super().__init__()

        self.running_threads = []
        self.pending_threads = []
        self.running_thread_count = 0
        self.max_threads = max_threads

    def get_citation(self, citekey: str):
        print("Received request to start thread")
        thread = ManubotCiteThread(self, citekey)
        thread.finished.connect(self.on_manubot_cite_thread_finished)

        if self.running_thread_count < self.max_threads:
            print("Starting thread")
            self.running_threads.append(thread)
            self.running_thread_count += 1
            thread.start()
        else:
            print("Putting thread to pending")
            self.pending_threads.append(thread)

    def markdown_to_html(self, markdown: str):
        print("Asked to start pandoc thread")
        thread = PandocThread(self, markdown)
        thread.finished.connect(self.on_pandoc_thread_finished)

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

        print("Finished thread. Obtained citation: ", citation, " for citekey ", citekey)

        self.manubotCiteThreadFinished.emit(citekey, citation)

    def run_next_thread(self):
        print("Looking for next thread to run")
        if self.pending_threads:
            print("Starting thread from pending")
            print("Thread count: ", self.running_thread_count)
            print("Pending thread count: ", len(self.pending_threads))
            self.running_threads.append(self.pending_threads[-1])
            self.running_thread_count += 1
            self.pending_threads[-1].start()
            self.pending_threads.remove(self.pending_threads[-1])
        else:
            print("No new thread to run")

    def on_pandoc_thread_finished(self):
        sender = QObject.sender(self)

        self.running_threads.remove(sender)
        self.running_thread_count -= 1
        self.run_next_thread()

        html = sender.html
        self.pandocThreadFinished.emit(html)
