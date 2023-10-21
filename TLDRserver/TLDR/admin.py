from django.contrib import admin

# Register your models here.
from .models import Lecture, Video

admin.site.register(Lecture)
admin.site.register(Video)
