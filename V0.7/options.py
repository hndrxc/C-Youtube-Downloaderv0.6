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

def download_thumbnail(thumbnail_url, video_title, download_dir):
    import requests
    import os

    # Get the file extension of the thumbnail (e.g., .jpg, .png)
    file_extension = thumbnail_url.split('.')[-1]

    # Create the thumbnail file path using the video title
    thumbnail_path = os.path.join(download_dir, f"{video_title}_thumbnail.{file_extension}")

    # Download the thumbnail using requests
    response = requests.get(thumbnail_url)
    with open(thumbnail_path, 'wb') as f:
        f.write(response.content)

    print(f"Thumbnail saved at: {thumbnail_path}")
    return thumbnail_path