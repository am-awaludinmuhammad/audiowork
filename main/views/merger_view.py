import os
from pydub import AudioSegment
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from wsgiref.util import FileWrapper
from django.http import FileResponse, Http404

def merge(files, merge_type = 'normal'):
    file_paths = []

    # Save uploaded files to the media directory
    for file in files:
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        file_paths.append(file_path)

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

def merge_mp3(request):
    if request.method == "POST":
        files = request.FILES.getlist("files")

        # Validate the number of uploaded files
        if len(files) < 2:
            return JsonResponse({"error": "Please upload at least two MP3 files."}, status=400)

        data = merge(files, 'overlap')
        return JsonResponse(data)
    elif request.method == "GET":
        return render(request, "merger_upload.html")

    return JsonResponse({"error": "Invalid request method."}, status=400)

def download_file_merge(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(file_path):
        response = FileResponse(
            FileWrapper(open(file_path, 'rb')),
            content_type='audio/mpeg',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    else:
        raise Http404("File not found")
