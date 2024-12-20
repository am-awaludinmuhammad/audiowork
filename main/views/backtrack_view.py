import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
import requests
from ..utils import download_secret_mp3_file,chunk_mp3_file,obtain_token
from django.http import FileResponse, Http404
from wsgiref.util import FileWrapper
import time

from ..services.backing_track_service import generate_backing_track

def download_backtrack_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'back_track', filename)
    if os.path.exists(file_path):
        response = FileResponse(
            FileWrapper(open(file_path, 'rb')),
            content_type='audio/mpeg',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    else:
        raise Http404("File not found")

def download_backtrack(request):
    if request.method == 'POST':
        url = os.getenv('MY_SECRET_CHECK_URL')
        token = request.POST.get('token')
        payload = {"id": token}
        idx1 = os.getenv('MY_SECRET_RESULT_IDX_A')
        idx2 = os.getenv('MY_SECRET_RESULT_IDX_B')

        try:
            response = requests.post(url, data=payload)
            data = dict(response.json())
            
            download_file_url = data['result'][token][idx1][idx2]
            filename = f"back_track_{data['result'][token]['name']}"
            download_secret_mp3_file(download_file_url, filename=filename)

            return JsonResponse({
                "download_link": reverse('download_backtrack_file', args=[filename]),
                "filename": filename
            })
        except requests.exceptions.RequestException as e:
            # Handle exceptions
            return JsonResponse({
                "message": "An error occurred",
                "error": str(e)
            }, status=500)

    else:
        # data = obtain_secret_token('chunk_6_Song For An Eternal Child.mp3')
        data = {'token':'697a1948-9cd4-43a1-96b7-06bacbd93109'}
        if data.get('token'):
            job_status = do_the_secret_job(data['token'])

            if job_status == "success":
                print('sucess')
        #     removed = do_the_secret_job(data.id)
        #     print({'removed': removed})

        print({'obtain_secret_token': data})
        return render(request, 'download_backtrack.html')

def final_destination(request):
    return render(request, 'final_destination.html')

# step 1
def generate_attachment(request):
    if request.method == 'POST':
        mp3_file = request.FILES['mp3file']
        data = generate_backing_track(mp3_file)
        
        # obtain token
        # generate backing track
    
        return JsonResponse({
            'message': 'Attachments generated successfully',
            'status': 'success',
            'next_stage': 'Obtaining token',
            'next_url': reverse('obtain_secret_token'),
            'progress': 25,
            'data': data
        })

# def generate_backing_track(request):
#     time.sleep(5)
    
#     return JsonResponse({
#         'message': 'Backing track generated successfully',
#         'status': 'success',
#         'progress': 100
#     })

def obtain_secret_token(filename):
    time.sleep(3)
    # loop over the chunk file.txt
    chunk_file_paths = os.path.join(settings.MEDIA_ROOT,'chunk_list.txt')
    tokens = []
    with open(chunk_file_paths, 'r')  as f:
        for line in f:
            chunk_file_path = line.strip()
            filename = os.path.basename(chunk_file_path)
            obtain_token_data = obtain_token(filename)
            tokens.append(obtain_token_data)

    # obtain token for each file
    print(tokens)
    
    return JsonResponse({
        'message': 'Token obtained',
        'status': 'success',
        'next_stage': 'Generating backing track',
        'next_url': reverse('generate_backing_track'),
        'progress': 70
    })

    
    url = os.getenv('MY_SECRET_UPLOAD_URL')
    file_path = os.path.join(settings.MEDIA_ROOT,'splits', filename)
    file = {'attachment': open(file_path, 'rb')}
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

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
         return ({
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
        print({'do_the_secret_job': response.json()})
        return (response.json)
    except requests.exceptions.RequestException as e:

        return ({
                "message": "An error occurred",
                "error": str(e)
            })

    