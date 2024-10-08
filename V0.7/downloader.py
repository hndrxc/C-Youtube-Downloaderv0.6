from idlelib.pathbrowser import PathBrowser

from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QComboBox, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon
from PySide6 import QtCore
from options import create_opts_list, download_thumbnail
from threading import Thread
import yt_dlp





class YouTubeDownloaderFrame(QMainWindow):
    def __init__(self):
        super(YouTubeDownloaderFrame, self).__init__()
        # Main widget
        widget = QWidget()
        self.setCentralWidget(widget)

        vbox = QVBoxLayout()
        # URL input field

        self.url_label = QLabel("YouTube URL:")
        vbox.addWidget(self.url_label)
        self.url_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.url_input = QLineEdit()
        vbox.addWidget(self.url_input)
        # Format selection
        self.combo_box = QComboBox()
        vbox.addWidget(self.combo_box)
        self.combo_box.addItem("Mp3")
        self.combo_box.addItem("Mp4")
        self.combo_box.addItem("Wav")
        self.combo_box.currentIndexChanged.connect(self.on_selection_change)
        # Directory picker
        self.dir_picker_button = QPushButton("Select download directory")
        vbox.addWidget(self.dir_picker_button)
        self.dir_picker_button.clicked.connect(self.select_directory)

        # Download button
        self.download_button = QPushButton("Download")
        vbox.addWidget(self.download_button)
        self.download_button.clicked.connect(self.on_download)

        # Status display
        self.status_text = QLabel("")
        vbox.addWidget(self.status_text)

        # Downloads display table
        self.dl_table = QTableWidget(0, 1, self)
        self.dl_table.resizeColumnsToContents()
        self.dl_table.horizontalHeader().setStretchLastSection(True)
        self.dl_table.verticalHeader().setStretchLastSection(True)
        labels = ["Downloads", "Format", "Path"]
        self.dl_table.setHorizontalHeaderLabels(labels)
        vbox.addWidget(self.dl_table)

        widget.setLayout(vbox)
        self.setWindowTitle("YouTube Audio Extractor")
        self.setGeometry(300, 300, 400, 300)
        self.local_options = create_opts_list(self)

    def on_selection_change(self, index):
        print(f"Selected index: {index}, item: {self.sender().currentText()}")

    def selected_format(self):
        if self.combo_box.currentText() == "Mp3":
            return self.local_options[0]
        elif self.combo_box.currentText() == "Mp4":
            return self.local_options[1]
        elif self.combo_box.currentText() == "Wav":
            return self.local_options[2]

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selected_directory = directory
            self.status_text.setText(directory)

    def on_download(self):
        url = self.url_input.text()
        download_dir = getattr(self, 'selected_directory', '')

        if not url:
            self.status_text.setText("Please enter a valid URL.")
        else:
            self.status_text.setText(f"Downloading to {download_dir}...")
            download_thread = Thread(target=self.download_file, args=(url, download_dir))
            download_thread.start()

    def download_file(self, url, download_dir):
        try:
            ydl_opt = self.selected_format()
            ydl_opt['paths']['home'] = download_dir

            with yt_dlp.YoutubeDL(ydl_opt) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict.get('title', 'Unknown Title')
                thumbnail_url = info_dict.get('thumbnail', None)
                print(thumbnail_url)
                ydl.download([url])
                self.thumbnail_path = download_thumbnail(thumbnail_url, video_title, download_dir)
                thumbnail_path = self.thumbnail_path
                self.previous_downloads(video_title)

            self.status_text.setText("Download complete!")
        except Exception as e:
            self.status_text.setText(f"Error: {str(e)}")

    def previous_downloads(self, video_title):
        row_position = self.dl_table.rowCount()
        self.dl_table.insertRow(row_position)
        new_item = QTableWidgetItem(video_title)
        icon = QIcon(getattr(self, 'thumbnail_path'))
        new_item.setIcon(icon)
        self.dl_table.setItem(row_position, 0, new_item)

