from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Lecture

# Create your views here.

def index(request):
    lectures = Lecture.objects.all()
    template = loader.get_template('views/index.html')
    return HttpResponse(template.render({'lectures': lectures}, request))

def videos(request, class_id):
    return HttpResponse("This is where the list of summaries for a lecture " +
                        str(class_id) + "will go.")

def summary(request, summary_id):
    return HttpResponse("summary: " + str(summary_id))
