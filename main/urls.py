from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.upload_mp3, name="upload"),
    path("splitter/download/<str:filename>/", views.download_chunk, name="download_chunk"),

    path("backtrack/download/", views.download_backtrack, name="download_backtrack"),
    path("backtrack/final-destination/", views.final_destination, name="final_destination"),
    path("backtrack/download/<str:filename>/", views.download_backtrack_file, name="download_backtrack_file"),

    path("merger/download/<str:filename>/", views.download_file_merge, name="download_file_merge"),
    path("merger/merge-mp3/", views.merge_mp3, name="merge_mp3"),

    path('api', include([
        path('generate-attachment/', views.generate_attachment, name='generate_attachment'),
        path('obtain-secret-token/', views.obtain_secret_token, name='obtain_secret_token'),
        # path('generate-backing-track/', views.generate_backing_track, name='generate_backing_track')
    ]))
]
