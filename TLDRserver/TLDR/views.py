from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Lecture

# Create your views here.

def index(request):
    latest_lecture = Lecture.objects.order_by("-lecture_number")[1]
    template = loader.get_template("views/index.html")
    context = {
        "lecture": latest_lecture,
    }
    return HttpResponse(template.render(context, request))

def videos(request, class_id):
    latest_lecture = Lecture.objects.order_by("-lecture_number")[1]
    template = loader.get_template("views/video.html")
    context = {
        "lecture": latest_lecture,
    }
    return HttpResponse(template.render(context, request))

def summary(request, summary_id):
    latest_lecture = Lecture.objects.order_by("-lecture_number")[1]
    template = loader.get_template("views/summary.html")
    context = {
        "lecture": latest_lecture,
    }
    return HttpResponse(template.render(context, request))
