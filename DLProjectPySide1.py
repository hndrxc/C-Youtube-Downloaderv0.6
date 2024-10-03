from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QFileDialog, QApplication, QComboBox, )
from PySide6 import QtCore
import yt_dlp
from options1 import create_opts_list
from threading import Thread



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
        #Format selection
        self.combo_box = QComboBox()
        vbox.addWidget(self.combo_box)
        self.combo_box.addItem("Mp3")
        self.combo_box.addItem("Mp4")
        self.combo_box.addItem("Wav")
        self.combo_box.currentIndexChanged.connect(self.on_selection_change)
        #event handler to respond to selection changes

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
            # download logic here
        download_thread = Thread(target=self.download_audio, args=(url, download_dir))
        download_thread.start()

    def download_audio(self, url, download_dir):
        try:
            ydl_opt = self.selected_format()
            # ydl_opt['paths']['home'] = getattr(self, 'selected_directory', '')  below has identical functionality
            ydl_opt['paths']['home'] = download_dir
            # print(ydl_opt)
            with yt_dlp.YoutubeDL(ydl_opt) as ydl:
                ydl.download([url])
            self.status_text.setText("Download complete!")
        except Exception as e:
            self.status_text.setText(f"Error: {str(e)}")


# For running the application
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = YouTubeDownloaderFrame()
    main_window.show()
    sys.exit(app.exec())
