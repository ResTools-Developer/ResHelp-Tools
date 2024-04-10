import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QLineEdit, QProgressBar, QMessageBox, QComboBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
import sys 

MAX_RETRIES = 20
RETRY_DELAY = 3  # Delay between retries in seconds
MAX_CONCURRENT_REQUESTS = 10 # Maximum number of concurrent requests
THROTTLING_DELAY = 0.2  # Delay between each concurrent request in seconds

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int, int)  # Signal to indicate download finished with success and error counts

    def __init__(self, names, save_folder, file_type):
        super().__init__()
        self.names = names
        self.save_folder = save_folder
        self.file_type = file_type

    def update_progress(self, value):
        # Emit the progress signal via QMetaObject.invokeMethod to ensure it's handled in the main thread
        QMetaObject.invokeMethod(self.progress, "emit", Qt.ConnectionType.QueuedConnection, value)

    def run(self):
        total_chemicals = len(self.names)
        downloaded_count = 0
        error_count = 0

        log_file = os.path.join(self.save_folder, "download_errors.log")
        cid_list_file = os.path.join(self.save_folder, "cid_list.txt")

        with open(cid_list_file, 'w') as cid_file:
            with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
                futures = []
                for name in self.names:
                    name = name.strip()  # Remove leading/trailing whitespace and newline characters
                    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{quote_plus(name)}/cids/JSON?name_type=word"
                    future = executor.submit(self.download_and_track_progress, url, self.save_folder, self.file_type, log_file, cid_file)
                    futures.append(future)
                    time.sleep(THROTTLING_DELAY)  # Introduce a delay between each concurrent request
                
                for future in futures:
                    result = future.result()
                    if result:
                        downloaded_count += 1
                    else:
                        error_count += 1
                    self.update_progress(int((downloaded_count + error_count) / total_chemicals * 100))
            
        self.finished.emit(downloaded_count, error_count)

    def download_and_track_progress(self, url, save_folder, file_type, log_file, cid_file):
        session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'IdentifierList' in data:
                cid = data['IdentifierList']['CID'][0]
                url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/{file_type}/?record_type=3d"
                if self.download_file(url, save_folder, f"{cid}.{file_type}", log_file):
                    cid_file.write(f"{cid}\n")  # Write CID to cid_list.txt
                    return True
        else:
            error_msg = f"Failed to download {file_type} file for {url}: {response.status_code} - {response.reason}"
            self.log_error(error_msg, log_file)
        return False

    def download_file(self, url, save_folder, filename, log_file):
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(save_folder, filename), 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return True
        else:
            error_msg = f"Failed to download {filename}: {response.status_code} - {response.reason}"
            self.log_error(error_msg, log_file)
            response.raise_for_status()  # Raise an exception for non-200 responses

    def log_error(self, error_msg, log_file):
        with open(log_file, 'a') as f:
            f.write(error_msg + '\n')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PubChem Database')
        self.setWindowIcon(QIcon('logo.png'))

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.btn = QPushButton('Select File')
        self.btn.clicked.connect(self.selectFile)
        vbox.addWidget(self.btn)

        self.label = QLabel()
        vbox.addWidget(self.label)

        self.textEdit = QTextEdit()
        vbox.addWidget(self.textEdit)

        self.saveFolderBtn = QPushButton('Select Save Folder')
        self.saveFolderBtn.clicked.connect(self.selectSaveFolder)
        vbox.addWidget(self.saveFolderBtn)

        self.fileTypeInput = QComboBox()
        self.fileTypeInput.addItems(["sdf", "json", "xml", "asnt"])
        vbox.addWidget(self.fileTypeInput)

        self.downloadBtn = QPushButton('Start Download')
        self.downloadBtn.clicked.connect(self.startDownload)
        vbox.addWidget(self.downloadBtn)

        self.progressBar = QProgressBar(self)
        vbox.addWidget(self.progressBar)

        self.setGeometry(300, 300, 300, 200)

        self.retryBtn = QPushButton('Retry Failed Downloads')
        self.retryBtn.clicked.connect(self.retryFailedDownloads)
        self.retryBtn.setEnabled(False)  # Disable the button initially
        vbox.addWidget(self.retryBtn)

    def selectFile(self):
        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.label.setText(fname[0])
            with open(fname[0], 'r') as f:
                data = f.read()
                self.textEdit.setText(data)

    def selectSaveFolder(self):
        save_folder = QFileDialog.getExistingDirectory(self)
        self.saveFolderBtn.setText(save_folder if save_folder else 'Select Save Folder')

    def startDownload(self):
        names = self.textEdit.toPlainText().split('\n')
        save_folder = self.saveFolderBtn.text()
        file_type = self.fileTypeInput.currentText()
        self.downloadThread = DownloadThread(names, save_folder, file_type)
        self.downloadThread.progress.connect(self.progressBar.setValue)
        self.downloadThread.finished.connect(self.downloadFinished)
        self.downloadThread.start()
        self.downloadBtn.setText("Downloading...")

    def downloadFinished(self, success_count, error_count):
        self.downloadBtn.setText("Start Download")
        QMessageBox.information(self, "Download Finished", f"Download finished with {success_count} successful downloads and {error_count} errors.")
        self.retryBtn.setEnabled(True)  # Enable the retry button after download finished

    def retryFailedDownloads(self):
        log_file = os.path.join(self.saveFolderBtn.text(), "download_errors.log")
        with open(log_file, 'r') as f:
            lines = f.readlines()
        failed_chemicals = [line.split(':')[1].strip() for line in lines if '503' in line]
        self.textEdit.setText('\n'.join(failed_chemicals))
        QMessageBox.question(self, "Retry Failed Downloads", "Do you want to retry downloading for these chemicals?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if QMessageBox.StandardButton.Yes:
            self.startDownload()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())
