from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_mp3, name="upload"),
    path("splitter/download/<str:filename>/", views.download_chunk, name="download_chunk"),

    path("backtrack/download/", views.download_backtrack, name="download_backtrack"),
    path("backtrack/download/<str:filename>/", views.download_backtrack_file, name="download_backtrack_file"),

    path("merger/download/<str:filename>/", views.download_file_merge, name="download_file_merge"),
    path("merger/merge-mp3/", views.merge_mp3, name="merge_mp3"),
]
