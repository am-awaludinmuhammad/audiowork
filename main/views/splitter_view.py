import os
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, Http404
from django.http import JsonResponse
from pydub import AudioSegment
from django.urls import reverse
from wsgiref.util import FileWrapper

def upload_mp3(request):
    if request.method == 'POST' and request.FILES.get('mp3file'):
        mp3_file = request.FILES['mp3file']
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        filename = mp3_file.name
        chunk_type=request.POST.get('type', 2)

        # Construct the absolute file path
        file_path = os.path.join(temp_dir, filename)

        # Save the file manually
        with open(file_path, 'wb+') as destination:
            for chunk in mp3_file.chunks():
                destination.write(chunk)
        try:
            # Load the MP3 file using pydub
            audio = AudioSegment.from_file(file_path)
            chunks = []

            if chunk_type == 1:
            ####################################################################################
                # exact 1 minute chunk
                # Split into 1-minute chunks
                one_minute = 60 * 1000  # 1 minute in milliseconds
                chunks = [audio[i:i+one_minute] for i in range(0, len(audio), one_minute)]
            ####################################################################################
            else:
            ####################################################################################
            # lets work in milisecond
                one_minute = 60 * 1000
                overlap = 2 * 1000

                start_time = 0  # Initial start time for chunk 1

                audio_length = len(audio)
                while start_time + one_minute <= audio_length:
                    end_time = start_time + one_minute
                    chunks.append(audio[start_time:end_time])

                    start_time = (end_time - overlap)

                remaining_duration = len(audio) % one_minute // 1000  # In seconds
                remaining_audio = audio[start_time:]
                
                if len(remaining_audio) > 0:
                    chunks.append(remaining_audio)
            ####################################################################################


            # Prepare directory for output
            output_dir = os.path.join(settings.MEDIA_ROOT, 'splits')
            os.makedirs(output_dir, exist_ok=True)  # Ensure splits directory exists

            # Save each chunk and generate download links
            download_links = []
            for idx, chunk in enumerate(chunks):
                chunk_filename = f"chunk_{idx + 1}_{filename}"
                output_path = os.path.join(output_dir, chunk_filename)
                chunk.export(output_path, format="mp3")
                download_links.append({
                    'download_link': reverse('download_chunk', args=[chunk_filename]),
                    'filename': chunk_filename
                })

            total_chunks = len(chunks)
            remaining_duration = len(audio) % one_minute // 1000  # In seconds

            os.remove(file_path)

            return JsonResponse({
                "message": "MP3 file split successfully!",
                "total_chunks": total_chunks,
                "remaining_duration": remaining_duration,
                "download_links": download_links,
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, 'upload.html')

def download_chunk(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'splits', filename)

    if os.path.exists(file_path):
        response = FileResponse(
            FileWrapper(open(file_path, 'rb')),
            content_type='audio/mpeg',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    else:
        raise Http404("File not found")
