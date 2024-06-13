#HariOm
"""
Copyright 2024 Manav Amit Choudhary

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QLineEdit, QProgressBar, QMessageBox, QComboBox, QHBoxLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMetaObject 
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
import sys 

MAX_RETRIES = 20
RETRY_DELAY = 3  # Delay between retries in seconds
MAX_CONCURRENT_REQUESTS = 10 # Maximum number of concurrent requests
THROTTLING_DELAY = 0.2  # Delay between each concurrent request in seconds

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int, int)  # Signal to indicate download finished with success and error counts

    def __init__(self, names, save_folder, file_type, is_retry):
        super().__init__()
        self.names = names
        self.save_folder = save_folder
        self.file_type = file_type
        self.is_retry = is_retry

    def update_progress(self, value):
        # Emit the progress signal via QMetaObject.invokeMethod to ensure it's handled in the main thread
        self.progress.emit(value)

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
                    if self.is_retry:
                        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{name}/record/{self.file_type}/?record_type=3d"
                        future = executor.submit(self.download_file, url, self.save_folder, f"{name}.{self.file_type}", log_file)
                    else:
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
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'IdentifierList' in data:
                cid = data['IdentifierList']['CID'][0]
                cid_file.write(f"{cid}\n")  # Write CID to cid_list.txt
                file_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{cid}/record/{file_type}/?record_type=3d"
                return self.download_file(file_url, save_folder, f"{cid}.{file_type}", log_file)
        else:
            error_msg = f"Failed to download {file_type} file for {url}: {response.status_code} - {response.reason}"
            self.log_error(error_msg, log_file)
        return False

    def download_file(self, url, save_folder, filename, log_file):
        session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        response = session.get(url, stream=True)
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
        icon_path = os.path.join(os.path.dirname(__file__), '../root/logo.png')
        self.setWindowIcon(QIcon(icon_path))  # Set icon path accordingly
        self.setMinimumSize(600, 400)  # Set minimum window size

        # Apply dark theme
        self.applyDarkTheme()

        vbox = QVBoxLayout(self)

        # Title label with larger font
        title_font = QFont("Arial", 18)
        title_label = QLabel('PubChem Database')
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(title_label)

        # Horizontal layout for file selection buttons
        button_layout = QHBoxLayout()

        self.btn_select_file = QPushButton('Select File')
        self.btn_select_file.clicked.connect(self.selectFile)
        self.styleButton(self.btn_select_file)
        button_layout.addWidget(self.btn_select_file)

        self.btn_select_save_folder = QPushButton('Select Save Folder')
        self.btn_select_save_folder.clicked.connect(self.selectSaveFolder)
        self.styleButton(self.btn_select_save_folder)
        button_layout.addWidget(self.btn_select_save_folder)

        vbox.addLayout(button_layout)

        self.label = QLabel()
        self.label.setStyleSheet("color: white;")
        vbox.addWidget(self.label)

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Enter chemical names or CID numbers, one per line...")
        self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
            }
            QTextEdit::placeholder {
                color: white;
            }
        """)
        vbox.addWidget(self.textEdit)

        self.fileTypeInput = QComboBox()
        self.fileTypeInput.addItems(["sdf", "json", "xml", "asnt"])
        self.styleComboBox(self.fileTypeInput)
        vbox.addWidget(self.fileTypeInput)

        self.downloadBtn = QPushButton('Start Download')
        self.downloadBtn.clicked.connect(self.startDownload)
        self.styleButton(self.downloadBtn)
        vbox.addWidget(self.downloadBtn)

        self.progressBar = QProgressBar(self)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 20px;
            }
        """)
        vbox.addWidget(self.progressBar)

        self.retryBtn = QPushButton('Retry Failed Downloads')
        self.retryBtn.clicked.connect(self.retryFailedDownloads)
        self.styleButton(self.retryBtn)
        vbox.addWidget(self.retryBtn)

        self.retryBtn.setEnabled(False)  # Disable retry button initially

    def applyDarkTheme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(dark_palette)

        font = QFont("Arial", 12)
        self.setFont(font)

    def styleButton(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #353535;
                color: white;
                border: 2px solid #05B8CC;
                padding: 10px;
                border-radius: 20px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #454545;
            }
        """)

    def styleComboBox(self, combo_box):
        combo_box.setStyleSheet("""
            QComboBox {
                background-color: #3E3E3E;
                color: white;
                border: 1px solid gray;
                padding: 5px;
                border-radius: 10px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

    def selectFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt);;All Files (*)")
        if fname:
            self.label.setText(f"Selected file: {fname}")
            with open(fname, 'r') as f:
                data = f.read()
                self.textEdit.setText(data)

    def selectSaveFolder(self):
        save_folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if save_folder:
            self.btn_select_save_folder.setText(f"Save Folder: {save_folder}")
        else:
            self.btn_select_save_folder.setText('Select Save Folder')

    def startDownload(self):
        names = self.textEdit.toPlainText().split('\n')
        save_folder = self.btn_select_save_folder.text().replace('Save Folder: ', '')
        file_type = self.fileTypeInput.currentText()
        self.downloadThread = DownloadThread(names, save_folder, file_type, self.retryBtn.isEnabled())
        self.downloadThread.progress.connect(self.progressBar.setValue)
        self.downloadThread.finished.connect(self.downloadFinished)
        self.downloadThread.start()
        self.downloadBtn.setText("Downloading...")
        self.downloadBtn.setEnabled(False)

    def downloadFinished(self, success_count, error_count):
        self.downloadBtn.setText("Start Download")
        self.downloadBtn.setEnabled(True)
        QMessageBox.information(self, "Download Finished", f"Download finished with {success_count} successful downloads and {error_count} errors.")
        if error_count > 0:
            self.retryBtn.setEnabled(True)

    def retryFailedDownloads(self):
        log_file = QFileDialog.getOpenFileName(self, "Select Log File", "", "Log Files (*.log)")
        if log_file[0]:
            with open(log_file[0], 'r') as f:
                lines = f.readlines()
            failed_chemicals = [line.split(' ')[3].split('.')[0] for line in lines if '503' in line]
            self.textEdit.setText('\n'.join(failed_chemicals))
            self.startDownload()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), '../root/logo.png')
    app.setWindowIcon(QIcon(icon_path))

    ex = MyApp()
    ex.show()
    sys.exit(app.exec())