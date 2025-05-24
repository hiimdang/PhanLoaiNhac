from django.db import models
from django.utils import timezone
from mutagen import File
import os

class Song(models.Model):
    title = models.CharField(max_length=255) 
    artist = models.CharField(max_length=255)
    lyrics = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.audio_file:
            file_path = self.audio_file.path
            try:
                audio = File(file_path)
                if audio and audio.info.length:
                    minutes = int(audio.info.length // 60)
                    seconds = int(audio.info.length % 60)
                    self.duration = f"{minutes:02}:{seconds:02}"
                    super().save(update_fields=["duration"])
            except Exception as e:
                print(f"❌ Lỗi khi lấy duration: {e}")
