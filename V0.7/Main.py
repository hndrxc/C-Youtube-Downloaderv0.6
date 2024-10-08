from PySide6.QtWidgets import QApplication
from downloader import YouTubeDownloaderFrame

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = YouTubeDownloaderFrame()
    main_window.show()
    sys.exit(app.exec())
