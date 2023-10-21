from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import *
from django.template import loader

from .models import Lecture

# Create your views here.

def index(request):
    lectures = Lecture.objects.all()
    template = loader.get_template('views/index.html')
    return HttpResponse(template.render({'lectures': lectures}, request))

def videos(request, class_id):
    lecture = Lecture.objects.get(id=class_id)
    videos = lecture.video_set.order_by("-presentation_date").all()
    template = loader.get_template("views/video.html")
    context = {
        "lecture": lecture,
        "videos": videos,
    }
    return HttpResponse(template.render(context, request))

def summary(request, summary_id):
    latest_lecture = Lecture.objects.order_by("-lecture_number")[1]
    template = loader.get_template("views/summary.html")
    
    vid = Video.objects.get(pk=summary_id)
    
    topics = vid.topics.all()

    context = {
        "lecture": latest_lecture,

    }
    return HttpResponse(template.render(context, request))

def get_dict():
    print("test")
