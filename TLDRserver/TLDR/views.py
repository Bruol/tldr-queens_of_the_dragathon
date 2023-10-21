from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
     return HttpResponse("Hello, world. You're at the TLDR index.")

def videos(request, class_id):
    return HttpResponse("This is where the list of summaries for a lecture " +
                        str(class_id) + "will go.")

def summary(request, summary_id):
    return HttpResponse("summary: " + str(summary_id))
