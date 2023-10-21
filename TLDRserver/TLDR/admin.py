from django.contrib import admin

# Register your models here.
from .models import Lecture, Video, Topic, Tag

admin.site.register(Lecture)
admin.site.register(Video)
admin.site.register(Topic)
admin.site.register(Tag)
