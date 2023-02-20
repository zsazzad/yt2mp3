import os
import ssl
from pytube import YouTube
from moviepy.editor import *
from django.shortcuts import render

# Disable SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

def downloader(request):
    if request.method == 'POST':
        # Get the YouTube video URL from the form
        
        url = request.POST['ytlink']

        # Download the video
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        video.download()

        # Convert the video to MP3
        video_path = video.default_filename
        mp3_path = f"{os.path.splitext(video_path)[0]}.mp3"
        video_clip = AudioFileClip(video_path)
        video_clip.write_audiofile(mp3_path)
        video_clip.close()

        # Delete the original video
        os.remove(video_path)

        # Return the path to the saved MP3 file
        return render(request, 'index.html', {'mp3_path': mp3_path})

    else:
        # If the request is not a POST request, render the download form
        return render(request, 'index.html')
