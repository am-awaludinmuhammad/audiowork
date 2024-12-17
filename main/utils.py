import requests
import os
from django.conf import settings

def download_secret_mp3_file(url, filename="downloaded_file.mp3"):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        media_path = os.path.join(settings.MEDIA_ROOT, 'back_track')
        if not os.path.exists(media_path):
            os.makedirs(media_path)

        file_path = os.path.join(media_path, filename)

        with open(file_path, 'wb') as mp3_file:
            for chunk in response.iter_content(chunk_size=8192):
                mp3_file.write(chunk)

        print(f"File saved at: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None
