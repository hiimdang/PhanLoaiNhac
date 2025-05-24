from django.contrib import admin
from .models import Song

class SongAdmin(admin.ModelAdmin):
    exclude = ('duration',)

admin.site.register(Song, SongAdmin)
