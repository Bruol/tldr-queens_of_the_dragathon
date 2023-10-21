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
    template = loader.get_template("views/summary.html")
    
    vid = Video.objects.get(pk=summary_id)
    
    topics = vid.topics.all()

    for topic in topics:
        bps = topic.bulletpoints.split(" -")
        bps = [i.split("\n-") for i in bps]
        bps = flatten_list(bps)
        filtered_bps = []
        for bp in bps:
            if not (bp.isspace() or bp == "" or istitle(bp)):
                bp = bp.replace("\n", "")
                filtered_bps.append(bp)
               

    tp_dict = {
        "title": vid.infered_titel,
        "topics": topics,
        "bulletpoints": filtered_bps,
        "presenter": vid.presenters[:-1],
        "date": vid.presentation_date,
        "trasncript": vid.transcript,
        "source": vid.source_url,
    }

    context = {
        "lecture": tp_dict, 
    }
    
    return HttpResponse(template.render(context, request))



def istitle(str):
    if(len(str) < 60 and str.count(":") > 0):
        return True
    else:
        return False
    
def flatten_list(nested_list):
    flattened = []
    for i in nested_list:
        if isinstance(i, list):
            flattened.extend(flatten_list(i))
        else:
            flattened.append(i)
    return flattened