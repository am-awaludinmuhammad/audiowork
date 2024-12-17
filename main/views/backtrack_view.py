import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
import requests
from ..utils import download_secret_mp3_file
from django.http import FileResponse, Http404
from wsgiref.util import FileWrapper

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
        return render(request, 'download_backtrack.html')