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
    context = {
        'lectures': lectures,
        }
    return HttpResponse(template.render(context, request))

def videos(request, class_id):
    lecture = Lecture.objects.get(id=class_id)
    videos = lecture.video_set.order_by("-presentation_date").all()
    template = loader.get_template("views/video.html")

    test = [[video, video.presenters[:-2].split(';')] for video in videos]
    print(test)

    context = {
        "lecture": lecture,
        "videos": videos,
        "names": test,
    }
    return HttpResponse(template.render(context, request))

def summary(request, summary_id):
    template = loader.get_template("views/summary.html")
    
    vid = Video.objects.get(pk=summary_id)
    lecture = Lecture.objects.get(id=vid.lecture_id.id)
    
    topics = vid.topics.all()

    tps = []

    for topic in topics:
        bps = topic.bulletpoints.split(" -")
        bps = [i.split("\n-") for i in bps]
        bps = flatten_list(bps)
        filtered_bps = []
        for bp in bps:
            if not (bp.isspace() or bp == "" or istitle(bp)):
                bp = bp.replace("\n", "")
                filtered_bps.append(bp)

        chunk1 = topic.chunk1
        chunk2 = topic.chunk2
        chunk3 = topic.chunk3

        chunks = []

        if chunk1 != None:
            chunks.append(chunk1)
        if chunk2 != None:
            chunks.append(chunk2)
        if chunk3 != None:
            chunks.append(chunk3)

        tps.append(
            {
                "title": topic.title,
                "bulletpoints": filtered_bps,
                "summary": topic.summary,
                "chunks": chunks,
            }
        )
               

    # Iterate over topic_list by doing for topic in topic_list and then access topic fields with topic.title, topic.bulletpoints, topic.summary, topic.chunks

    context = {
        "lecture": lecture,
        "video": vid,
        "topic_list": tps,
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
