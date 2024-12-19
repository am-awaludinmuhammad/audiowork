import requests
import os
from django.conf import settings
from pydub import AudioSegment
from wsgiref.util import FileWrapper
from django.urls import reverse

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
        return None
    
def chunk_mp3_file(mp3_file):
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    filename = mp3_file.name
    file_path = os.path.join(temp_dir, filename)

    with open(file_path, 'wb+') as destination:
        for chunk in mp3_file.chunks():
            destination.write(chunk)
    
    audio = AudioSegment.from_file(file_path)
    chunks = []
    one_minute = 60 * 1000
    overlap = 2 * 1000

    start_time = 0

    audio_length = len(audio)
    while start_time + one_minute <= audio_length:
        end_time = start_time + one_minute
        chunks.append(audio[start_time:end_time])

        start_time = (end_time - overlap)

    remaining_audio = audio[start_time:]

    txt_chunk_path = os.path.join(settings.MEDIA_ROOT, 'chunk_list.txt')
    if os.path.exists(txt_chunk_path):
        os.remove(txt_chunk_path)

    chunk_paths = []
    if len(remaining_audio) > 0:
        chunks.append(remaining_audio)

        output_dir = os.path.join(settings.MEDIA_ROOT, 'splits')
        os.makedirs(output_dir, exist_ok=True)

        download_links = []
        for idx, chunk in enumerate(chunks):
            chunk_filename = f"chunk_{idx + 1}_{filename}"
            output_path = os.path.join(output_dir, chunk_filename)
            chunk.export(output_path, format="mp3")
            chunk_paths.append({
                'filename': chunk_filename,
                'filepath': output_path
            })
            with open(txt_chunk_path, 'a') as f:
                f.write(f"{output_path}\n")

            download_links.append({
                'download_link': reverse('download_chunk', args=[chunk_filename]),
                'filename': chunk_filename
            })

        total_chunks = len(chunks)
        remaining_duration = len(audio) % one_minute // 1000  # In seconds

        os.remove(file_path)
        return {
            "total_chunks": total_chunks,
            "remaining_duration": remaining_duration,
            "download_links": download_links,
            'results': chunk_paths
        }

def obtain_token(filename):
    url = os.getenv('MY_SECRET_UPLOAD_URL')
    file_path = os.path.join(settings.MEDIA_ROOT,'splits', filename)
    file = {'attachment': open(file_path, 'rb')}
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    import random
    random_float_in_range = random.uniform(1, 10)
    return ({
            'token': random_float_in_range   
        })
    try:
        response = requests.post(url, headers=headers, files=file)
        data = response.json()
        print({'obtain_secret_token_raw':data})

        token = ""

        if data.get('status') == 'success':
            token = data.get(os.getenv('TOKEN_KEY'))

            
        return ({
            'token': token
        })
    except requests.exceptions.RequestException as e:
        print('obtain_token err')
        return ({
            "status": "error",
            "message": "An error occurred",
            "error": str(e)
        })