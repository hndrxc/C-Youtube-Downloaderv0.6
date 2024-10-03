# from DLProjectPySide import YouTubeDownloaderFrame
def create_opts_list(self):
    download_dir1 = str
    self.ydl_opts_list = [

            # First version of ydl_opts
        {
            'format': 'mp3/bestaudio/best',
            'paths': {'home': download_dir1},
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        },
        {
            'format': 'bestvideo+bestaudio',
            'paths': {'home': download_dir1},
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],

        },
        {
            'format': 'bestaudio',
            'paths': {'home': download_dir1},
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
        }
    ]
    return self.ydl_opts_list