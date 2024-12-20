import requests
import os
from django.conf import settings
from pydub import AudioSegment
from wsgiref.util import FileWrapper
from django.urls import reverse
import logging
logger = logging.getLogger('file')

def merge_by_paths(file_paths, merge_type = 'overlap'):
    # Prepare output path
    output_file = os.path.join(settings.MEDIA_ROOT, "merged_output.mp3")
    combined_audio = AudioSegment.empty()

    for idx, file_path in enumerate(file_paths):
        audio = AudioSegment.from_file(file_path)
        
        if merge_type == 'overlap':
            if idx == 0:
                # First file: Remove last 1 second
                trimmed_audio = audio[:-1000]
            elif idx == len(file_paths) - 1:
                # Last file: Remove first 1 second
                trimmed_audio = audio[1000:]
            else:
                # Middle files: Remove first and last 1 second
                trimmed_audio = audio[1000:-1000]
        else:
            # Normal merge without trimming
            trimmed_audio = audio

        # Combine the processed audio
        combined_audio += trimmed_audio

    # Export the final merged audio
    combined_audio.export(output_file, format="mp3")

    # Cleanup temporary file list
    with open("file_list.txt", "w") as f:
        for file_path in file_paths:
            os.remove(file_path)
    os.remove("file_list.txt")

    link = reverse('download_file_merge', args=['merged_output.mp3'])
    filename = 'merged_output.mp3'

    return {
            'download_link':link,
            'filename':filename
        }

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

def obtain_token(file_path):
    url = os.getenv('MY_SECRET_UPLOAD_URL')
    filename = os.path.basename(file_path)
    file = {'attachment': open(file_path, 'rb')}
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

    import random
    random_float_in_range = random.uniform(1, 10)
    try:
        response = requests.post(url, headers=headers, files=file)
        data = response.json()
        logger.info(data)

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

def do_the_secret_job(token):
    url = os.getenv('MY_SECRET_JOB_URL')
    headers = {
        "Authorization": os.getenv('MY_SECRET_AUTHORIZATION')
    }
    payload = {
        os.getenv('TOKEN_KEY') : token,
        os.getenv('JOB1_KEY') : os.getenv('JOB1_VALUE'),
        os.getenv('JOB2_KEY') : os.getenv('JOB2_VALUE'),
        os.getenv('JOB3_KEY') : os.getenv('JOB3_VALUE'),
        os.getenv('JOB2_KEY') : os.getenv('JOB2_VALUE'),
        os.getenv('JOB2_KEY') : os.getenv('JOB2_VALUE'),
        os.getenv('JOB2_KEY') : os.getenv('JOB2_VALUE')
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()

        logger.info(data)

        return {
            "status": data.get('status')
        }
    except requests.exceptions.RequestException as e:
        return {
                "message": "An error occurred",
                "error": str(e)
            }

def get_processed_file(token):
    url = os.getenv('MY_SECRET_CHECK_URL')
    payload = {"id": token}
    idx1 = os.getenv('MY_SECRET_RESULT_IDX_A')
    idx2 = os.getenv('MY_SECRET_RESULT_IDX_B')

    try:
        response = requests.post(url, data=payload)
        data = dict(response.json())
        print({'split raw data': data})
        
        # download_file_url = data['result'][token][idx1][idx2]
        # filename = f"back_track_{data['result'][token]['name']}"
        
        # file_path = download_secret_mp3_file(download_file_url, filename=filename)

        return {
            "filepath": 'file_path',
        }
    except requests.exceptions.RequestException as e:
        return {
            "message": "An error occurred",
            "error": str(e)
        }
